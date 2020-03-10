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
from subprocess import CalledProcessError

import numpy as np
import pandas as pd
from pandas.errors import EmptyDataError


def get_bit(data, shift):
    """Checks whether bit is 1 or 0

    :param data: given number
    :param shift: bit offset"""
    return (data >> shift) & 1


def exec_command(*args, print_output=False):
    """Executes command using subprocess module

    :param args: arguments of a command to be executed
    :param print_output: true is output has to be printed, false if not
    """
    exec_str = ' '.join(args)
    output = subprocess.check_output(exec_str, shell=True)
    if print_output:
        print(output.decode('UTF-8'))
    return output


def read_page_data(pid):
    """Reads pages of a given pid

    :param pid: pid
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
            # Convert to long long unsigned and to unsigned int
            offset = struct.unpack('Q', offset)[0]
            flags = struct.unpack('I', flags)[0]
            data.append([offset,  # Swap offset or page address
                         get_bit(flags, shift=26),  # return 1 if page present : 0 if swapped
                         get_bit(flags, shift=4),  # return 1 if page dirty : 0 if clean
                         get_bit(flags, shift=12)])  # return 1 if page anonymous : 0 if not
            # Read address
            offset = f.read(offset_size)
            flags = f.read(flags_size)

    # Throw exception if no data in list
    if data:
        return data
    else:
        raise EmptyDataError


def adb_cgroups_list(device):
    """Get control groups list from device

    :param device: device
    """
    try:
        raw_data = str(exec_command(f'adb -s {device}', 'shell', 'cat', '/proc/mounts'))
    except CalledProcessError:
        raw_data = ''
    return list(map(lambda x: x + '/tasks', re.findall(r'(\S+) cgroup ', raw_data)))


def adb_collect_pid_list(device, tool, filename, pull_path, group):
    """Collect pid list from device

    :param device: target device
    :param tool: script name on android device
    :param filename: data filename on android device
    :param pull_path: path for data on PC
    :param group: control group to collect pid list from
    """
    exec_command(f'adb -s {device}',
                 'shell',
                 f'/data/local/testing/{tool}',
                 '/data/local/testing/',
                 group)
    # pull pid list from device
    exec_command(f'adb -s {device}',
                 'pull',
                 f'/data/local/testing/{filename}.csv',
                 f'./resources/data/{pull_path}',
                 print_output=True)
    return pd.read_csv(f'resources/data/{pull_path}/{filename}.csv', sep=',', header=None).values


def adb_collect_page_data(device, pid_list):
    """Collect information about memory pages

    :param device: target device
    :param pid_list: list of processes to be examined
    """
    page_data = OrderedDict()
    swapped_data = OrderedDict()
    present_data = OrderedDict()
    error_pids = []
    for pid in pid_list:
        try:
            filename = str(pid) + '_page_data'
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
        except Exception:
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
    :ivar device: serial number of connected android device
    :ivar page_data: page by page data about processes, indexed with pid
    :ivar present_page_data: data about processes' pages in memory (each process indexed with pid)
    :ivar present_page_data: data about processes' present pages in memory (each process  indexed with pid)
    :ivar swapped_page_data: data about processes' swapped pages in memory (each process  indexed with pid)
    :ivar error_pids: list of pids, for which data couldn't be collected
    :ivar all_pid_list: list of all processes's pids running on connected device
    :ivar cgroups_list: list connected device's available cgroups
    :ivar cgroup_pid_list: list of processes's pids  in chosen cgroup, running on connected device
    :ivar iterations: number of iterations of data collecting
    """
    def __init__(self):
        self.device = None
        self.page_data = {}
        self.present_page_data = {}
        self.swapped_page_data = {}
        self.error_pids = []
        self.all_pid_list = []
        self.cgroup_pid_list = []
        self.cgroups_list = []
        self.iterations = None

    def get_all_pid_list(self):
        """Returns list of all pids from device
        """
        return self.all_pid_list

    def get_cgroup_pid_list(self):
        """Returns list of all pids from cgroup
        """
        return self.cgroup_pid_list

    def get_cgroups_list(self):
        """Returns list of all cgroups
        """
        return self.cgroups_list

    def get_page_data(self, iteration=None, present=False, swapped=False):
        """Returns pages information

        :param iteration: number of collecting iteration
        :param present: True if present data is required, False if not
        :param swapped: True if swapped data is required, False if not
        """
        if not present and not swapped:
            return self.page_data if iteration is None else self.page_data.get(iteration)
        elif present:
            return self.present_page_data if iteration is None else self.present_page_data.get(iteration)
        else:
            return self.swapped_page_data if iteration is None else self.swapped_page_data.get(iteration)

    def get_iterations(self):
        """Returns total amount of iterations
        """
        return self.iterations

    def set_device(self, device):
        """Sets working device to get data

        :param device: device serial number
        """
        self.device = device

    def clear(self):
        """Removes collected data
        """
        self.cgroup_pid_list = []
        self.all_pid_list = []
        self.cgroups_list = []
        self.error_pids = []

    def set_iterations(self, iterations):
        """Sets total amount of iterations and initializes page_data structures

        :param iterations: amount to be set
        """
        self.iterations = iterations
        for i in range(self.iterations):
            self.page_data.setdefault(i, OrderedDict())
            self.present_page_data.setdefault(i, OrderedDict())
            self.swapped_page_data.setdefault(i, OrderedDict())

    def adb_collect_cgroups_list(self):
        """Collects list of available cgroups from a device
        """
        self.cgroups_list = adb_cgroups_list(self.device)

    def adb_collect_all_pid_list(self):
        """Collects list of all processes running on a device
        """
        try:
            self.all_pid_list = adb_collect_pid_list(self.device,
                                                     tool='get_pid_list',
                                                     filename='pid_list',
                                                     pull_path='pids_data',
                                                     group='')
        except Exception:
            self.all_pid_list = []
            raise

    def adb_collect_cgroup_pid_list(self, group=''):
        """Collects list of all processes in a given cgroup running on a device

        :param group: cgroup name
        """
        try:
            self.cgroup_pid_list = adb_collect_pid_list(self.device,
                                                        tool='read_cgroup',
                                                        filename='group_list',
                                                        pull_path='pids_data',
                                                        group=group)
        except Exception:
            self.cgroup_pid_list = []
            raise

    def adb_collect_page_data(self, cur_iteration, pid_list):
        """Collects information about memory pages

        :param cur_iteration: current iteration of collecting
        :param pid_list: list of pids to collect data from
        """
        page_data, present_data, swapped_data, error_pids = adb_collect_page_data(self.device, pid_list)
        self.page_data[cur_iteration] = page_data
        self.present_page_data[cur_iteration] = present_data
        self.swapped_page_data[cur_iteration] = swapped_data
        return error_pids
