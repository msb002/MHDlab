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

        FigureCanvas.setSizePolicy(self,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)

        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class MyDynamicMplCanvas(MyMplCanvas):
    def __init__(self,*args,**kwargs):
        MyMplCanvas.__init__(self,*args,**kwargs)

    def compute_initial_figure(self):
        self.axes.plot([], [], 'r')

    def update_figure(self):
        l = [random.randint(0,10) for i in range(4)]
        self.axes.cla()
        self.axes.plot([0,1,2,3], l)
        self.draw()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(771, 508)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.plotwidget = MyDynamicMplCanvas(self.centralwidget, width = 5, height = 4, dpi = 100)
        self.plotwidget.setGeometry(QtCore.QRect(40, 40, 381, 241))
        self.plotwidget.setObjectName("widget")

        self.startTimeInput = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.startTimeInput.setGeometry(QtCore.QRect(40, 310, 194, 22))
        self.startTimeInput.setObjectName("startTimeInput")

        self.endTimeInput = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.endTimeInput.setGeometry(QtCore.QRect(240, 310, 194, 22))
        self.endTimeInput.setObjectName("endTimeInput")

        self.btn_refresh = QtWidgets.QPushButton(self.centralwidget)
        self.btn_refresh.setGeometry(QtCore.QRect(140, 350, 93, 28))
        self.btn_refresh.setObjectName("btn_refresh")
        self.btn_refresh.clicked.connect(self.plotwidget.update_figure)

        self.btn_parse = QtWidgets.QPushButton(self.centralwidget)
        self.btn_parse.setGeometry(QtCore.QRect(240, 350, 93, 28))
        self.btn_parse.setObjectName("btn_parse")

        self.btn_open = QtWidgets.QPushButton(self.centralwidget)
        self.btn_open.setGeometry(QtCore.QRect(40, 350, 93, 28))
        self.btn_open.setObjectName("btn_open")
        self.btn_open.clicked.connect(self.open_tdmsfile)

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(450, 40, 301, 250))
        self.textBrowser.setObjectName("textBrowser")

        self.selectChannel = QtWidgets.QListWidget(self.centralwidget)
        self.selectChannel.setGeometry(QtCore.QRect(600, 320, 151, 151))
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
        self.selectGroup.setGeometry(QtCore.QRect(450, 320, 141, 151))
        self.selectGroup.setProperty("isWrapping", False)
        self.selectGroup.setResizeMode(QtWidgets.QListView.Fixed)
        self.selectGroup.setViewMode(QtWidgets.QListView.ListMode)
        self.selectGroup.setModelColumn(0)
        self.selectGroup.setWordWrap(False)
        self.selectGroup.setSelectionRectVisible(False)
        self.selectGroup.setObjectName("selectGroup")
        self.selectGroup.itemClicked.connect(self.updatechannels)

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
        MainWindow.setWindowTitle(_translate("MainWindow", "MHDLab PostProcessor"))
        self.btn_refresh.setText(_translate("MainWindow", "Refresh"))
        self.btn_parse.setText(_translate("MainWindow", "Parse"))
        self.btn_open.setText(_translate("MainWindow", "Open File"))

    def open_tdmsfile(self):
        name = QtWidgets.QFileDialog.getOpenFileName(MainWindow, 'Open File', 'C:\\Labview Test Data\\2018-08-16\\Sensors')
        filepath = name[0]
        self.Logfiletdms = TF(filepath)

        folder = os.path.split(filepath)
        datefolder = os.path.split(folder[0])
        eventlogpath = os.path.join(datefolder[0],'eventlog.json')
        with open(eventlogpath) as fp:
            self.jsonfile = json.load(fp)
        text = json.dumps(self.jsonfile)
        self.textBrowser.setText(text)
        
        self.groups = self.Logfiletdms.groups()
        self.selectGroup.clear()
        self.selectGroup.insertItems(0,self.groups)
        self.selectGroup.setCurrentRow(0)

        self.updatechannels()



        #self.selectGroup.set


    def updatechannels(self):
        selgroup = self.selectGroup.currentRow()
        
        channels = self.Logfiletdms.group_channels(self.groups[selgroup])
        channelnamelist = []
        for channel in channels:
            channelnamelist.append(channel.channel)
        self.selectChannel.clear()
        self.selectChannel.insertItems(0,channelnamelist)
        self.selectChannel.setCurrentRow(0)





app = QtWidgets.QApplication(sys.argv)

MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()


sys.exit(app.exec_())
