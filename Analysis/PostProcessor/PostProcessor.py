# -*- coding: utf-8 -*-
"""
A post processing GUI function for parsing log files.

In general this Gui is used to call post processing functions from mhdpy.post. Some post processing functions want informaiton like a list of input files and times to parse those files by, and this GUI facilitates gathering that information. Use the vertical bars on the graph to select the desired parsing times, or select a time selection function to get a list of times (from the event log for instance).
"""

from __future__ import unicode_literals
import numpy as np
import os
import sys
from nptdms import TdmsFile as TF
import datetime
import pytz
import json
import scipy.stats as stats
import layout
import inspect
import importlib
import types

from PyQt5 import QtCore, QtWidgets
from MPLCanvas import MyDynamicMplCanvas

import mhdpy.post as pp
import mhdpy.timefuncs as timefuncs



progname = os.path.basename(sys.argv[0])
progversion = "0.1"

progfolder = os.path.dirname(sys.argv[0])

class Ui_MainWindow(layout.Ui_MainWindow):
    """Main window of the post processor. Inherits from the MainWindow class within layout.py"""

    def __init__(self):
        self.channel = None # replace in __init__
        self.eventlog = None
        self.Logfiletdms = None

        self.settingspath = os.path.join(progfolder, "ppsettings.json")
        if not os.path.exists(self.settingspath):
            print('hello')
            with open(self.settingspath, 'w') as filewrite:
                json.dump({},filewrite)
        
        with open(self.settingspath,'r') as fileread:
            try:
                self.ppsettings = json.load(fileread)
            except json.decoder.JSONDecodeError:
                print('Could not read settings')
                self.ppsettings = {}
                #json.dump({},fileread)

        if not 'defaultpath' in self.ppsettings:
            self.ppsettings['defaultpath'] = 'C:\\Labview Test Data'
    

    
    def link_buttons(self):
        """links internal function to the various widgets in the main window"""
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
        self.actionOpen.triggered.connect(self.open_tdmsfile)
        self.actionReload_ppr.triggered.connect(self.reloadppr)
        self.selectGroup.itemClicked.connect(self.update_channel_display)
        
        #Pull post processing funcitons from the post processing package and add to the routines combo box
        self.routinelist = []
        self.routineliststr = []
        for module in inspect.getmembers(pp,inspect.ismodule):
            members = inspect.getmembers(module[1],inspect.isfunction)
            self.routinelist.extend(func[1] for func in members if func[0][0] != '_')
            self.routineliststr.extend(func[0] for func in members if func[0][0] != '_')
        self.combo_routines.insertItems(0,self.routineliststr)

    def open_tdmsfile(self, filepath= 0):
        """
        Loads in a tdms file to be displayed for parsing.
        
        This function also searches for the eventlog in higher folders.
        """

        if(filepath == 0):
            paths = QtWidgets.QFileDialog.getOpenFileName(MainWindow, 'Open File', self.ppsettings['defaultpath'])
            filepath = paths[0]
        if(filepath == ''):
            pass
        else:
            
            self.Logfiletdms = TF(filepath)
            self.logfilepath = filepath
            folder = os.path.split(filepath)[0]

            with open(self.settingspath,'w') as writefile:
                self.ppsettings['defaultpath'] = folder
                json.dump(self.ppsettings,writefile )

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
        """Updates the channel list to display channels in selected group"""
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
        self.timedata = list(map(lambda x: timefuncs.np64_to_utc(x),self.timearray))

        startdatetime = QtCore.QDateTime()
        startdatetime.setTime_t(timefuncs.np64_to_unix(self.timearray[0]))
        enddatetime = QtCore.QDateTime()
        enddatetime.setTime_t(timefuncs.np64_to_unix(self.timearray[-1]))

        self.startTimeInput.setDateTime(startdatetime)
        self.endTimeInput.setDateTime(enddatetime)

    def refresh(self):
        """full refresh of everything"""
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
        """pull the time from the inputs and update the gray lines on the display and cut event log"""
        self.time1 = self.startTimeInput.dateTime().toPyDateTime()
        self.time1 = self.time1.replace(tzinfo = None).astimezone(pytz.utc)
        
        self.time2 = self.endTimeInput.dateTime().toPyDateTime()
        self.time2 = self.time2.replace(tzinfo = None).astimezone(pytz.utc)
        
        self.plotwidget.timeline1.set_xdata([self.time1,self.time1])
        self.plotwidget.timeline2.set_xdata([self.time2,self.time2])
        
        self.plotwidget.draw()

    def update_stats(self,channel):
        """update the statistics calculations and display"""
        idx1 = timefuncs.nearest_timeind(self.timedata,self.time1)
        idx2 = timefuncs.nearest_timeind(self.timedata,self.time2)
        if len(channel.data[idx1:idx2]) > 0:
            self.t_mean.setText('{0:.3f}'.format(np.mean(channel.data[idx1:idx2])))
            self.t_med.setText('{0:.3f}'.format(np.median(channel.data[idx1:idx2])))
            self.t_skew.setText('{0:.3f}'.format(stats.skew(channel.data[idx1:idx2])))
            self.t_std.setText('{0:.3f}'.format(np.std(channel.data[idx1:idx2])))
            self.t_min.setText('{0:.3f}'.format(np.min(channel.data[idx1:idx2])))
            self.t_max.setText('{0:.3f}'.format(np.max(channel.data[idx1:idx2])))

    def cut_eventlog(self):
        """create array of events that are between the two timemarkers"""
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
        """refresh the cut eventlog in the text display and update the folder and filename inputs"""
        string = ''

        for event in self.eventlog_cut:
            time = datetime.datetime.utcfromtimestamp(event['dt'])
            string += time.strftime('%H:%M:%S') + ' - '
            string += json.dumps(event['event'])
            string += '\r\n'
        
        self.textBrowser.setText(string)

        tci_cut = self.geteventinfo('TestCaseInfoChange',cut = True)
        basefilename = os.path.splitext(os.path.split(self.logfilepath)[1])[0]
        folder, filename = self.gen_fileinfo(tci_cut[-1])
        filename = basefilename + filename
        self.folderEdit.setText(folder)    
        self.filenameEdit.setText(filename)

    def gen_fileinfo(self,tci_event):
        """Takes in a test case and return a destination folder and filename"""
        folder = tci_event['project'] + '\\'+ tci_event['subfolder']
        filename = '_' + tci_event['filename'] + '_'+ tci_event['measurementnumber']
        return folder, filename
        
    def geteventinfo(self,eventstr, cut = False):
        """pull the testcase info from the json file, only those after time1 if cut is true"""
        tci = {}
        for event in self.jsonfile:
            if event['event']['type'] == eventstr:
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
        """Runs a post processing routine, passing in information from the main window as **kwargs"""
        index = self.combo_routines.currentIndex()
        pp_function = self.routinelist[index]

        #parse a file based on the seleted times, internal or external
        folder = self.folderEdit.text()

        #filename = self.filenameEdit.text() #Abandoned custom filename for now as it cases issues

        isinternalfile = not (self.combo_files.currentIndex())

        kwargs = {'MainWindow': MainWindow, 'ui' : ui}

        #Get the list of files to parse
        if(isinternalfile):
            fileinpaths = [self.logfilepath]
        else:
            fileinpaths = QtWidgets.QFileDialog.getOpenFileNames(MainWindow, 'Open File', self.ppsettings['defaultpath'], 'All Files (*)')[0]

        #Get the list of output files and times for parsing. There is a list of output files and times for each input file     
        if self.Logfiletdms == None:
            times = None
            fileoutpaths_list = None
        else:
            times = self.gen_times()
            fileoutpaths_list = self.gen_fileout(fileinpaths,times)
            
        kwargs = {**kwargs, 'fileinpaths':fileinpaths, 'times': times, 'fileoutpaths_list':fileoutpaths_list}
        pp_function(**kwargs)

    def gen_times(self):
        """Generate a list of times, based on the time combo list in the mainwindow"""
        timetype = self.combo_times.currentIndex()
        
        times = []
        if timetype == 0: 
            #Parse all files based on internal time (graph) 
            times = [(self.time1,self.time2)]
        elif timetype == 1: 
            #Parse each file based on event log
            tci = self.geteventinfo('TestCaseInfoChange',cut = False)
            timelist = list(tci.keys())
            for i in range(len(tci)-1):
                times.append((timelist[i],timelist[i+1]))
        elif timetype == 2:
            saveevents = self.geteventinfo('VISavingChange',cut = False)
            camsaveevents = []
            timeslist = []
            for time, saveevent in saveevents.items():
                if saveevent['name'] == "PIMAX-Cam1":
                    camsaveevents.append(saveevent)
                    timeslist.append(time)
            for i in range(len(camsaveevents)-1):
                event1 = camsaveevents[i]
                event2 = camsaveevents[i+1]
                if(event1['newstate'] == True and event2['newstate'] == False):
                    times.append((timeslist[i],timeslist[i+1]))

        return times

    def gen_fileout(self,fileinpaths,times):
        """Generate fileoutpaths_list useing the times array and eventlog"""
        fileoutpaths_list = []
        
        for fileinpath in fileinpaths:
            basefilename = os.path.splitext(os.path.split(fileinpath)[1])[0]
            fileoutpaths= []
            for timepair in times:
                folder, filename = self.gen_fileinfo(self.event_before(timepair[0]))
                fileoutpaths.append(os.path.join(self.datefolder, folder, basefilename + filename) + '.tdms')
            fileoutpaths_list.append(fileoutpaths)

        return fileoutpaths_list
    
    def event_before(self,time_cut):
        """returns the event before time_cut"""
        tci = self.geteventinfo('TestCaseInfoChange',cut = False)
        tci_cut = []
        for time, event in tci.items():
            if(time<=time_cut): 
                tci_cut.append(event)
        return tci_cut[-1]

    def reloadppr(self):
        reload_package(pp)

        self.routinelist = []
        self.routineliststr = []
        self.combo_routines.clear()
        for module in inspect.getmembers(pp,inspect.ismodule):
            members = inspect.getmembers(module[1],inspect.isfunction)
            self.routinelist.extend(func[1] for func in members if func[0][0] != '_')
            self.routineliststr.extend(func[0] for func in members if func[0][0] != '_')
        self.combo_routines.insertItems(0,self.routineliststr)

