import glob
import os
import random
from subprocess import CalledProcessError

from PyQt5.QtCore import QTimer, QEventLoop
from PyQt5.QtGui import QColor
from intervaltree import Interval, IntervalTree

from device_interaction import exec_command


def generate_color():
    red = int(random.randrange(0, 255))
    green = int(random.randrange(0, 255))
    blue = int(random.randrange(0, 255))
    alpha = 255
    return QColor(red, green, blue, alpha)


def sleep(sec):
    loop = QEventLoop()
    QTimer.singleShot(sec * 1000, loop.quit)
    loop.exec_()


def clean_tmp_data_from_device(device, remove_page_data=True, remove_pids_data=True):
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


def create_regions_map(page_data={}):
    """
        Function creates map of processes regions in RAM
        Region means continuous block of pages,
        represented like (start_pfn, end_pfn, pid)
        Regions inserted into tree, to search
        which regions contain particular page by given pfn
    """
    regions = IntervalTree()
    for pid, data in page_data.items():
        pages_info = sorted(data.values, key=lambda el: el[0])  # sort by pfn

        if len(pages_info) > 0:
            bound = pages_info[0][0]
        else:
            break

        for i in range(len(pages_info) - 1):
            if pages_info[i][0] + 1 != pages_info[i + 1][0]:
                regions.add(Interval(bound, pages_info[i][0] + 1, pid))
                bound = pages_info[i + 1][0]
    return regions