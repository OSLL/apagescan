import subprocess

import numpy as np


class DeviceHandler:
    """
    Class to handle Android devices, connected to PC
    :ivar listeners: list of listeners - objects (implementing Listener interface), that are tracking devices' changes
    :ivar serial_numbers: list of all connected devices' serial numbers
    :ivar current_device: serial number of selected connected device
    """
    def __init__(self):
        self.listeners = []
        self.serial_numbers = []
        self.current_device = None

    def device_selected(self):
        """Return True if current device is still selected (selection is being cancelled on disconnect), else False
        """
        return self.current_device in list(np.asarray(self.serial_numbers).flatten())

    def has_devices(self):
        """Returns True if there are connected devices, False if not"""
        return len(self.serial_numbers) != 0

    def get_device(self):
        """Returns current working device
        """
        return self.current_device if self.device_selected() else None

    def switch(self, number):
        """Switches working device to new device

        :param number: number of a new working device
        """
        self.current_device = number
        if not self.device_selected():
            self.current_device = None

    def devices_list(self):
        """Returns all connected devices
        """
        return self.serial_numbers

    def add_listener(self, listener):
        """Adds new listener

        :param listener: listener to be added
        """
        self.listeners.append(listener)

    def update(self):
        """Updates list of all connected devices and notifies listeners
        """
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
