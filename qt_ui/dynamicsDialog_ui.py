# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dynamicsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DynamicsDialog(object):
    def setupUi(self, DynamicsDialog):
        DynamicsDialog.setObjectName("DynamicsDialog")
        DynamicsDialog.resize(253, 187)
        self.gridLayout = QtWidgets.QGridLayout(DynamicsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.totalTimeEdit = QtWidgets.QLineEdit(DynamicsDialog)
        self.totalTimeEdit.setObjectName("totalTimeEdit")
        self.gridLayout.addWidget(self.totalTimeEdit, 4, 0, 1, 1)
        self.iterationTimeLabel = QtWidgets.QLabel(DynamicsDialog)
        self.iterationTimeLabel.setObjectName("iterationTimeLabel")
        self.gridLayout.addWidget(self.iterationTimeLabel, 3, 0, 1, 1)
        self.totalTimeLabel = QtWidgets.QLabel(DynamicsDialog)
        self.totalTimeLabel.setObjectName("totalTimeLabel")
        self.gridLayout.addWidget(self.totalTimeLabel, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(DynamicsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 1)
        self.iterationTimeEdit = QtWidgets.QLineEdit(DynamicsDialog)
        self.iterationTimeEdit.setReadOnly(False)
        self.iterationTimeEdit.setObjectName("iterationTimeEdit")
        self.gridLayout.addWidget(self.iterationTimeEdit, 2, 0, 1, 1)

        self.retranslateUi(DynamicsDialog)
        self.buttonBox.accepted.connect(DynamicsDialog.accept)
        self.buttonBox.rejected.connect(DynamicsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DynamicsDialog)
        DynamicsDialog.setTabOrder(self.iterationTimeEdit, self.totalTimeEdit)

    def retranslateUi(self, DynamicsDialog):
        _translate = QtCore.QCoreApplication.translate
        DynamicsDialog.setWindowTitle(_translate("DynamicsDialog", "Collect Data Dialog"))
        self.iterationTimeLabel.setText(_translate("DynamicsDialog", "Total measurment time in sec."))
        self.totalTimeLabel.setText(_translate("DynamicsDialog", "Time between measurements in sec."))

