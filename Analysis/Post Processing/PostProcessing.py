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

import layout

#Make sure Python Analysis folder in in PYTHONPATH and import the MHDpy module
PythonAnalysisPath = 'C:\\Users\\bowenm\\Github\\MHDLab\\Python Analysis'
if not PythonAnalysisPath in sys.path:
    sys.path.append(PythonAnalysisPath)



import random
import matplotlib as mpl
from PyQt5 import QtCore, QtWidgets, QtGui


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

progname = os.path.basename(sys.argv[0])
progversion = "0.1"


class Ui_MainWindow(layout.Ui_MainWindow):
    def link_buttons(self):
        self.plotwidget = MyDynamicMplCanvas(self.centralwidget, width = 5, height = 4, dpi = 100)
        self.plotwidget.setGeometry(QtCore.QRect(0, 0, 400, 300))
        self.plotwidget.setObjectName("widget")
        self.startTimeInput.dateTimeChanged.connect(self.refresh_time)
        self.endTimeInput.dateTimeChanged.connect(self.refresh_time)
        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_parse.clicked.connect(self.cut_tdms_file)
        self.btn_open.clicked.connect(self.open_tdmsfile)
        self.selectGroup.itemClicked.connect(self.update_channel_display)

    def open_tdmsfile(self, filepath= 0):
        if(filepath == 0):
            paths = QtWidgets.QFileDialog.getOpenFileName(MainWindow, 'Open File', 'C:\\Labview Test Data\\2018-08-22\\Sensors')
            filepath = paths[0]
        if(filepath == ''):
            pass
        else:
            
            self.origfilename = os.path.splitext(os.path.split(filepath)[1])[0]

            self.Logfiletdms = TF(filepath)
            folder = os.path.split(filepath)
            self.datefolder = os.path.split(folder[0])[0]
            eventlogpath = os.path.join(self.datefolder,'Eventlog.json')
            with open(eventlogpath) as fp:
                self.jsonfile = json.load(fp)
            
            
            self.groups = self.Logfiletdms.groups()
            self.selectGroup.clear()
            self.selectGroup.insertItems(0,self.groups)
            self.selectGroup.setCurrentRow(0)

            self.update_channel_display() 
            self.refresh()      

    def update_channel_display(self):
        #Updates the channel list to display channels in selected group
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
        #updates the time inputs to max and min of channel
        self.timearray = channel.time_track(absolute_time = True)
        startdatetime = QtCore.QDateTime()
        startdatetime.setTime_t(np64_to_unix(self.timearray[0]))
        enddatetime = QtCore.QDateTime()
        enddatetime.setTime_t(np64_to_unix(self.timearray[-1]))

        self.startTimeInput.setDateTime(startdatetime)
        self.endTimeInput.setDateTime(enddatetime)

    def refresh_time(self):
        #pull the time from the inputs and update the gray lines on the display and cut event log
        self.time1 = self.startTimeInput.dateTime().toPyDateTime()
        self.time1 = self.time1.replace(tzinfo = None).astimezone(pytz.utc)
        
        self.time2 = self.endTimeInput.dateTime().toPyDateTime()
        self.time2 = self.time2.replace(tzinfo = None).astimezone(pytz.utc)
        self.plotwidget.update_time(self.time1,self.time2)
        self.cut_eventlog()

    def refresh(self):
        #full refresh of everything
        selgroup = self.selectGroup.currentRow()
        channels = self.Logfiletdms.group_channels(self.groups[selgroup])
        selchannel = self.selectChannel.currentRow()
        channel = channels[selchannel]

        self.plotwidget.update_data(channel)
        self.refresh_time()
        self.cut_eventlog()



    def cut_eventlog(self):
        #create array of events within the time window
        self.eventlog_cut= []
        for event in self.jsonfile:
            time = datetime.datetime.utcfromtimestamp(event['dt'])
            time = time.replace(tzinfo=pytz.utc)
            if((time>self.time1) and (time<self.time2)):
                self.eventlog_cut.append(event)
        self.display_eventlog()

    def display_eventlog(self):
        #refresh the cut eventlog in the text display
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
            filename = self.origfilename + '_' + self.tci[-1]['filename'] + '_'+ self.tci[-1]['measurementnumber']
            self.filenameEdit.setText(filename)
            self.filepath = os.path.join(self.datefolder, folder, filename)
            self.filepath =   self.filepath + '.tdms'


    def gettestcaseinfo(self):
        #pull the testcase info from the json file
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

        x_label  = 'Time'
        y_label = channel.properties['NI_ChannelName'] + ' (' + channel.properties['unit_string'] + ')'

        if self.dataline in self.axes.lines:
            self.axes.lines.remove(self.dataline)

        self.dataline, = self.axes.plot(timearray,data, linestyle = '-', color = 'b')

        mintime = min(timearray)
        maxtime = max(timearray)
        padtime = (maxtime-mintime)/10

        self.axes.set_xlim(mintime - padtime,maxtime + padtime)
        self.fig.autofmt_xdate()
        self.axes.set_ylim(min(data),max(data))
        
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
        self.fig.tight_layout()

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
ui.link_buttons()
MainWindow.show()

ui.open_tdmsfile('C:\\Labview Test Data\\2018-09-04\\Sensors\\Log_Sensors_DAQ_0.tdms') #Windows
#ui.open_tdmsfile('//home//lee//Downloads//2018-08-22//Sensors//Log_Sensors_DAQ_5.tdms') #Linux


sys.exit(app.exec_())
