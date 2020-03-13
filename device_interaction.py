import re
import struct
import subprocess
from collections import OrderedDict
from subprocess import CalledProcessError

import numpy as np
import pandas as pd
from pandas.errors import EmptyDataError


def get_bit(data, shift):
    return (data >> shift) & 1


def exec_command(*args, print_output=False):
    exec_str = ' '.join(args)
    output = subprocess.check_output(exec_str, shell=True)
    if print_output:
        print(output.decode('UTF-8'))
    return output


def read_page_data(pid):
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
    # Read /proc/mounts - file with all mount points
    try:
        raw_data = str(exec_command(f'adb -s {device}', 'shell', 'cat', '/proc/mounts'))
    except CalledProcessError:
        raw_data = ''
    return list(map(lambda x: x + '/tasks', re.findall(r'(\S+) cgroup ', raw_data)))


def adb_collect_pid_list(device, tool, filename, pull_path, group_name):
    # collect pid list on device
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
    def __init__(self):
        self.device = None
        self.page_data = {}
        self.present_page_data = {}
        self.swapped_page_data = {}
        self.error_pids = []
        self.pid_list_all = []
        self.pid_list_cgroup = []
        self.cgroups_list = []
        self.iterations = None

    def get_pid_list_all(self):
        return self.pid_list_all

    def get_pid_list_cgroup(self):
        return self.pid_list_cgroup

    def get_cgroups_list(self):
        return self.cgroups_list

    def get_page_data(self, iteration=None, present=False, swapped=False):
        if not present and not swapped:
            return self.page_data if iteration is None else self.page_data.get(iteration)
        elif present:
            return self.present_page_data if iteration is None else self.present_page_data.get(iteration)
        else:
            return self.swapped_page_data if iteration is None else self.swapped_page_data.get(iteration)

    def get_iterations(self):
        return self.iterations

    def set_device(self, device):
        self.device = device

    def clear(self):
        self.pid_list_cgroup = []
        self.pid_list_all = []
        self.cgroups_list = []
        self.error_pids = []

    def set_iterations(self, iterations):
        self.iterations = iterations

        for i in range(self.iterations):
            self.page_data.setdefault(i, OrderedDict())
            self.present_page_data.setdefault(i, OrderedDict())
            self.swapped_page_data.setdefault(i, OrderedDict())

    def collect_cgroups_list(self):
        self.cgroups_list = adb_cgroups_list(self.device)

    def collect_pid_list_all(self):
        try:
            self.pid_list_all = adb_collect_pid_list(self.device,
                                                     tool='get_pid_list',
                                                     filename='pid_list',
                                                     pull_path='pids_data',
                                                     group_name='')
        except Exception:
            self.pid_list_all = []
            raise

    def collect_pid_list_cgroup(self, group=''):
        try:
            self.pid_list_cgroup = adb_collect_pid_list(self.device,
                                                        tool='read_cgroup',
                                                        filename='group_list',
                                                        pull_path='pids_data',
                                                        group_name=group)
        except Exception:
            self.pid_list_cgroup = []
            raise

    def collect_page_data(self, cur_iteration, pid_list):
        page_data, present_data, swapped_data, error_pids = adb_collect_page_data(self.device, pid_list)
        self.page_data[cur_iteration] = page_data
        self.present_page_data[cur_iteration] = present_data
        self.swapped_page_data[cur_iteration] = swapped_data
        return error_pids
