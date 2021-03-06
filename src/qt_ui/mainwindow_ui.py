# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/interface.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1043, 613)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.refreshColorsButton = QtWidgets.QPushButton(self.centralWidget)
        self.refreshColorsButton.setObjectName("refreshColorsButton")
        self.gridLayout.addWidget(self.refreshColorsButton, 0, 0, 1, 1)
        self.highlightButton = QtWidgets.QPushButton(self.centralWidget)
        self.highlightButton.setObjectName("highlightButton")
        self.gridLayout.addWidget(self.highlightButton, 1, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.centralWidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_4.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.presentGroupBox = QtWidgets.QGroupBox(self.frame)
        self.presentGroupBox.setObjectName("presentGroupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.presentGroupBox)
        self.gridLayout_3.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.graphicsPresent = QtWidgets.QWidget(self.presentGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsPresent.sizePolicy().hasHeightForWidth())
        self.graphicsPresent.setSizePolicy(sizePolicy)
        self.graphicsPresent.setObjectName("graphicsPresent")
        self.gridLayout_3.addWidget(self.graphicsPresent, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.presentGroupBox, 0, 0, 2, 2)
        self.groupBox_2 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_2.setMaximumSize(QtCore.QSize(16777215, 250))
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_6.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.graphicsBar = QtWidgets.QWidget(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsBar.sizePolicy().hasHeightForWidth())
        self.graphicsBar.setSizePolicy(sizePolicy)
        self.graphicsBar.setMinimumSize(QtCore.QSize(0, 80))
        self.graphicsBar.setMaximumSize(QtCore.QSize(16777215, 200))
        self.graphicsBar.setObjectName("graphicsBar")
        self.gridLayout_6.addWidget(self.graphicsBar, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_2, 2, 0, 1, 2)
        self.gridLayout.addWidget(self.frame, 0, 1, 5, 2)
        self.buttonsBox = QtWidgets.QGroupBox(self.centralWidget)
        self.buttonsBox.setMaximumSize(QtCore.QSize(150, 16777215))
        self.buttonsBox.setStyleSheet("QGroupBox{padding-top:15px; margin-top:-15px}")
        self.buttonsBox.setTitle("")
        self.buttonsBox.setObjectName("buttonsBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.buttonsBox)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pidsButton = QtWidgets.QPushButton(self.buttonsBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pidsButton.sizePolicy().hasHeightForWidth())
        self.pidsButton.setSizePolicy(sizePolicy)
        self.pidsButton.setObjectName("pidsButton")
        self.gridLayout_2.addWidget(self.pidsButton, 1, 0, 1, 2)
        self.dataButton = QtWidgets.QPushButton(self.buttonsBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataButton.sizePolicy().hasHeightForWidth())
        self.dataButton.setSizePolicy(sizePolicy)
        self.dataButton.setObjectName("dataButton")
        self.gridLayout_2.addWidget(self.dataButton, 2, 0, 1, 2)
        self.playButton = QtWidgets.QPushButton(self.buttonsBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playButton.sizePolicy().hasHeightForWidth())
        self.playButton.setSizePolicy(sizePolicy)
        self.playButton.setObjectName("playButton")
        self.gridLayout_2.addWidget(self.playButton, 3, 0, 1, 2)
        self.prevButton = QtWidgets.QPushButton(self.buttonsBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prevButton.sizePolicy().hasHeightForWidth())
        self.prevButton.setSizePolicy(sizePolicy)
        self.prevButton.setObjectName("prevButton")
        self.gridLayout_2.addWidget(self.prevButton, 4, 0, 1, 1)
        self.nextButton = QtWidgets.QPushButton(self.buttonsBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nextButton.sizePolicy().hasHeightForWidth())
        self.nextButton.setSizePolicy(sizePolicy)
        self.nextButton.setObjectName("nextButton")
        self.gridLayout_2.addWidget(self.nextButton, 4, 1, 1, 1)
        self.devicesButton = QtWidgets.QPushButton(self.buttonsBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.devicesButton.sizePolicy().hasHeightForWidth())
        self.devicesButton.setSizePolicy(sizePolicy)
        self.devicesButton.setObjectName("devicesButton")
        self.gridLayout_2.addWidget(self.devicesButton, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.buttonsBox, 0, 3, 5, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.centralWidget)
        self.tableWidget.setMaximumSize(QtCore.QSize(250, 16777215))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 2, 0, 3, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1043, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuPIDs = QtWidgets.QMenu(self.menuBar)
        self.menuPIDs.setObjectName("menuPIDs")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionShow_CGroup_tree = QtWidgets.QAction(MainWindow)
        self.actionShow_CGroup_tree.setObjectName("actionShow_CGroup_tree")
        self.menuPIDs.addAction(self.actionShow_CGroup_tree)
        self.menuBar.addAction(self.menuPIDs.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.refreshColorsButton.setText(_translate("MainWindow", "Refresh colors"))
        self.highlightButton.setText(_translate("MainWindow", "Highlight"))
        self.presentGroupBox.setTitle(_translate("MainWindow", "Present and swap pages (swap pages are under the black line)"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Pages percentage"))
        self.pidsButton.setText(_translate("MainWindow", "Show pids"))
        self.dataButton.setText(_translate("MainWindow", "Collect Data"))
        self.playButton.setText(_translate("MainWindow", "Play"))
        self.prevButton.setText(_translate("MainWindow", "Prev"))
        self.nextButton.setText(_translate("MainWindow", "Next"))
        self.devicesButton.setText(_translate("MainWindow", "Devices"))
        self.menuPIDs.setTitle(_translate("MainWindow", "&PIDs"))
        self.actionShow_CGroup_tree.setText(_translate("MainWindow", "&Show CGroup tree"))
