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
        MainWindow.resize(887, 663)
        MainWindow.setStatusTip("")
        MainWindow.setAccessibleName("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.startTimeInput = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.startTimeInput.setGeometry(QtCore.QRect(80, 4, 194, 22))
        self.startTimeInput.setCurrentSection(QtWidgets.QDateTimeEdit.MonthSection)
        self.startTimeInput.setObjectName("startTimeInput")
        self.endTimeInput = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.endTimeInput.setGeometry(QtCore.QRect(360, 4, 194, 22))
        self.endTimeInput.setCurrentSection(QtWidgets.QDateTimeEdit.MonthSection)
        self.endTimeInput.setCurrentSectionIndex(0)
        self.endTimeInput.setTimeSpec(QtCore.Qt.TimeZone)
        self.endTimeInput.setObjectName("endTimeInput")
        self.btn_refresh = QtWidgets.QPushButton(self.centralwidget)
        self.btn_refresh.setGeometry(QtCore.QRect(0, 190, 81, 28))
        self.btn_refresh.setObjectName("btn_refresh")
        self.text_events = QtWidgets.QTextBrowser(self.centralwidget)
        self.text_events.setGeometry(QtCore.QRect(580, 230, 291, 221))
        self.text_events.setObjectName("text_events")
        self.selectChannel = QtWidgets.QListWidget(self.centralwidget)
        self.selectChannel.setGeometry(QtCore.QRect(730, 40, 141, 151))
        self.selectChannel.setProperty("isWrapping", False)
        self.selectChannel.setResizeMode(QtWidgets.QListView.Fixed)
        self.selectChannel.setViewMode(QtWidgets.QListView.ListMode)
        self.selectChannel.setModelColumn(0)
        self.selectChannel.setWordWrap(False)
        self.selectChannel.setSelectionRectVisible(False)
        self.selectChannel.setObjectName("selectChannel")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(750, 10, 91, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(600, 10, 91, 20))
        self.label_2.setObjectName("label_2")
        self.selectGroup = QtWidgets.QListWidget(self.centralwidget)
        self.selectGroup.setGeometry(QtCore.QRect(580, 40, 131, 151))
        self.selectGroup.setProperty("isWrapping", False)
        self.selectGroup.setResizeMode(QtWidgets.QListView.Fixed)
        self.selectGroup.setViewMode(QtWidgets.QListView.ListMode)
        self.selectGroup.setModelColumn(0)
        self.selectGroup.setWordWrap(False)
        self.selectGroup.setSelectionRectVisible(False)
        self.selectGroup.setObjectName("selectGroup")
        self.folderEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.folderEdit.setGeometry(QtCore.QRect(60, 480, 301, 22))
        self.folderEdit.setObjectName("folderEdit")
        self.filenameEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.filenameEdit.setGeometry(QtCore.QRect(440, 480, 291, 22))
        self.filenameEdit.setObjectName("filenameEdit")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 480, 55, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(380, 480, 55, 16))
        self.label_5.setObjectName("label_5")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(580, 200, 291, 20))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.btn_zoomsel = QtWidgets.QPushButton(self.centralwidget)
        self.btn_zoomsel.setGeometry(QtCore.QRect(0, 70, 81, 28))
        self.btn_zoomsel.setObjectName("btn_zoomsel")
        self.btn_zoomout = QtWidgets.QPushButton(self.centralwidget)
        self.btn_zoomout.setGeometry(QtCore.QRect(0, 110, 81, 28))
        self.btn_zoomout.setObjectName("btn_zoomout")
        self.btn_fitall = QtWidgets.QPushButton(self.centralwidget)
        self.btn_fitall.setGeometry(QtCore.QRect(0, 150, 81, 28))
        self.btn_fitall.setObjectName("btn_fitall")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(740, 473, 151, 31))
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(41, 411, 31, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(135, 411, 40, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(324, 411, 31, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(230, 411, 41, 16))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(418, 411, 20, 16))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(513, 411, 23, 16))
        self.label_12.setObjectName("label_12")
        self.combo_function = QtWidgets.QComboBox(self.centralwidget)
        self.combo_function.setGeometry(QtCore.QRect(20, 580, 181, 22))
        self.combo_function.setObjectName("combo_function")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(80, 560, 61, 16))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(600, 560, 55, 16))
        self.label_14.setObjectName("label_14")
        self.combo_files = QtWidgets.QComboBox(self.centralwidget)
        self.combo_files.setGeometry(QtCore.QRect(600, 580, 181, 22))
        self.combo_files.setObjectName("combo_files")
        self.combo_files.addItem("")
        self.combo_files.addItem("")
        self.btn_parse = QtWidgets.QPushButton(self.centralwidget)
        self.btn_parse.setGeometry(QtCore.QRect(789, 572, 91, 31))
        self.btn_parse.setObjectName("btn_parse")
        self.combo_times = QtWidgets.QComboBox(self.centralwidget)
        self.combo_times.setGeometry(QtCore.QRect(600, 530, 181, 22))
        self.combo_times.setObjectName("combo_times")
        self.combo_times.addItem("")
        self.combo_times.addItem("")
        self.combo_times.addItem("")
        self.combo_times.addItem("")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(600, 510, 91, 16))
        self.label_15.setObjectName("label_15")
        self.mplframe = QtWidgets.QFrame(self.centralwidget)
        self.mplframe.setGeometry(QtCore.QRect(90, 40, 471, 361))
        self.mplframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mplframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mplframe.setObjectName("mplframe")
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(10, 6, 71, 16))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(285, 6, 71, 16))
        self.label_17.setObjectName("label_17")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(-20, 460, 921, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(40, 510, 151, 16))
        self.label_18.setObjectName("label_18")
        self.combo_module = QtWidgets.QComboBox(self.centralwidget)
        self.combo_module.setGeometry(QtCore.QRect(20, 530, 181, 22))
        self.combo_module.setObjectName("combo_module")
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        self.label_19.setGeometry(QtCore.QRect(310, 506, 231, 20))
        self.label_19.setObjectName("label_19")
        self.text_docstring = QtWidgets.QTextBrowser(self.centralwidget)
        self.text_docstring.setGeometry(QtCore.QRect(220, 530, 371, 81))
        self.text_docstring.setObjectName("text_docstring")
        self.btn_cutinternalinloc = QtWidgets.QPushButton(self.centralwidget)
        self.btn_cutinternalinloc.setGeometry(QtCore.QRect(790, 520, 91, 41))
        self.btn_cutinternalinloc.setObjectName("btn_cutinternalinloc")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 430, 561, 24))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.t_mean = QtWidgets.QLineEdit(self.widget)
        self.t_mean.setText("")
        self.t_mean.setObjectName("t_mean")
        self.horizontalLayout.addWidget(self.t_mean)
        self.t_std = QtWidgets.QLineEdit(self.widget)
        self.t_std.setText("")
        self.t_std.setObjectName("t_std")
        self.horizontalLayout.addWidget(self.t_std)
        self.t_med = QtWidgets.QLineEdit(self.widget)
        self.t_med.setText("")
        self.t_med.setObjectName("t_med")
        self.horizontalLayout.addWidget(self.t_med)
        self.t_skew = QtWidgets.QLineEdit(self.widget)
        self.t_skew.setText("")
        self.t_skew.setObjectName("t_skew")
        self.horizontalLayout.addWidget(self.t_skew)
        self.t_min = QtWidgets.QLineEdit(self.widget)
        self.t_min.setText("")
        self.t_min.setObjectName("t_min")
        self.horizontalLayout.addWidget(self.t_min)
        self.t_max = QtWidgets.QLineEdit(self.widget)
        self.t_max.setText("")
        self.t_max.setObjectName("t_max")
        self.horizontalLayout.addWidget(self.t_max)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 887, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionReload_ppr = QtWidgets.QAction(MainWindow)
        self.actionReload_ppr.setObjectName("actionReload_ppr")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionReload_ppr)
        self.menubar.addAction(self.menuFile.menuAction())

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
        self.label_6.setText(_translate("MainWindow", "File information from event before 1st cuttime."))
        self.label_7.setText(_translate("MainWindow", "Mean"))
        self.label_8.setText(_translate("MainWindow", "StdDev"))
        self.label_9.setText(_translate("MainWindow", "Skew"))
        self.label_10.setText(_translate("MainWindow", "Median"))
        self.label_11.setText(_translate("MainWindow", "Min"))
        self.label_12.setText(_translate("MainWindow", "Max"))
        self.label_13.setText(_translate("MainWindow", "Function"))
        self.label_14.setText(_translate("MainWindow", "File(s)"))
        self.combo_files.setItemText(0, _translate("MainWindow", "Internal"))
        self.combo_files.setItemText(1, _translate("MainWindow", "Dialog"))
        self.btn_parse.setText(_translate("MainWindow", "Process!"))
        self.combo_times.setItemText(0, _translate("MainWindow", "Eventlog in Time Window"))
        self.combo_times.setItemText(1, _translate("MainWindow", "Markers"))
        self.combo_times.setItemText(2, _translate("MainWindow", "Entire Eventlog"))
        self.combo_times.setItemText(3, _translate("MainWindow", "PIMAX1 Savetimes"))
        self.label_15.setText(_translate("MainWindow", "Cutting Times"))
        self.label_16.setText(_translate("MainWindow", "Cut Time 1:"))
        self.label_17.setText(_translate("MainWindow", "Cut Time 2:"))
        self.label_18.setText(_translate("MainWindow", "Post Processing Module"))
        self.label_19.setText(_translate("MainWindow", "Post Processing Function Docstring"))
        self.btn_cutinternalinloc.setText(_translate("MainWindow", "Cut Internal \n"
" in location"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionReload_ppr.setText(_translate("MainWindow", "Reload PPR"))

