from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView

from dataDialog_view import DataDialog
from qt_ui.selectDialog_ui import Ui_SelectDialog


class SelectDialog(DataDialog):
    def initUI(self):
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
        self.set_data(self.data_list)

    def get_checked(self):
        checked_data = []
        try:
            for i in range(self.row):
                if self._ui.tableWidget.item(i, 0).checkState() == Qt.Checked:
                    checked_data.append([self.data_list[i][j] for j in range(len(self.data_list[i]))])
        except AttributeError:
            pass
        return checked_data

    def button_clicked(self):
        self.signals.send_data.emit(self.get_checked())

    def select_all_button_clicked(self):
        if self._ui.checkBox.checkState() == Qt.Checked:
            for i in range(self.row):
                self._ui.tableWidget.item(i, 0).setCheckState(Qt.Checked)
        else:
            for i in range(self.row):
                self._ui.tableWidget.item(i, 0).setCheckState(Qt.Unchecked)

    def set_data(self, new_data_list):
        if len(new_data_list) == 0:
            self._ui.tableWidget.clear()
            return
        old_checked = self.get_checked()

        self.data_list = new_data_list
        self.row = len(self.data_list)
        self.col = len(self.data_list[0])
        self._ui.tableWidget.setColumnCount(self.col)
        self._ui.tableWidget.setRowCount(self.row)

        for i in range(self.row):
            for j in range(self.col):
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

    def hide_select_all_push_button(self):
        self._ui.checkBox.hide()
