import datetime as dt
import os

__log_file = './resources/log_file.txt'
if not os.path.exists(__log_file):
    with open(__log_file, 'w+') as f: f.close()

def __write_log(log: str):
    time = dt.datetime.now().strftime('"%m/%d/%Y, %H:%M:%S"')
    log = '({})::{}\n'.format(time, log)
    f = open(__log_file, 'a')
    f.write(log)
    f.close()
    print('Logged: ', log)


def log_error(err_msg: str):
    line = "ERROR::{}".format(err_msg)
    __write_log(line)

def log_info(info_msg: str):
    line = "INFO::{}".format(info_msg)
    __write_log(line)

def log_boot(boot_info: str):
    line = 'BOOT::{}'.format(boot_info)
    __write_log(line)
