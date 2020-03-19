"""Contains functions to work with connected android device and DeviceInteraction class

Functions provide interface to interact with connected Android device and collect
page by page memory data about processes running on a device. DeviceInteraction class
combines these functions along with convenient storage of collected data

Usage example:
    connection = DeviceInteraction()
    connection.set_device("04322b6c2208c98b")
    connection.adb_collect_all_pid_list()
    pid_list = connection.get_all_pid_list()
"""

import re
import struct
import subprocess
from collections import OrderedDict
from subprocess import SubprocessError

import numpy as np
import pandas as pd
from pandas.errors import EmptyDataError


def get_bit(data, shift):
    """Get the flag information from data

    :param data: 32-bit number, containing info about flags for 1 page
    :param shift: bit offset for certain flag checking
    :return: 0 or 1 (ex. 1 if page present : 0 if swapped for shift=26)
    :rtype: Int
    """
    return (data >> shift) & 1


def exec_command(*args, print_output=False):
    """Executes command using subprocess module

    :param args: arguments of a command to be executed
    :param print_output: True is output has to be printed, False if not
    :return: the console output for executed command
    :rtype: byte
    """
    exec_str = ' '.join(args)
    output = subprocess.check_output(exec_str, shell=True)
    if print_output:
        print(output.decode('UTF-8'))
    return output


def read_page_data(pid):
    """Reads binary data for pages of a given pid and convert it to list of tuples.
    One tuple is one page. Tuple is kind of (<Swap offset or page address>, <flag>, <flag>, ...)

    :param pid: pid
    :return: list containing information about each page
    :rtype: List
    :raises EmptyDataError: if no data was stored for current pid
    """
    # The number of bytes for offset (address) and flags in binary file
    offset_size = 8
    flags_size = 4
    data = []
    file = f'resources/data/binary_page_data/{pid}_page_data'
    # Opens a file in byte reading mode
    with open(file, 'rb') as f:
        # Read the first 8 bytes as offset and next 4 bytes as flags
        offset = f.read(offset_size)
        flags = f.read(flags_size)
        while offset and flags:
            # Convert to uint64_t
            offset = struct.unpack('Q', offset)[0]
            # Convert to uint32_t
            flags = struct.unpack('I', flags)[0]
            data.append((offset,  # Swap offset or page address
                         get_bit(flags, shift=26),  # return 1 if page present : 0 if swapped
                         get_bit(flags, shift=4),  # return 1 if page dirty : 0 if clean
                         get_bit(flags, shift=12)))  # return 1 if page anonymous : 0 if not
            # Read address
            offset = f.read(offset_size)
            flags = f.read(flags_size)

    # Throw exception if no data in list
    if data:
        return data
    else:
        raise EmptyDataError


def adb_cgroups_list(device):
    """Searches control groups in /proc/mounts file and returns paths to it's tasks files

    :param device: device's serial number
    :return: list of paths to control groups' tasks files
    :rtype: List
    """
    try:
        raw_data = str(exec_command(f'adb -s {device}', 'shell', 'cat', '/proc/mounts'))
    except SubprocessError:
        raw_data = ''
    return list(map(lambda x: x + '/tasks', re.findall(r'(\S+) cgroup ', raw_data)))


def adb_collect_pid_list(device, tool, filename, pull_path, group_name):
    """Collect list of processes from device

    :param device: target device's serial number
    :param tool: script name on android device (get_pid_list or read_cgroup)
    :param filename: data filename on android device
    :param pull_path: path for data on PC
    :param group_name: control group to collect list of processes from; group_name='' for get_pid_list tool
    :return: list of processes like [[<pid>, <process full name>], [<pid>, <process full name>]...]
    :rtype: numpy.ndarray
    """
    exec_command(f'adb -s {device}',
                 'shell',
                 f'/data/local/testing/{tool}',
                 '/data/local/testing/',
                 group_name)
    # pull pid list from device
    exec_command(f'adb -s {device}',
                 'pull',
                 f'/data/local/testing/{filename}.csv',
                 f'./resources/data/{pull_path}',
                 print_output=True)
    return pd.read_csv(f'resources/data/{pull_path}/{filename}.csv', sep=',', header=None).values


def adb_collect_page_data(device, pid_list):
    """Collect information about memory pages

    :param device: target device's serial number
    :param pid_list: list of processes to be examined
    :return: page_data - info about all pages for each pid from pid_list, except error_pids,
    present_data - info about all PRESENT pages for each pid from pid_list,
    swapped_data - info about all SWAPPED pages for each pid from pid_list,
    error_pids - list of pids, to which there was no access
    :rtype: OrderedDict, OrderedDict, OrderedDict, List
    """
    page_data = OrderedDict()
    swapped_data = OrderedDict()
    present_data = OrderedDict()
    error_pids = []
    for pid in pid_list:
        try:
            filename = f'{pid}_page_data'
            # collect raw data on device
            exec_command(f'adb -s {device}',
                         'shell',
                         '/data/local/testing/pagemap',
                         str(pid),
                         '/data/local/testing',
                         print_output=True)
            # pull raw data
            exec_command(f'adb -s {device}',
                         'pull',
                         f'/data/local/testing/{filename}',
                         './resources/data/binary_page_data',
                         print_output=True)
            # create data from raw data
            data = read_page_data(pid)
        except (SubprocessError, EmptyDataError):
            error_pids.append(pid)
            continue

        p_data = list(filter(lambda el: el[1] == 1, data))
        s_data = list(filter(lambda el: el[1] == 0, data))
        page_data[pid] = pd.DataFrame(np.array(data))
        present_data[pid] = pd.DataFrame(np.array(p_data))
        swapped_data[pid] = pd.DataFrame(np.array(s_data))
    return page_data, present_data, swapped_data, error_pids


