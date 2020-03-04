from PyQt5.QtCore import QObject, pyqtSignal


class CustomSignals(QObject):
    pids_changed = pyqtSignal(list)
    cgroup_changed = pyqtSignal(list)
    devices_changed = pyqtSignal(list)
    send_data = pyqtSignal(list)
    cgroup_data_request = pyqtSignal(str)
