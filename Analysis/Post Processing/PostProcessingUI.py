# -*- coding: utf-8 -*-
"""
This program pulls data from the logging files to copy the 'control VI' files
"""

from __future__ import unicode_literals
import numpy as np
import time
import pandas as pd
import os
import sys
from nptdms import TdmsFile as TF
from nptdms import TdmsWriter, RootObject, GroupObject, ChannelObject
import datetime
import pytz
import json

#Make sure Python Analysis folder in in PYTHONPATH and import the MHDpy module
PythonAnalysisPath = 'C:\\Users\\aspit\\Git\\MHDLab\\Python Analysis'
if not PythonAnalysisPath in sys.path:
    sys.path.append(PythonAnalysisPath)



import random
import matplotlib as mpl
from PyQt5 import QtCore, QtWidgets, QtGui


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

progname = os.path.basename(sys.argv[0])
progversion = "0.1"

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent = None, width =5, height = 4, dpi = 100):
        fig = mpl.figure.Figure(figsize = (width,height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.compute_initial_figure()
        
        FigureCanvas.__init__(self,fig)
        self.setParent(parent)

        print(FigureCanvas)

        FigureCanvas.setSizePolicy(self,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)

        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class MyDynamicMplCanvas(MyMplCanvas):
    def __init__(self,*args,**kwargs):
        MyMplCanvas.__init__(self,*args,**kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        l = [random.randint(0,10) for i in range(4)]
        self.axes.cla()
        self.axes.plot([0,1,2,3], l)
        self.draw()

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
        self.btn_open.clicked.connect(self.open_file)

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(450, 40, 301, 351))
        self.textBrowser.setObjectName("textBrowser")

        self.widget = MyDynamicMplCanvas(self.centralwidget, width = 5, height = 4, dpi = 100)
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

    def open_file(self):
        name = QtWidgets.QFileDialog.getOpenFileName(MainWindow, 'Open File')
        print(name)


app = QtWidgets.QApplication(sys.argv)

MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()


sys.exit(app.exec_())
