# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layout.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(775, 565)
        MainWindow.setStatusTip("")
        MainWindow.setAccessibleName("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.startTimeInput = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.startTimeInput.setGeometry(QtCore.QRect(30, 350, 194, 22))
        self.startTimeInput.setCurrentSection(QtWidgets.QDateTimeEdit.MonthSection)
        self.startTimeInput.setObjectName("startTimeInput")
        self.endTimeInput = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.endTimeInput.setGeometry(QtCore.QRect(230, 350, 194, 22))
        self.endTimeInput.setCurrentSection(QtWidgets.QDateTimeEdit.MonthSection)
        self.endTimeInput.setCurrentSectionIndex(0)
        self.endTimeInput.setTimeSpec(QtCore.Qt.TimeZone)
        self.endTimeInput.setObjectName("endTimeInput")
        self.btn_refresh = QtWidgets.QPushButton(self.centralwidget)
        self.btn_refresh.setGeometry(QtCore.QRect(372, 310, 81, 28))
        self.btn_refresh.setObjectName("btn_refresh")
        self.btn_parse = QtWidgets.QPushButton(self.centralwidget)
        self.btn_parse.setGeometry(QtCore.QRect(350, 470, 93, 28))
        self.btn_parse.setObjectName("btn_parse")
        self.btn_open = QtWidgets.QPushButton(self.centralwidget)
        self.btn_open.setGeometry(QtCore.QRect(10, 310, 91, 28))
        self.btn_open.setObjectName("btn_open")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(450, 40, 301, 241))
        self.textBrowser.setObjectName("textBrowser")
        self.selectChannel = QtWidgets.QListWidget(self.centralwidget)
        self.selectChannel.setGeometry(QtCore.QRect(600, 340, 151, 171))
        self.selectChannel.setProperty("isWrapping", False)
        self.selectChannel.setResizeMode(QtWidgets.QListView.Fixed)
        self.selectChannel.setViewMode(QtWidgets.QListView.ListMode)
        self.selectChannel.setModelColumn(0)
        self.selectChannel.setWordWrap(False)
        self.selectChannel.setSelectionRectVisible(False)
        self.selectChannel.setObjectName("selectChannel")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(630, 310, 91, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(480, 310, 91, 20))
        self.label_2.setObjectName("label_2")
        self.selectGroup = QtWidgets.QListWidget(self.centralwidget)
        self.selectGroup.setGeometry(QtCore.QRect(450, 340, 141, 171))
        self.selectGroup.setProperty("isWrapping", False)
        self.selectGroup.setResizeMode(QtWidgets.QListView.Fixed)
        self.selectGroup.setViewMode(QtWidgets.QListView.ListMode)
        self.selectGroup.setModelColumn(0)
        self.selectGroup.setWordWrap(False)
        self.selectGroup.setSelectionRectVisible(False)
        self.selectGroup.setObjectName("selectGroup")
        self.folderEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.folderEdit.setGeometry(QtCore.QRect(120, 460, 211, 22))
        self.folderEdit.setObjectName("folderEdit")
        self.filenameEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.filenameEdit.setGeometry(QtCore.QRect(120, 490, 211, 22))
        self.filenameEdit.setObjectName("filenameEdit")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 460, 55, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 490, 55, 16))
        self.label_5.setObjectName("label_5")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(460, 10, 291, 20))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.btn_zoomsel = QtWidgets.QPushButton(self.centralwidget)
        self.btn_zoomsel.setGeometry(QtCore.QRect(110, 310, 81, 28))
        self.btn_zoomsel.setObjectName("btn_zoomsel")
        self.btn_zoomout = QtWidgets.QPushButton(self.centralwidget)
        self.btn_zoomout.setGeometry(QtCore.QRect(200, 310, 81, 28))
        self.btn_zoomout.setObjectName("btn_zoomout")
        self.btn_fitall = QtWidgets.QPushButton(self.centralwidget)
        self.btn_fitall.setGeometry(QtCore.QRect(290, 310, 71, 28))
        self.btn_fitall.setObjectName("btn_fitall")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(120, 430, 291, 20))
        self.label_6.setObjectName("label_6")
        self.t_mean = QtWidgets.QLineEdit(self.centralwidget)
        self.t_mean.setGeometry(QtCore.QRect(10, 400, 70, 22))
        self.t_mean.setText("")
        self.t_mean.setObjectName("t_mean")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(30, 380, 55, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(100, 380, 55, 16))
        self.label_8.setObjectName("label_8")
        self.t_std = QtWidgets.QLineEdit(self.centralwidget)
        self.t_std.setGeometry(QtCore.QRect(80, 400, 70, 22))
        self.t_std.setText("")
        self.t_std.setObjectName("t_std")
        self.t_skew = QtWidgets.QLineEdit(self.centralwidget)
        self.t_skew.setGeometry(QtCore.QRect(220, 400, 70, 22))
        self.t_skew.setText("")
        self.t_skew.setObjectName("t_skew")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(240, 380, 55, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(170, 380, 55, 16))
        self.label_10.setObjectName("label_10")
        self.t_med = QtWidgets.QLineEdit(self.centralwidget)
        self.t_med.setGeometry(QtCore.QRect(150, 400, 70, 22))
        self.t_med.setText("")
        self.t_med.setObjectName("t_med")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(310, 380, 55, 16))
        self.label_11.setObjectName("label_11")
        self.t_min = QtWidgets.QLineEdit(self.centralwidget)
        self.t_min.setGeometry(QtCore.QRect(290, 400, 70, 22))
        self.t_min.setText("")
        self.t_min.setObjectName("t_min")
        self.t_max = QtWidgets.QLineEdit(self.centralwidget)
        self.t_max.setGeometry(QtCore.QRect(360, 400, 70, 22))
        self.t_max.setText("")
        self.t_max.setObjectName("t_max")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(380, 380, 55, 16))
        self.label_12.setObjectName("label_12")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 775, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.selectChannel.setCurrentRow(-1)
        self.selectGroup.setCurrentRow(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Post Processor"))
        self.startTimeInput.setDisplayFormat(_translate("MainWindow", "M/d/yyyy h:mm:ss AP"))
        self.endTimeInput.setDisplayFormat(_translate("MainWindow", "M/d/yyyy h:mm:ss"))
        self.btn_refresh.setText(_translate("MainWindow", "Refresh"))
        self.btn_parse.setText(_translate("MainWindow", "Parse"))
        self.btn_open.setText(_translate("MainWindow", "Open File"))
        self.selectChannel.setSortingEnabled(False)
        self.label.setText(_translate("MainWindow", "Select Channel"))
        self.label_2.setText(_translate("MainWindow", "Select Group"))
        self.selectGroup.setSortingEnabled(False)
        self.label_4.setText(_translate("MainWindow", "Folder"))
        self.label_5.setText(_translate("MainWindow", "Filename"))
        self.label_3.setText(_translate("MainWindow", "Events within window"))
        self.btn_zoomsel.setText(_translate("MainWindow", "Zoom Select"))
        self.btn_zoomout.setText(_translate("MainWindow", "Zoom out"))
        self.btn_fitall.setText(_translate("MainWindow", "Fit all"))
        self.label_6.setText(_translate("MainWindow", "File information from event before 1st marker"))
        self.label_7.setText(_translate("MainWindow", "Mean"))
        self.label_8.setText(_translate("MainWindow", "StdDev"))
        self.label_9.setText(_translate("MainWindow", "Skew"))
        self.label_10.setText(_translate("MainWindow", "Median"))
        self.label_11.setText(_translate("MainWindow", "Min"))
        self.label_12.setText(_translate("MainWindow", "Max"))

