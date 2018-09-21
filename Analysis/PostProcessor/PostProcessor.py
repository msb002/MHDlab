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
import scipy.stats as stats

import MHDpy.pproutines as pproutines
import MHDpy.various as various

import layout
import random
from PyQt5 import QtCore, QtWidgets, QtGui

import inspect

from MPLCanvas import MyDynamicMplCanvas

progname = os.path.basename(sys.argv[0])
progversion = "0.1"


class Ui_MainWindow(layout.Ui_MainWindow):
    #The main window inherits from the MainWindow class within layout.py
    def link_buttons(self):
        #functions are tied to the widgets
        self.plotwidget = MyDynamicMplCanvas(self,self.centralwidget, width = 5, height = 4, dpi = 100)
        self.plotwidget.setGeometry(QtCore.QRect(0, 0, 400, 300))
        self.plotwidget.setObjectName("widget")
        self.startTimeInput.dateTimeChanged.connect(self.refresh)
        self.endTimeInput.dateTimeChanged.connect(self.refresh)
        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_fitall.clicked.connect(lambda : self.plotwidget.zoom('all'))
        self.btn_zoomsel.clicked.connect(lambda : self.plotwidget.zoom('sel'))
        self.btn_zoomout.clicked.connect(lambda : self.plotwidget.zoom('out'))


        self.btn_parse.clicked.connect(self.run_routine)

        self.btn_open.clicked.connect(self.open_tdmsfile)
        self.selectGroup.itemClicked.connect(self.update_channel_display)

        self.channel = None # replace in __init__
        self.eventlog = None

        self.routinelist = [func[1] for func in inspect.getmembers(pproutines,inspect.isfunction) if func[0][0] != '_']
        self.routineliststr = [func[0] for func in inspect.getmembers(pproutines,inspect.isfunction) if func[0][0] != '_']
        self.combo_routines.insertItems(0,self.routineliststr)

    def open_tdmsfile(self, filepath= 0):
        if(filepath == 0):
            paths = QtWidgets.QFileDialog.getOpenFileName(MainWindow, 'Open File', 'C:\\Labview Test Data')
            filepath = paths[0]
        if(filepath == ''):
            pass
        else:
            
            
            self.Logfiletdms = TF(filepath)
            self.logfilepath = filepath
            folder = os.path.split(filepath)[0]

            #search upward in file directory for eventlog.json, then set that as the date folder
            while(True):             
                filelist = os.listdir(folder)
                if 'Eventlog.json' in filelist:
                    self.datefolder = folder
                    eventlogpath = os.path.join(self.datefolder,'Eventlog.json')
                    with open(eventlogpath) as fp:
                        self.jsonfile = json.load(fp)
                    break
                folder = os.path.split(folder)[0]

            #pull out groups and populate the group display
            self.groups = self.Logfiletdms.groups()
            self.selectGroup.clear()
            self.selectGroup.insertItems(0,self.groups)
            self.selectGroup.setCurrentRow(0)

            self.update_channel_display()
            self.plotwidget.update_eventticks()
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

        #update_time_displays : updates the time inputs to max and min of channel
        self.timearray = channels[0].time_track(absolute_time = True)
        self.timedata = list(map(lambda x: various.np64_to_utc(x),self.timearray))

        startdatetime = QtCore.QDateTime()
        startdatetime.setTime_t(various.np64_to_unix(self.timearray[0]))
        enddatetime = QtCore.QDateTime()
        enddatetime.setTime_t(various.np64_to_unix(self.timearray[-1]))

        self.startTimeInput.setDateTime(startdatetime)
        self.endTimeInput.setDateTime(enddatetime)

        
    def refresh(self):
        #full refresh of everything
        selgroup = self.selectGroup.currentRow()
        channels = self.Logfiletdms.group_channels(self.groups[selgroup])
        selchannel = self.selectChannel.currentRow()

        if (self.channel == None) or (self.channel != channels[selchannel]):
            self.channel = channels[selchannel]
            self.plotwidget.update_data(self.channel)
        
        self.refresh_time()
        self.cut_eventlog()
        self.update_stats(self.channel)
        

    def refresh_time(self):
        #pull the time from the inputs and update the gray lines on the display and cut event log
        self.time1 = self.startTimeInput.dateTime().toPyDateTime()
        self.time1 = self.time1.replace(tzinfo = None).astimezone(pytz.utc)
        
        self.time2 = self.endTimeInput.dateTime().toPyDateTime()
        self.time2 = self.time2.replace(tzinfo = None).astimezone(pytz.utc)
        
        self.plotwidget.timeline1.set_xdata([self.time1,self.time1])
        self.plotwidget.timeline2.set_xdata([self.time2,self.time2])
        
        self.plotwidget.draw()

    def update_stats(self,channel):
        #update the statistics calculations and display
        idx1 = various.nearest_timeind(self.timedata,self.time1)
        idx2 = various.nearest_timeind(self.timedata,self.time2)
        if len(channel.data[idx1:idx2]) > 0:
            self.t_mean.setText('{0:.3f}'.format(np.mean(channel.data[idx1:idx2])))
            self.t_med.setText('{0:.3f}'.format(np.median(channel.data[idx1:idx2])))
            self.t_skew.setText('{0:.3f}'.format(stats.skew(channel.data[idx1:idx2])))
            self.t_std.setText('{0:.3f}'.format(np.std(channel.data[idx1:idx2])))
            self.t_min.setText('{0:.3f}'.format(np.min(channel.data[idx1:idx2])))
            self.t_max.setText('{0:.3f}'.format(np.max(channel.data[idx1:idx2])))

    def cut_eventlog(self):
        #create array of events within the time window
        self.eventlog_cut= []
        for event in self.jsonfile:
            time = datetime.datetime.utcfromtimestamp(event['dt'])
            time = time.replace(tzinfo=pytz.utc)
            if((time>self.time1) and (time<self.time2)):
                self.eventlog_cut.append(event)
        if self.eventlog_cut != self.eventlog:
            self.eventlog = self.eventlog_cut
            self.display_eventlog()

    def display_eventlog(self):
        #refresh the cut eventlog in the text display and update the folder and filename inputs
        string = ''

        for event in self.eventlog_cut:
            time = datetime.datetime.utcfromtimestamp(event['dt'])
            string += time.strftime('%H:%M:%S') + ' - '
            string += json.dumps(event['event'])
            string += '\r\n'
        
        self.textBrowser.setText(string)

        tci_cut = self.gettestcaseinfo(cut = True)
        basefilename = os.path.splitext(os.path.split(self.logfilepath)[1])[0]
        folder, filename = self.get_fileinfo(tci_cut[-1])
        filename = basefilename + filename
        self.folderEdit.setText(folder)    
        self.filenameEdit.setText(filename)

    def get_fileinfo(self,tci_event):
            folder = tci_event['project'] + '\\'+ tci_event['subfolder']
            filename = '_' + tci_event['filename'] + '_'+ tci_event['measurementnumber']
            return folder, filename
        
    def gettestcaseinfo(self, cut = False):
        #pull the testcase info from the json file, only those after time1 if cut is true
        tci = {}
        for event in self.jsonfile:
            if event['event']['type'] == 'TestCaseInfoChange':
                time = datetime.datetime.utcfromtimestamp(event['dt'])
                time = time.replace(tzinfo=pytz.utc)
                tci[time] = event['event']['event info']

        #pull only those events before time1 if cut is true
        if(cut):
            tci_cut = []
            for time, event in tci.items():
                if(time<self.time1): 
                    tci_cut.append(event)
            tci = tci_cut

        return tci

    def run_routine(self):
        index = self.combo_routines.currentIndex()
        pp_function = self.routinelist[index]

        #parse a file based on the seleted times, internal or external
        folder = self.folderEdit.text()
        isinternalfile = not (self.combo_files.currentIndex())

        if(isinternalfile):
            fileinpath = self.logfilepath
            filename = self.filenameEdit.text() # having to have weird redundancies because of ability to edit filename
            basefilename = os.path.splitext(os.path.split(fileinpath)[1])[0]
        else:
            paths = QtWidgets.QFileDialog.getOpenFileName(MainWindow, 'Open File', 'C:\\Labview Test Data')
            fileinpath = paths[0]
            basefilename = os.path.splitext(os.path.split(fileinpath)[1])[0]
            tci_cut = self.gettestcaseinfo(cut = True)
            folder, filename = self.get_fileinfo(tci_cut[-1])
            filename = basefilename + filename
        
        timetype = self.combo_times.currentIndex()

        if timetype:
            fileoutpath = os.path.join(self.datefolder, folder, filename)
            fileoutpath =   fileoutpath + '.tdms'
            pp_function(fileinpath, fileoutpath, self.time1, self.time2)
        else:
            tci = self.gettestcaseinfo(cut = False)
            i=0
            for i in range(len(tci)-1):
                times = list(tci.keys())
                folder, filename = self.get_fileinfo(tci[times[i]])
                newfilename = basefilename + filename
                fileoutpath = os.path.join(self.datefolder, folder, newfilename)
                fileoutpath =   fileoutpath + '.tdms'
                pp_function(fileinpath, fileoutpath, times[i],times[i+1])




app = QtWidgets.QApplication(sys.argv)

MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
ui.link_buttons()
MainWindow.show()

ui.open_tdmsfile('C:\\Labview Test Data\\2018-09-19\\Logfiles\\Sensors_TC\\Log_Sensors_TC_0.tdms') #Windows
#ui.open_tdmsfile('//home//lee//Downloads//2018-08-22//Sensors//Log_Sensors_DAQ_5.tdms') #Linux

#ui.refresh()

sys.exit(app.exec_())
