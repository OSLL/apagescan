import glob
import os
import random
from subprocess import CalledProcessError

from PyQt5.QtCore import QTimer, QEventLoop
from PyQt5.QtGui import QColor

from device_interaction import exec_command


def generate_color():
    """Generates random color"""
    red = int(random.randrange(0, 255))
    green = int(random.randrange(0, 255))
    blue = int(random.randrange(0, 255))
    alpha = 255
    return QColor(red, green, blue, alpha)


def sleep(sec):
    """Stops application

    :param sec: amount of seconds to sleep for
    """
    loop = QEventLoop()
    QTimer.singleShot(sec * 1000, loop.quit)
    loop.exec_()


def clean_tmp_data_from_device(device, remove_page_data=True, remove_pids_data=True):
    """Removes data from connected android device

    :param remove_page_data: true if page data has to be removed, false if not
    :param remove_pids_data: true if pids data has to be removed, false if not
    """
    page_data_mask = '*_page_data'
    pids_file_mask = '*.csv'
    # Remove binary data from telephone
    try:
        if remove_page_data:
            exec_command(f'adb -s {device}', 'shell', 'rm', f'/data/local/testing/{page_data_mask}')
        if remove_pids_data:
            exec_command(f'adb -s {device}', 'shell', 'rm', f'/data/local/testing/{pids_file_mask}')
    except CalledProcessError:
        pass


def clean_tmp_data(remove_page_data=True, remove_pictures_data=True, remove_pids_data=True):
    """Removes data from PC

    :param remove_page_data: true if page data has to be removed, false if not
    :param remove_pids_data: true if pids data has to be removed, false if not
    :param remove_pictures_data: true if pictures data has to be removed, false if not
    """
    page_data_mask = '*_page_data'
    picture_mask = '*.png'
    pid_list_mask = '*.csv'

    file_list = []
    picture_list = []
    pid_list = []

    if remove_pids_data:
        pid_list = glob.glob(f'./resources/data/pids_data/{pid_list_mask}')
    if remove_page_data:
        file_list = glob.glob(f'./resources/data/binary_page_data/{page_data_mask}')
    if remove_pictures_data:
        picture_list = glob.glob(f'./resources/data/pictures/*/{picture_mask}')

    for file in file_list + picture_list + pid_list:
        try:
            if os.path.isfile(file):
                os.remove(file)
        except Exception as ex:
            print(ex)
