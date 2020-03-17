import re
from itertools import chain

from utilities import exec_command


class DeviceHandler:
    """
    Class to handle Android devices, connected to PC
    :ivar listeners: list of listeners - objects (implementing Listener interface), that are tracking devices' changes
    :ivar serial_numbers: list of all connected devices' serial numbers
    :ivar current_device_id: serial number of selected connected device
    """
    def __init__(self):
        self.listeners = []
        self.serial_numbers = []
        self.current_device_id = None

    def is_device_selected(self):
        """Return True if current device is still selected (selection is being cancelled on disconnect), else False
        """
        return self.current_device_id in list(chain.from_iterable(self.serial_numbers))

    def has_devices(self):
        """Returns True if there are connected devices, False if not"""
        return len(self.serial_numbers) != 0

    def get_device(self):
        """Returns current working device
        """
        return self.current_device_id

    def switch(self, device_number):
        """Switches working device to new device

        :param device_number: number of a new working device
        """
        self.current_device_id = device_number
        if not self.is_device_selected():
            self.current_device_id = None

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
        res = exec_command('adb devices')
        prev_state = self.serial_numbers
        output = [x for x in res.decode('UTF-8').split('\n') if x]
        number_pattern = re.compile(r'(.*)\t')
        self.serial_numbers = list(map(lambda x: number_pattern.findall(x), output[1:]))

        if len(self.serial_numbers) == 0:
            self.current_device_id = None

        if sorted(self.serial_numbers) != sorted(prev_state):
            for listener in self.listeners:
                listener.react()
