# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tableDialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TableDialog(object):
    def setupUi(self, TableDialog):
        TableDialog.setObjectName("TableDialog")
        TableDialog.resize(500, 400)
        self.gridLayout = QtWidgets.QGridLayout(TableDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.pidLabel = QtWidgets.QLabel(TableDialog)
        self.pidLabel.setObjectName("pidLabel")
        self.gridLayout.addWidget(self.pidLabel, 0, 0, 1, 1)
        self.pidLineEdit = QtWidgets.QLineEdit(TableDialog)
        self.pidLineEdit.setReadOnly(True)
        self.pidLineEdit.setObjectName("pidLineEdit")
        self.gridLayout.addWidget(self.pidLineEdit, 0, 1, 1, 1)
        self.pidTableView = QtWidgets.QTableView(TableDialog)
        self.pidTableView.setObjectName("pidTableView")
        self.gridLayout.addWidget(self.pidTableView, 1, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(TableDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)
        self.retranslateUi(TableDialog)
        self.buttonBox.accepted.connect(TableDialog.accept)
        self.buttonBox.rejected.connect(TableDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TableDialog)

    def retranslateUi(self, TableDialog):
        _translate = QtCore.QCoreApplication.translate
        TableDialog.setWindowTitle(_translate("TableDialog", "Table Dialog"))
        self.pidLabel.setText(_translate("TableDialog", "PID"))
