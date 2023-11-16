import adif_io
import os

filename="hf23wtte.log.adi"
dist_directory = os.path.join(os.getcwd(), "dist")

qsos, headers = adif_io.read_from_file(filename)

for qso in qsos:
    current_path = os.path.join(dist_directory, qso["CALL"].replace("/","-") + qso["TIME_ON"])
    os.mkdir(current_path)
    if "EMAIL" in qso:
        os.system("echo " +qso["EMAIL"]+ " >> "+ current_path + "/mail")
    os.system("cp ./tex/qslf.pdf " + current_path)
    os.system("cp ./img/qsl_r.jpg "+current_path)
    os.system("cp ./tex/qsl.tex " + current_path)
    os.system("cp ./tex/qsl_r.tex " + current_path)
    qsl_r_file = current_path + "/qsl_r.tex"
    if "RST_SENT" not in qso:
        qso["RST_SENT"] = "-"
    with open(qsl_r_file, "r") as f:
        contents = f.read()
        contents = contents.replace("[CALL]",qso["CALL"].replace("/","{\slash}")).replace("[TIME]",qso["TIME_ON"][:2]+":"+qso["TIME_ON"][2:]).replace("[FREQ]",qso["FREQ"]).replace("[MODE]",qso["MODE"]).replace("[RST-RECV]",qso["RST_SENT"])
    f.close()
    f = open(qsl_r_file, "w")
    f.write(contents)
    f.close()
    os.system("./qsl.sh " + qso["CALL"]+qso["TIME_ON"])
