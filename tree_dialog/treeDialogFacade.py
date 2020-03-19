from subprocess import CalledProcessError

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QMessageBox
from pandas.errors import EmptyDataError


class TreeDialogFacade(QObject):
    """Facade class to handle transfer data between device and treeDialog instance
    """
    def __init__(self, device_interaction, tree_dialog):
        super().__init__()
        self.dialog = tree_dialog
        self.data_collector = device_interaction

    @pyqtSlot(str)
    def transfer_data(self, group_name=''):
        try:
            self.data_collector.collect_pid_list_cgroup(group_name)
        except CalledProcessError:
            QMessageBox.about(self, 'Error', 'Check connection with device and tool presence')
        except EmptyDataError:
            QMessageBox.about(self, 'Error', 'Pid list unavailable')

        self.dialog.display_data(self.data_collector.get_pid_list_cgroup())
