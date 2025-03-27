import adif_io
import os


def copy_files(current_path) -> str:
    """
    The function `copy_files` copies specific files to a specified directory and returns the path to a
    specific file.

    :param current_path: The `copy_files` function takes the `current_path` as a parameter, which is the
    destination path where the files will be copied. The function copies four files (`qslf.pdf`,
    `qsl_r.jpg`, `qsl.tex`, `qsl_r.tex`) from their respective source
    :return: The function `copy_files` is returning the path to the copied file "qsl_r.tex" within the
    specified `current_path`. The returned value will be in the format `current_path + "/qsl_r.tex"`.
    """
    os.system("cp ./tex/qslf.pdf " + current_path)
    os.system("cp ./img/qsl_r.jpg " + current_path)
    os.system("cp ./tex/qsl.tex " + current_path)
    os.system("cp ./tex/qsl_r.tex " + current_path)
    return current_path + "/qsl_r.tex"


def create_working_directory_for_qso(qso -> dict) -> str:
    """
    This function creates a working directory for a QSO (amateur radio contact) based on the call sign
    and time of the contact.

    :param dict: The function `create_working_directory_for_qso` takes a dictionary `qso` as input and
    creates a working directory based on the values in the dictionary. The dictionary `qso` likely
    contains information related to a radio communication contact, such as the call sign and time of the
    contact
    :return: A list containing the current path and the QSL directory name is being returned.
    """
    qsl_directory = qso["CALL"].replace("/", "-") + qso["TIME_ON"]
    current_path = os.path.join(
        dist_directory, qso["CALL"].replace(
            "/", "-") + qso["TIME_ON"])
    os.mkdir(current_path)
    return [current_path, qsl_directory]


def create_email_file_for_qso(email - > str, current_path -> str):
    """
    The function `create_email_file_for_qso` appends an email address to a file named "mail" in the
    specified directory.

    :param email: The `email` parameter is a string that represents the email address that you want to
    write to a file
    :param current_path: The `current_path` parameter is a string that represents the path to the
    directory where you want to create the email file. This path should be the location where you want
    to store the email file named "mail"
    """
    os.system("echo " + email + " >> " + current_path + "/mail")


def update_qsl_content(qso -> dict, content -> str) -> str:
    """
    The function `update_qsl_content` updates a given content string with specific values from a QSO
    dictionary.

    :param dict: The `update_qsl_content` function takes two parameters:
    :param content: The `content` parameter is a string that contains placeholders such as `[CALL]`,
    `[TIME]`, `[FREQ]`, `[MODE]`, and `[RST-RECV]`. The function `update_qsl_content` takes a dictionary
    `qso` and a string `content`
    :return: The function `update_qsl_content` is returning a string with placeholders `[CALL]`,
    `[TIME]`, `[FREQ]`, `[MODE]`, and `[RST-RECV]` replaced by corresponding values from the `qso`
    dictionary.
    """
    qso_call = qso["CALL"].replace("/", "{\\slash}")
    qso_time = qso["TIME_ON"][:2] + ":" + qso["TIME_ON"][2:]
    qso_freq = qso["FREQ"]
    qso_mode = qso["MODE"]

    return content.replace(
        "[CALL]",
        qso_call).replace(
        "[TIME]",
        qso_time).replace(
            "[FREQ]",
            qso_freq).replace(
                "[MODE]",
                qso_mode).replace(
                    "[RST-RECV]",
        qso["RST_SENT"])


def write_qsl_template_for_qso(content -> str, qsl_r_file_name -> str):
    """
    The function `write_qsl_template_for_qso` writes the provided content to a file with the specified
    file name.

    :param content: The `content` parameter in the `write_qsl_template_for_qso` function is a string
    that represents the content you want to write to a file. This content could be a template for a QSL
    (confirmation of a two-way radio communication) that you want to save to a file
    :param qsl_r_file_name: The `qsl_r_file_name` parameter is the name of the file where you want to
    write the content. It should be a string representing the file name or the path to the file where
    you want to save the content
    """
    f = open(qsl_r_file_name, "w")
    f.write(content)
    f.close()


def generate_qsl_with_latex(qsl_directory):
    """
    The function `generate_qsl_with_latex` executes a shell script `qsl.sh` with the provided directory
    as an argument.

    :param qsl_directory: The `qsl_directory` parameter in the `generate_qsl_with_latex` function
    represents the directory where the QSL (QSL cards) files are located. This function seems to be
    calling a shell script named `qsl.sh` with the provided directory as an argument to generate QSL
    """
    os.system("./qsl.sh " + qsl_directory)


def preparing_environment_for_generating_qsl_with_qso(qso -> dict):
    """
    The function prepares the environment for generating QSL with QSO by creating a working directory,
    copying files, and handling email information.

    :param dict: The function `preparing_environment_for_generating_qsl_with_qso` takes a dictionary
    `qso` as input and performs the following tasks:
    :return: The function `preparing_environment_for_generating_qsl_with_qso` is returning a list
    containing the following items:
    1. The QSO dictionary with any modifications made during the preparation process.
    2. The filename of the copied QSL files.
    3. The directory where the QSL files are stored.
    """
    current_path, qsl_directory = create_working_directory_for_qso(qso)
    if "EMAIL" in qso:
        create_email_file_for_qso(qso["EMAIL"], current_path)
    qsl_r_file_name = copy_files(current_path)
    if "RST_SENT" not in qso:
        qso["RST_SENT"] = "-"
    return [qso, qsl_r_file_name, qsl_directory]


def generate_qsl_with_qso(qso -> dict):
    """
    The function generates a QSL card using a QSO dictionary and LaTeX templates.

    :param dict: The `generate_qsl_with_qso` function seems to be a part of a larger script or program
    related to generating QSL cards for amateur radio contacts
    """
    qso, qsl_r_file_name, qsl_directory = preparing_environment_for_generating_qsl_with_qso(
        qso)
    with open(qsl_r_file_name, "r") as f:
        content = update_qsl_content(f.read())
    f.close()
    write_qsl_template_for_qso(content, qsl_r_file_name)
    generate_qsl_with_latex(qsl_directory)


filename = "hf23wtte.log.adi"
dist_directory = os.path.join(os.getcwd(), "dist")

qsos = adif_io.read_from_file(filename)[0]

for qso in qsos:
    generate_qsl_with_qso(qso)
