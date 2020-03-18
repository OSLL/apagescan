import re
from itertools import chain

from utilities import exec_command


class DeviceHandler:
    """
    Class to handle Android devices, connected to PC

    :ivar __listeners: list of listeners - objects (implementing Listener interface), that are tracking devices' changes
    :ivar __serial_numbers: list of all connected devices' serial numbers
    :ivar __current_device_id: serial number of selected connected device
    """

    def __init__(self):
        self.__listeners = []
        self.__serial_numbers = []
        self.__current_device_id = None

    def is_device_selected(self):
        """
        Checks if current device is still connected to PC

        :return: True if device is connected, else False
        :rtype: Bool
        """
        return self.__current_device_id in self.__serial_numbers

    def has_devices(self):
        """
        Checks if there are connected to PC devices

        :return: True if there are connected devices, else False
        :rtype: Bool
        """
        return len(self.__serial_numbers) != 0

    @property
    def current_device(self):
        """
        The unique serial number of selected device

        :getter: returns serial number of current selected device
        :type: String
        """
        return self.__current_device_id

    def switch(self, device_number):
        """
        Switches working device to new device

        :param device_number: number of a new working device
        :return: None
        """
        self.__current_device_id = device_number
        if not self.is_device_selected():
            self.__current_device_id = None

    @property
    def devices_list(self):
        """
        List of all connected devices' serial numbers

        :getter: returns list of all connected devices
        :type: List
        """
        return self.__serial_numbers

    def add_listener(self, listener):
        """Adds new listener

        :param listener: listener to be added
        :return: None
        """
        self.__listeners.append(listener)

    def update(self):
        """Updates list of all connected devices and notifies listeners

        :return: None
        """
        res = exec_command('adb devices')
        prev_state = self.__serial_numbers
        output = [x for x in res.decode('UTF-8').split('\n') if x]
        number_pattern = re.compile(r'(.*)\t')
        serial_numbers = list(map(lambda x: number_pattern.findall(x), output[1:]))
        # flatten list
        self.__serial_numbers = list(chain.from_iterable(serial_numbers))

        if len(self.__serial_numbers) == 0:
            self.__current_device_id = None

        if sorted(self.__serial_numbers) != sorted(prev_state):
            for listener in self.__listeners:
                listener.react()
