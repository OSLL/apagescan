from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QAbstractItemView

from custom_signals import CustomSignals
from qt_ui.dataDialog_ui import Ui_DataDialog


class DataDialog(QDialog):
    """DataDialog class: prototype dialog for selecting data
    """
    def __init__(self, data_list, label='', close_on_detach=True, parent=None, header=[False, False]):
        super(DataDialog, self).__init__(parent)

        self.data_list = data_list
        self.row = 0
        self.col = 0
        self.label = label
        self.header = {'horizontal': header[0], 'vertical': header[1]}
        self.signals = CustomSignals()
        self.initUI()
        self.close_on_detach = close_on_detach

    def initUI(self):
        self._ui = Ui_DataDialog()
        self._ui.setupUi(self)
        self._ui.label.setText(self.label)

        self._ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self._ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        if not self.header['horizontal']:
            self._ui.tableWidget.horizontalHeader().hide()
        if not self.header['vertical']:
            self._ui.tableWidget.verticalHeader().hide()
        self._ui.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        self._ui.buttonBox.clicked.connect(self.button_clicked)
        self.set_data(self.data_list)

    def button_clicked(self):
        self.done(0)

    def set_data(self, new_data_list):
        if len(new_data_list) == 0:
            self._ui.tableWidget.clear()
            return

        self.data_list = new_data_list
        self.row = len(self.data_list)
        self.col = len(self.data_list[0])
        self._ui.tableWidget.setColumnCount(self.col)
        self._ui.tableWidget.setRowCount(self.row)

        for i in range(self.row):
            for j in range(self.col):
                item = QTableWidgetItem()
                item.setText(str(self.data_list[i][j]))
                self._ui.tableWidget.setItem(i, j, item)

    @pyqtSlot(list)
    def update(self, new_data_list):
        if len(new_data_list) == 0 and self.close_on_detach:
            self.done(0)
            return
        self.set_data(new_data_list)
