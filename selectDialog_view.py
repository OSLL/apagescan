from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QAbstractItemView

from custom_signals import CustomSignals
from qt_ui.selectDialog_ui import Ui_SelectDialog


class SelectDialog(QDialog):
    def __init__(self, data_list, label='', close_on_detach=True, has_select_all=False, parent=None):
        super(SelectDialog, self).__init__(parent)

        self.data_list = data_list
        self.rows = 0
        self.cols = 0
        self.label = label
        self.signals = CustomSignals()
        self.close_on_detach = close_on_detach

        self.initUI(label, has_select_all)

    def initUI(self, label, has_select_all):
        self._ui = Ui_SelectDialog()
        self._ui.setupUi(self)
        self._ui.label.setText(self.label)

        self._ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self._ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        self._ui.tableWidget.horizontalHeader().hide()
        self._ui.tableWidget.verticalHeader().hide()
        self._ui.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        self._ui.buttonBox.clicked.connect(self.button_clicked)
        self._ui.checkBox.clicked.connect(self.select_all_button_clicked)

        if not has_select_all:
            self._ui.checkBox.hide()

        self.set_data(self.data_list)

    def get_checked(self):
        checked_data = []

        for i in range(self.rows):
            if self._ui.tableWidget.item(i, 0).checkState() == Qt.Checked:
                checked_data.append(list(self.data_list[i]))

        return checked_data

    def button_clicked(self):
        self.signals.send_data.emit(self.get_checked())

    def select_all_button_clicked(self):
        check_all = self._ui.checkBox.checkState() == Qt.Checked
        for i in range(self.rows):
            self._ui.tableWidget.item(i, 0).setCheckState(Qt.Checked if check_all else Qt.Unchecked)

    def set_data(self, new_data_list):
        if len(new_data_list) == 0:
            self._ui.tableWidget.clear()
            return

        old_checked = self.get_checked()

        self.data_list = new_data_list

        self.rows = len(self.data_list)
        self.cols = len(self.data_list[0])

        self._ui.tableWidget.setRowCount(self.rows)
        self._ui.tableWidget.setColumnCount(self.cols)

        for i in range(self.rows):
            for j in range(self.cols):
                item = QTableWidgetItem()
                if j == 0:
                    item.setCheckState(Qt.Checked if list(self.data_list[i]) in old_checked else Qt.Unchecked)
                item.setText(str(self.data_list[i][j]))
                self._ui.tableWidget.setItem(i, j, item)

    @pyqtSlot(list)
    def update(self, new_data_list):
        if len(new_data_list) == 0 and self.close_on_detach:
            self.done(0)
            return

        self.set_data(new_data_list)