def reload_package(package):
    #https://stackoverflow.com/questions/28101895/reloading-packages-and-their-submodules-recursively-in-python
    assert(hasattr(package, "__package__"))
    fn = package.__file__
    fn_dir = os.path.dirname(fn) + os.sep
    module_visit = {fn}
    del fn

    def reload_recursive_ex(module):
        importlib.reload(module)

        for module_child in vars(module).values():
            if isinstance(module_child, types.ModuleType):
                fn_child = getattr(module_child, "__file__", None)
                if (fn_child is not None) and fn_child.startswith(fn_dir):
                    if fn_child not in module_visit:
                        # print("reloading:", fn_child, "from", module)
                        module_visit.add(fn_child)
                        reload_recursive_ex(module_child)

    return reload_recursive_ex(package)
 

app = QtWidgets.QApplication(sys.argv)

MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
ui.link_buttons()
MainWindow.show()

#ui.open_tdmsfile('C:\\Labview Test Data\\2018-09-19\\Logfiles\\Sensors_TC\\Log_Sensors_TC_0.tdms') #Windows
#ui.open_tdmsfile('//home//lee//Downloads//2018-08-22//Sensors//Log_Sensors_DAQ_5.tdms') #Linux


#ui.refresh()

sys.exit(app.exec_())
