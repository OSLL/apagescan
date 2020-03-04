from PyQt5.QtWidgets import QAbstractItemView, QTableWidget

from custom_signals import CustomSignals
from selectDialog_view import SelectDialog
from qt_models.pidTreeModel import PidTreeModel
from qt_ui.treeDialog_ui import Ui_TreeDialog


class TreeDialog(SelectDialog):

    def __init__(self, cgroup_list):
        self.cgroup_list = cgroup_list
        self._ui = None
        self.model = None
        self.signals = CustomSignals
        super(TreeDialog, self).__init__(cgroup_list)

    def initUI(self):
        self._ui = Ui_TreeDialog()
        self._ui.setupUi(self)

        self.model = PidTreeModel()

        for group in self.cgroup_list:
            self._ui.groups.addItem(group)

        self._ui.treeView.setModel(self.model)
        self._ui.treeView.expandAll()
        self._ui.lineEdit.setText('Choose cgroup')

        self._ui.label.setText('Select PIDs')
        self._ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self._ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        self._ui.tableWidget.horizontalHeader().hide()
        self._ui.tableWidget.verticalHeader().hide()
        self._ui.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        self._ui.showButton.clicked.connect(self.show_button_clicked)
        self._ui.buttonBox.clicked.connect(self.button_clicked)
        self._ui.checkBox.setEnabled(False)
        self._ui.checkBox.clicked.connect(self.select_all_button_clicked)

    def display_data(self, cgroup_data=[]):
        self.model.setData(cgroup_data)
        self._ui.treeView.expandAll()
        super().set_data(self.model.tasks)

    def show_button_clicked(self):
        group = self.cgroup_list[self._ui.groups.currentIndex()]
        self._ui.lineEdit.setText('Path: ' + group)
        self._ui.checkBox.setEnabled(True)
        self.signals.cgroup_data_request.emit(group)

    # new_data_list is list of [pid, ppid, name_of_pid]
    def set_data(self, new_data_list):
        prev_group_list, self.cgroup_list = self.cgroup_list, new_data_list

        if prev_group_list != self.cgroup_list:
            self._ui.groups.clear()
            for group in self.groups:
                self._ui.groups.addItem(group)

