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
import tzlocal
import json
import matplotlib as mpl

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
        self.startTimeInput.setCurrentSection(QtWidgets.QDateTimeEdit.SecondSection)
        self.startTimeInput.dateTimeChanged.connect(self.refresh_time)

        self.endTimeInput = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.endTimeInput.setGeometry(QtCore.QRect(240, 310, 194, 22))
        self.endTimeInput.setObjectName("endTimeInput")
        self.endTimeInput.setCurrentSection(QtWidgets.QDateTimeEdit.SecondSection)
        self.endTimeInput.dateTimeChanged.connect(self.refresh_time)

        self.btn_refresh = QtWidgets.QPushButton(self.centralwidget)
        self.btn_refresh.setGeometry(QtCore.QRect(140, 350, 93, 28))
        self.btn_refresh.setObjectName("btn_refresh")
        self.btn_refresh.clicked.connect(self.refresh)

        self.btn_parse = QtWidgets.QPushButton(self.centralwidget)
        self.btn_parse.setGeometry(QtCore.QRect(240, 350, 93, 28))
        self.btn_parse.setObjectName("btn_parse")
        self.btn_parse.clicked.connect(self.cut_tdms_file)

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
        self.selectGroup.itemClicked.connect(self.update_channel_display)

        self.folderEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.folderEdit.setGeometry(QtCore.QRect(130, 390, 301, 22))
        self.folderEdit.setObjectName("folderEdit")
        self.filenameEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.filenameEdit.setGeometry(QtCore.QRect(130, 420, 301, 22))
        self.filenameEdit.setObjectName("filenameEdit")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(40, 390, 55, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(40, 420, 55, 16))
        self.label_5.setObjectName("label_5")

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
        self.startTimeInput.setDisplayFormat(_translate("MainWindow", "M/d/yyyy h:mm:ss"))
        self.endTimeInput.setDisplayFormat(_translate("MainWindow", "M/d/yyyy h:mm:ss"))
        self.label.setText(_translate("MainWindow", "Select Channel"))
        self.label_2.setText(_translate("MainWindow", "Select Group"))
        self.label_4.setText(_translate("MainWindow", "Folder"))
        self.label_5.setText(_translate("MainWindow", "Filename"))

    def open_tdmsfile(self, filepath= 0):
        if(filepath == 0):
            paths = QtWidgets.QFileDialog.getOpenFileName(MainWindow, 'Open File', 'C:\\Labview Test Data\\2018-08-22\\Sensors')
            filepath = paths[0]
        if(filepath == ''):
            pass
        else:
            self.Logfiletdms = TF(filepath)
            folder = os.path.split(filepath)
            self.datefolder = os.path.split(folder[0])[0]
            eventlogpath = os.path.join(self.datefolder,'eventlog.json')
            with open(eventlogpath) as fp:
                self.jsonfile = json.load(fp)
            
            
            self.groups = self.Logfiletdms.groups()
            self.selectGroup.clear()
            self.selectGroup.insertItems(0,self.groups)
            self.selectGroup.setCurrentRow(0)

            self.update_channel_display() 
            self.refresh()      

    def update_channel_display(self):
        selgroup = self.selectGroup.currentRow()
        channels = self.Logfiletdms.group_channels(self.groups[selgroup])
        channelnamelist = []
        for channel in channels:
            channelnamelist.append(channel.channel)
        self.selectChannel.clear()
        self.selectChannel.insertItems(0,channelnamelist)
        self.selectChannel.setCurrentRow(0)
        channel = channels[0]
        self.update_time_displays(channel)

    def update_time_displays(self,channel):
        self.timearray = channel.time_track(absolute_time = True)
        startdatetime = QtCore.QDateTime()
        startdatetime.setTime_t(np64_to_unix(self.timearray[0]))
        enddatetime = QtCore.QDateTime()
        enddatetime.setTime_t(np64_to_unix(self.timearray[-1]))

        self.startTimeInput.setDateTime(startdatetime)
        self.endTimeInput.setDateTime(enddatetime)

    def refresh_time(self):
        self.time1 = self.startTimeInput.dateTime().toPyDateTime()
        self.time1 = self.time1.replace(tzinfo = None).astimezone(pytz.utc)
        
        self.time2 = self.endTimeInput.dateTime().toPyDateTime()
        self.time2 = self.time2.replace(tzinfo = None).astimezone(pytz.utc)
        self.plotwidget.update_time(self.time1,self.time2)
        self.cut_eventlog()

    def refresh(self):
        selgroup = self.selectGroup.currentRow()
        channels = self.Logfiletdms.group_channels(self.groups[selgroup])
        selchannel = self.selectChannel.currentRow()
        channel = channels[selchannel]

        self.plotwidget.update_data(channel)
        self.refresh_time()
        self.cut_eventlog()
        self.display_eventlog()



    def cut_eventlog(self):
        self.eventlog_cut= []
        for event in self.jsonfile:
            time = datetime.datetime.utcfromtimestamp(event['dt'])
            time = time.replace(tzinfo=pytz.utc)
            if((time>self.time1) and (time<self.time2)):
                self.eventlog_cut.append(event)
        self.display_eventlog()

    def display_eventlog(self):
        string = ''

        for event in self.eventlog_cut:
            time = datetime.datetime.utcfromtimestamp(event['dt'])
            string += time.strftime('%H:%M:%S') + ' - '
            string += json.dumps(event['event'])
            string += '\r\n'

        
        self.textBrowser.setText(string)
        

        self.tci = self.gettestcaseinfo() 

        if(len(self.tci)>0):
            folder = self.tci[-1]['project'] + '\\'+ self.tci[0]['subfolder']
            self.folderEdit.setText(folder)
            filename = self.tci[-1]['filename'] + '_'+ self.tci[0]['measurementnumber']
            self.filenameEdit.setText(filename)
            self.filepath = os.path.join(self.datefolder, folder,filename)
            self.filepath = self.filepath + '.tdms'


    def gettestcaseinfo(self):
        testcaseinfo = {}
        times = []
        for event in self.jsonfile:
            if event['event']['type'] == 'TestCaseInfoChange':
                time = datetime.datetime.utcfromtimestamp(event['dt'])
                time = time.replace(tzinfo=pytz.utc)
                testcaseinfo[time] = event['event']['event info']
                times.append(time)

        self.plotwidget.update_eventticks(times)

        testcaseinfoarray = []
        for time, tci in testcaseinfo.items():
            if(time<self.time1): 
                testcaseinfoarray.append(tci)

        return testcaseinfoarray

    def cut_tdms_file(self):

        timedata = list(map(lambda x: np64_to_utc(x),self.timearray))
        idx1 = nearest_timeind(timedata,self.time1)
        idx2 = nearest_timeind(timedata,self.time2)

        f, ext = os.path.splitext(self.filepath)

        newfile = f + '_cut.tdms' #TODO add original file name to cut file

        direc = os.path.split(f)[0]
        if not os.path.exists(direc):
            os.makedirs(direc)

        root_object = RootObject(properties={ #TODO root properties
        })

        with TdmsWriter(newfile,mode='w') as tdms_writer:
            for group in self.Logfiletdms.groups():
                channels = self.Logfiletdms.group_channels(group)
                for channel in channels:
                    props = channel.properties
                    start= props['wf_start_time']
                    offset = datetime.timedelta(milliseconds = props['wf_increment']*1000*idx1)
                    props['wf_start_time'] = start + offset
                    channel_object = ChannelObject(group, channel.channel, channel.data[idx1:idx2], properties=props)
                    tdms_writer.write_segment([
                        root_object,
                        channel_object])

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent = None, width =5, height = 4, dpi = 100):
        self.fig = mpl.figure.Figure(figsize = (width,height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        
        self.compute_initial_figure()
        
        FigureCanvas.__init__(self,self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)

        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class MyDynamicMplCanvas(MyMplCanvas):
    def __init__(self,*args,**kwargs):
        MyMplCanvas.__init__(self,*args,**kwargs)

    def compute_initial_figure(self):
        self.dataline, = self.axes.plot([], [], 'r')
        self.timeline1 = mpl.lines.Line2D([0],[0])
        self.timeline2 = mpl.lines.Line2D([0],[0])
        self.eventticks = [mpl.lines.Line2D([0],[0])]

    def update_data(self,channel):
        timearray = channel.time_track(absolute_time = True)
        timearray = list(map(lambda x: np64_to_utc(x).replace(tzinfo=pytz.utc).astimezone(tzlocal.get_localzone()),timearray))
        
        data = channel.data

        if self.dataline in self.axes.lines:
            self.axes.lines.remove(self.dataline)

        self.dataline, = self.axes.plot(timearray,data, linestyle = '-', color = 'b')
        self.axes.set_xlim(min(timearray),max(timearray))
        self.axes.set_ylim(min(data),max(data))

        self.draw()

    def update_time(self,time1,time2):
        
        if self.timeline1 in self.axes.lines:
            self.axes.lines.remove(self.timeline1)
        
        if self.timeline2 in self.axes.lines:
            self.axes.lines.remove(self.timeline2)
        
        ##these vertical lines do not need to be in local time for some reason
        self.timeline1 = self.axes.axvline(time1, linestyle = '--', color = 'gray')  
        self.timeline2 = self.axes.axvline(time2, linestyle = '--',  color = 'gray') 
        
        self.draw()

    def update_eventticks(self,times):
        for line in self.eventticks:
            if line in self.axes.lines:
                self.axes.lines.remove(line)
        
        for time in times:
            self.eventticks.append(self.axes.axvline(time, ymin = 0.9, ymax = 1, color = 'red'))
        ##these vertical lines do not need to be in local time for some reason
        
        
        self.draw()

def np64_to_utc(np64_dt):
    utc_dt = datetime.datetime.utcfromtimestamp(np64_to_unix(np64_dt)).replace(tzinfo=pytz.utc)
    return utc_dt

def np64_to_unix(timestamp):
    return (timestamp - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')

def labview_to_unix(timestamps):
    newtimestamps = list(map(lambda x: x -2082844800 ,timestamps))
    return newtimestamps

def nearest_timeind(timearray, pivot):
    diffs =   np.array(list(map(lambda x: abs(x - pivot),timearray))) 
    seconds = np.array(list(map(lambda x: x.total_seconds(),diffs)))
    return seconds.argmin()

def combine_channels(Fileinfo,group,channel):
    combined = np.empty(0)
    for TDMSfile in Fileinfo['TDMSfile']:
        data = TDMSfile.channel_data(group,channel)
        combined = np.append(combined,data)
    return combined




app = QtWidgets.QApplication(sys.argv)

MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

ui.open_tdmsfile('C:\\Labview Test Data\\2018-08-22\\Sensors\\Log_Sensors_DAQ_5.tdms')

sys.exit(app.exec_())
