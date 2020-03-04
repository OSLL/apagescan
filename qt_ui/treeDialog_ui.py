# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/treeDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TreeDialog(object):
    def setupUi(self, TreeDialog):
        TreeDialog.setObjectName("TreeDialog")
        TreeDialog.resize(912, 804)
        self.gridLayout = QtWidgets.QGridLayout(TreeDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.groups = QtWidgets.QComboBox(TreeDialog)
        self.groups.setObjectName("groups")
        self.gridLayout.addWidget(self.groups, 0, 0, 1, 1)
        self.showButton = QtWidgets.QPushButton(TreeDialog)
        self.showButton.setObjectName("showButton")
        self.gridLayout.addWidget(self.showButton, 0, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(TreeDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(TreeDialog)
        self.label.setText("")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 3, 1, 1)
        self.treeView = QtWidgets.QTreeView(TreeDialog)
        self.treeView.setObjectName("treeView")
        self.gridLayout.addWidget(self.treeView, 1, 0, 1, 3)
        self.tableWidget = QtWidgets.QTableWidget(TreeDialog)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 1, 3, 1, 3)
        self.buttonBox = QtWidgets.QDialogButtonBox(TreeDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 6)
        self.checkBox = QtWidgets.QCheckBox(TreeDialog)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 0, 5, 1, 1)

        self.retranslateUi(TreeDialog)
        self.buttonBox.accepted.connect(TreeDialog.accept)
        self.buttonBox.rejected.connect(TreeDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TreeDialog)

    def retranslateUi(self, TreeDialog):
        _translate = QtCore.QCoreApplication.translate
        TreeDialog.setWindowTitle(_translate("TreeDialog", "Dialog"))
        self.showButton.setText(_translate("TreeDialog", "Show"))
        self.checkBox.setText(_translate("TreeDialog", "Select all"))
