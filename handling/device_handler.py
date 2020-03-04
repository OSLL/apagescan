import subprocess

import numpy as np


class DeviceHandler:
    def __init__(self):
        self.listeners = []
        self.serial_numbers = []
        self.current_device = None

    def device_selected(self):
        return self.current_device in list(np.asarray(self.serial_numbers).flatten())

    def has_devices(self):
        return len(self.serial_numbers) != 0

    def get_device(self):
        return self.current_device if self.device_selected() else None

    def switch(self, number):
        self.current_device = number
        if not self.device_selected():
            self.current_device = None

    def devices_list(self):
        return self.serial_numbers

    def add_listener(self, listener):
        self.listeners.append(listener)

    def update(self):
        res = subprocess.check_output(
            "adb devices",
            shell=True)
        prev_amount = len(self.serial_numbers)
        output = list(filter(lambda x: x, res.decode('UTF-8').split('\n')))
        self.serial_numbers = list(map(lambda x: [x[:x.find('\t')]], output[1:]))
        if self.serial_numbers is []:
            self.current_device = None
        if len(self.serial_numbers) != prev_amount:
            [listener.react() for listener in self.listeners]
