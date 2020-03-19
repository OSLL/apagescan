# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/dataDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DataDialog(object):
    def setupUi(self, DataDialog):
        DataDialog.setObjectName("DataDialog")
        DataDialog.resize(500, 400)
        self.gridLayout = QtWidgets.QGridLayout(DataDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(DataDialog)
        self.label.setText("")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.tableWidget = QtWidgets.QTableWidget(DataDialog)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 1, 0, 1, 4)
        self.buttonBox = QtWidgets.QDialogButtonBox(DataDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 4)

        self.retranslateUi(DataDialog)
        self.buttonBox.accepted.connect(DataDialog.accept)
        self.buttonBox.rejected.connect(DataDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DataDialog)

    def retranslateUi(self, DataDialog):
        _translate = QtCore.QCoreApplication.translate
        DataDialog.setWindowTitle(_translate("DataDialog", "Dialog"))
