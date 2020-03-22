from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QDialog

from src.custom_signals import CustomSignals
from src.qt_ui.dynamics_dialog_ui import Ui_DynamicsDialog


class DynamicsDialog(QDialog):
    """Widget provides input of two values: total_time - limit of time that all data collection would take,
    and iteration_time - time to wait between iterations of data collection
    """
    def __init__(self):
        super(DynamicsDialog, self).__init__()
        self._ui = Ui_DynamicsDialog()
        self._ui.setupUi(self)

        self._ui.buttonBox.setEnabled(False)
        self.signals = CustomSignals()
        self._ui.buttonBox.clicked.connect(self.button_clicked)

        # Double value regular expression for validator
        self.regexp = QtCore.QRegExp('\\d*[\\.]?\\d+')
        self.validator = QtGui.QRegExpValidator(self.regexp)

        self._ui.iterationTimeEdit.setValidator(self.validator)
        self._ui.totalTimeEdit.setValidator(self.validator)

        self._ui.iterationTimeEdit.textChanged.connect(self.check_state)
        self._ui.iterationTimeEdit.textChanged.emit(self._ui.iterationTimeEdit.text())

        self._ui.totalTimeEdit.textChanged.connect(self.check_state)
        self._ui.totalTimeEdit.textChanged.emit(self._ui.totalTimeEdit.text())

    def get_values(self):
        iteration_time = float(self._ui.iterationTimeEdit.text())
        total_time = float(self._ui.totalTimeEdit.text())
        if iteration_time <= total_time:
            return iteration_time, total_time
        else:
            return None

    def button_clicked(self):
        self.signals.send_data.emit(self.get_values())

    def check_state(self):
        iteration_state = self.validator.validate(self._ui.iterationTimeEdit.text(), 0)[0]
        total_state = self.validator.validate(self._ui.totalTimeEdit.text(), 0)[0]
        if iteration_state == QtGui.QValidator.Acceptable and total_state == QtGui.QValidator.Acceptable:
            self._ui.buttonBox.setEnabled(True)
        else:
            self._ui.buttonBox.setEnabled(False)

    def closeEvent(self, event):
        self.signals.send_data.emit(None)
        event.accept()

    def reject(self):
        self.close()

