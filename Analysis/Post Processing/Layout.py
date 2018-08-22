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
        MainWindow.resize(771, 448)
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
        self.textBrowser.setGeometry(QtCore.QRect(450, 40, 301, 351))
        self.textBrowser.setObjectName("textBrowser")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(40, 40, 381, 241))
        self.widget.setObjectName("widget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 771, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_refresh.setText(_translate("MainWindow", "Refresh"))
        self.btn_parse.setText(_translate("MainWindow", "Parse"))
        self.btn_open.setText(_translate("MainWindow", "Open File"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

