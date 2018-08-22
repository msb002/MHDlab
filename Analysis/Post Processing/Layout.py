# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Layout.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(765, 438)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.startTimeInput = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.startTimeInput.setGeometry(QtCore.QRect(40, 310, 194, 22))
        self.startTimeInput.setObjectName("startTimeInput")
        self.endTimeInput = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.endTimeInput.setGeometry(QtCore.QRect(240, 310, 194, 22))
        self.endTimeInput.setObjectName("endTimeInput")
        self.btn_refresh = QtWidgets.QPushButton(self.centralwidget)
        self.btn_refresh.setGeometry(QtCore.QRect(140, 350, 93, 28))
        self.btn_refresh.setObjectName("btn_refresh")
        self.btn_parse = QtWidgets.QPushButton(self.centralwidget)
        self.btn_parse.setGeometry(QtCore.QRect(240, 350, 93, 28))
        self.btn_parse.setObjectName("btn_parse")
        self.btn_open = QtWidgets.QPushButton(self.centralwidget)
        self.btn_open.setGeometry(QtCore.QRect(40, 350, 93, 28))
        self.btn_open.setObjectName("btn_open")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(450, 40, 301, 241))
        self.textBrowser.setObjectName("textBrowser")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(40, 40, 381, 241))
        self.widget.setObjectName("widget")
        self.selectChannel = QtWidgets.QListWidget(self.centralwidget)
        self.selectChannel.setGeometry(QtCore.QRect(600, 320, 151, 51))
        self.selectChannel.setProperty("isWrapping", False)
        self.selectChannel.setResizeMode(QtWidgets.QListView.Fixed)
        self.selectChannel.setViewMode(QtWidgets.QListView.ListMode)
        self.selectChannel.setModelColumn(0)
        self.selectChannel.setWordWrap(False)
        self.selectChannel.setSelectionRectVisible(False)
        self.selectChannel.setObjectName("selectChannel")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(620, 290, 91, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(460, 290, 91, 20))
        self.label_2.setObjectName("label_2")
        self.selectGroup = QtWidgets.QListWidget(self.centralwidget)
        self.selectGroup.setGeometry(QtCore.QRect(450, 320, 141, 51))
        self.selectGroup.setProperty("isWrapping", False)
        self.selectGroup.setResizeMode(QtWidgets.QListView.Fixed)
        self.selectGroup.setViewMode(QtWidgets.QListView.ListMode)
        self.selectGroup.setModelColumn(0)
        self.selectGroup.setWordWrap(False)
        self.selectGroup.setSelectionRectVisible(False)
        self.selectGroup.setObjectName("selectGroup")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 765, 26))
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
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_refresh.setText(_translate("MainWindow", "Refresh"))
        self.btn_parse.setText(_translate("MainWindow", "Parse"))
        self.btn_open.setText(_translate("MainWindow", "Open File"))
        self.selectChannel.setSortingEnabled(False)
        self.label.setText(_translate("MainWindow", "Select Channel"))
        self.label_2.setText(_translate("MainWindow", "Select Group"))
        self.selectGroup.setSortingEnabled(False)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