class DeviceInteraction:
    """
    Class for interaction with Android device and collection of device's running processes' pagedata

    :ivar __device: serial number of connected android device
    :ivar __page_data: processes' memory pagedata
    :ivar __present_page_data: processes' present memory pagedata
    :ivar __swapped_page_data: processes' swapped memory pagedata
    :ivar __error_pids: list of pids, for which data couldn't be collected
    :ivar __pid_list_all: list of all running processes' pids on connected device
    :ivar __pid_list_cgroup: list of processes' pids  in chosen cgroup, running on connected device
    :ivar __cgroups_list: list of connected device's available cgroups
    :ivar iterations: number of iterations of data collecting
    """
    def __init__(self):
        self.__device = None
        self.__page_data = {}
        self.__present_page_data = {}
        self.__swapped_page_data = {}
        self.__error_pids = []
        self.__pid_list_all = []
        self.__pid_list_cgroup = []
        self.__cgroups_list = []
        self.__iterations = None

    @property
    def pid_list_all(self):
        """List of all running processes' pids

        :getter: returns list of all pids from device
        :type: List
        """
        return self.__pid_list_all

    @property
    def pid_list_cgroup(self):
        """List of processes' pids  in chosen cgroup

        :getter: returns list of all pids from cgroup
        :type: List
        """
        return self.__pid_list_cgroup

    @property
    def cgroups_list(self):
        """List of connected device's available cgroups

        :getter: returns list of all available cgroups
        :type: List
        """
        return self.__cgroups_list

    def get_page_data(self, iteration=None, present=False, swapped=False):
        """Returns processes' memory pagedata

        :param iteration: number of collecting iteration
        :param present: True if only present pages are required, False if not
        :param swapped: True if only swapped pages are required, False if not

        :return: returns processes' memory pagedata
        :rtype: Dict
        """
        if not present and not swapped:
            return self.__page_data if iteration is None else self.__page_data.get(iteration)
        elif present:
            return self.__present_page_data if iteration is None else self.__present_page_data.get(iteration)
        else:
            return self.__swapped_page_data if iteration is None else self.__swapped_page_data.get(iteration)

    @property
    def iterations(self):
        """Number of iterations of data collecting

        :getter: returns total amount of iterations
        :type: Int
        """
        return self.__iterations

    def set_device(self, device):
        """Sets working device to get data

        :param device: device's serial number
        :return: None
        """
        self.__device = device

    def clear(self):
        """Removes collected data

        :return: None
        """
        self.__pid_list_cgroup = []
        self.__pid_list_all = []
        self.__cgroups_list = []
        self.__error_pids = []

    def set_iterations(self, iterations):
        """Sets total amount of iterations and initializes page_data structures

        :param iterations: amount to be set
        :return: None
        """
        self.__iterations = iterations

        for i in range(self.__iterations):
            self.__page_data.setdefault(i, OrderedDict())
            self.__present_page_data.setdefault(i, OrderedDict())
            self.__swapped_page_data.setdefault(i, OrderedDict())

    def collect_cgroups_list(self):
        """Collects list of available cgroups from a device

        :return: None
        """
        self.__cgroups_list = adb_cgroups_list(self.__device)

    def collect_pid_list_all(self):
        """Collects list of all processes running on a device

        :return: None
        """
        try:
            pid_list_all = adb_collect_pid_list(self.__device,
                                                tool='get_pid_list',
                                                filename='pid_list',
                                                pull_path='pids_data',
                                                group_name='')
            self.__pid_list_all = pid_list_all.tolist()
        except (SubprocessError, EmptyDataError):
            self.__pid_list_all = []
            raise

    def collect_pid_list_cgroup(self, group=''):
        """Collects list of all processes in a given cgroup running on a device

        :param group: cgroup name
        :return: None
        """
        try:
            pid_list_cgroup = adb_collect_pid_list(self.__device,
                                                   tool='read_cgroup',
                                                   filename='group_list',
                                                   pull_path='pids_data',
                                                   group_name=group)
            self.__pid_list_cgroup = pid_list_cgroup.tolist()
        except (SubprocessError, EmptyDataError):
            self.__pid_list_cgroup = []
            raise

    def collect_page_data(self, cur_iteration, pid_list):
        """Collects information about memory pages

        :param cur_iteration: current iteration of collecting
        :param pid_list: list of pids to collect data from
        :return: list of pids, for which data couldn't be collected
        :rtype: List
        """
        page_data, present_data, swapped_data, error_pids = adb_collect_page_data(self.__device, pid_list)
        self.__page_data[cur_iteration] = page_data
        self.__present_page_data[cur_iteration] = present_data
        self.__swapped_page_data[cur_iteration] = swapped_data
        return error_pids
