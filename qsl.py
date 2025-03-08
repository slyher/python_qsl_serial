import adif_io
import os


def copy_files(current_path) -> str:
    os.system("cp ./tex/qslf.pdf " + current_path)
    os.system("cp ./img/qsl_r.jpg "+current_path)
    os.system("cp ./tex/qsl.tex " + current_path)
    os.system("cp ./tex/qsl_r.tex " + current_path)
    return current_path + "/qsl_r.tex"

def create_working_directory_for_qso(qso -> dict) -> str:
    qsl_directory = qso["CALL"].replace("/","-") + qso["TIME_ON"]
    current_path = os.path.join(dist_directory, qso["CALL"].replace("/","-") + qso["TIME_ON"])
    os.mkdir(current_path)
    return [current_path, qsl_directory]

def create_email_file_for_qso(email- > str, current_path -> str):
    os.system("echo " +email+ " >> "+ current_path + "/mail")
    
def update_qsl_content(qso -> dict,content -> str) -> str:
    return content.replace("[CALL]",qso["CALL"].replace("/","{\slash}")).replace("[TIME]",qso["TIME_ON"][:2]+":"+qso["TIME_ON"][2:]).replace("[FREQ]",qso["FREQ"]).replace("[MODE]",qso["MODE"]).replace("[RST-RECV]",qso["RST_SENT"])
    
def write_qsl_for_qso(content->str, qsl_r_file_name -> str):
    f = open(qsl_r_file_name, "w")
    f.write(content)
    f.close()

def generate_qsl_with_latex(qsl_directory):
    os.system("./qsl.sh " + qsl_directory)

def preparing_environment_for_generating_qsl_with_qso(qso -> dict):
    current_path, qsl_directory = create_working_directory_for_qso(qso)
    if "EMAIL" in qso:
        create_email_file_for_qso( qso["EMAIL"], current_path)
    qsl_r_file_name = copy_files(current_path)
    if "RST_SENT" not in qso:
        qso["RST_SENT"] = "-"
    return [qso,qsl_r_file_name, qsl_directory]

def generate_qsl_with_qso(qso -> dict):
    qso,qsl_r_file_name, qsl_directory = preparing_environment_for_generating_qsl_with_qso(qso)
    with open(qsl_r_file_name, "r") as f:
        content = update_qsl_content(f.read())
    f.close()
    write_qsl_for_qso(content, qsl_r_file_name)
    generate_qsl_with_latex(qsl_directory)
    
filename="hf23wtte.log.adi"
dist_directory = os.path.join(os.getcwd(), "dist")

qsos, headers = adif_io.read_from_file(filename)

for qso in qsos:
    generate_qsl_with_qso(qso)
    