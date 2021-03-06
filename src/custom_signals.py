from PyQt5.QtCore import QObject, pyqtSignal


class CustomSignals(QObject):
    """CustomSignals class: contains custom signals for interaction between MainView and dialogs
    """
    pids_changed = pyqtSignal(list)
    cgroup_changed = pyqtSignal(list)
    devices_changed = pyqtSignal(list)
    send_data = pyqtSignal(object)
    cgroup_data_request = pyqtSignal(str)
