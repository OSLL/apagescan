# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/selectDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SelectDialog(object):
    def setupUi(self, SelectDialog):
        SelectDialog.setObjectName("SelectDialog")
        SelectDialog.resize(500, 400)
        self.gridLayout = QtWidgets.QGridLayout(SelectDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(SelectDialog)
        self.label.setText("")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.tableWidget = QtWidgets.QTableWidget(SelectDialog)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 1, 0, 1, 4)
        self.buttonBox = QtWidgets.QDialogButtonBox(SelectDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 4)
        self.checkBox = QtWidgets.QCheckBox(SelectDialog)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 0, 3, 1, 1)

        self.retranslateUi(SelectDialog)
        self.buttonBox.accepted.connect(SelectDialog.accept)
        self.buttonBox.rejected.connect(SelectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SelectDialog)

    def retranslateUi(self, SelectDialog):
        _translate = QtCore.QCoreApplication.translate
        SelectDialog.setWindowTitle(_translate("SelectDialog", "Dialog"))
        self.checkBox.setText(_translate("SelectDialog", "Select All"))
