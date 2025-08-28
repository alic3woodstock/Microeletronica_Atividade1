import hashlib
import logging
import os
from time import ctime, strftime
from kivy.uix.label import CoreLabel

LOGLEVEL = logging.ERROR
FORMAT = '%(levelname)s: %(asctime)s - %(message)s'
APPVERSION = "2.04.00"
WINE_GZDOOM = True  # linux gzdoom works only on ubuntu for now.
RE_DOWNLOAD = False

text_color = [1, 1, 1, 1]
highlight_color = [0.5, 0, 0, 1]
background_color = [0, 0, 0, 1]
button_height = 42
button_width = 128


def log(text, error=True):
    text = str(text)
    data_path = os.path.realpath(__file__)
    data_path = data_path.replace("functions.py", "")
    ctime()
    log_text = ''
    if error:
        log_text = '[ERROR] ' + strftime("%Y-%m-%d %H:%M:%S") + ' - ' + text + '\n'
    elif LOGLEVEL == logging.DEBUG:
        log_text = '[DEBUG] ' + strftime("%Y-%m-%d %H:%M:%S") + ' - ' + text + '\n'
    if log_text.strip():
        with open(data_path + 'main.log', 'a') as log_file:
            log_file.writelines(log_text)
            log_file.close()


def filehash(file_name):
    sha256hash = ""
    if os.path.isfile(file_name):
        try:
            with open(file_name, 'rb') as f:
                data = f.read()
                sha256hash = hashlib.sha256(data).hexdigest()
        except Exception as e:
            log(e)
    return sha256hash


def version_number():
    str_version = APPVERSION.replace(".", "")
    return int(str_version)

def canvas_label(**kwargs):
    label = CoreLabel(**kwargs)
    return label