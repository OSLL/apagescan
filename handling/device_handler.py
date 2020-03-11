import numpy as np
import re

from utilities import exec_command


class DeviceHandler:
    def __init__(self):
        self.listeners = []
        self.serial_numbers = []
        self.current_device_number = None

    def is_device_selected(self):
        return self.current_device_number in list(np.asarray(self.serial_numbers).flatten())

    def has_devices(self):
        return len(self.serial_numbers) != 0

    def get_device(self):
        return self.current_device_number

    def switch(self, device_number):
        self.current_device_number = device_number
        if not self.is_device_selected():
            self.current_device_number = None

    def devices_list(self):
        return self.serial_numbers

    def add_listener(self, listener):
        self.listeners.append(listener)

    def update(self):
        res = exec_command('adb devices')
        prev_state = self.serial_numbers
        output = [x for x in res.decode('UTF-8').split('\n') if x]
        number_pattern = re.compile(r'(.*)\t')
        self.serial_numbers = list(map(lambda x: number_pattern.findall(x), output[1:]))

        if len(self.serial_numbers) == 0:
            self.current_device_number = None

        if sorted(self.serial_numbers) != sorted(prev_state):
            for listener in self.listeners:
                listener.react()
