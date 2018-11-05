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

from PyQt5 import QtCore, QtWidgets, QtGui
from MPLCanvas import MyDynamicMplCanvas

import mhdpy.post as pp
import mhdpy.timefuncs as timefuncs
import mhdpy.eventlog as el

progname = os.path.basename(sys.argv[0]) #What is this?
progfolder = os.path.dirname(sys.argv[0])
progversion = "0.1"

class Ui_MainWindow(layout.Ui_MainWindow):
    """Main window of the post processor. Inherits from the MainWindow class within layout.py"""

    ###Initialization###
    def __init__(self):
        self.channel = None # replace in __init__
        self.eventlog_latest = None #used so eventlog is only updated if new events are in time window
        self.Logfiletdms = None
        self.logfilepath = None
        self.jsonfile = None
        self.timearray = None

        self.settingspath = os.path.join(progfolder, "ppsettings.json")
        if not os.path.exists(self.settingspath):
            with open(self.settingspath, 'w') as filewrite:
                json.dump({},filewrite)
        
        with open(self.settingspath,'r') as fileread:
            try:
                self.ppsettings = json.load(fileread)
            except json.decoder.JSONDecodeError:
                print('Could not read settings')
                self.ppsettings = {}

        if not 'defaultpath' in self.ppsettings:
            self.ppsettings['defaultpath'] = 'C:\\Labview Test Data'
    
    def link_buttons(self):
        """links internal function to the various widgets in the main window"""
        self.plotwidget = MyDynamicMplCanvas(self,self.centralwidget, width = 5, height = 4, dpi = 100)
        self.plotwidget.setGeometry(self.mplframe.geometry())
        self.plotwidget.setObjectName("widget")
        self.startTimeInput.dateTimeChanged.connect(self.timeinput_edited)
        self.endTimeInput.dateTimeChanged.connect(self.timeinput_edited)
        self.btn_update_fig.clicked.connect(self.update_fig)
        self.btn_fitall.clicked.connect(lambda : self.plotwidget.zoom('all'))
        self.btn_zoomsel.clicked.connect(lambda : self.plotwidget.zoom('sel'))
        self.btn_zoomout.clicked.connect(lambda : self.plotwidget.zoom('out'))
        self.btn_parse.clicked.connect(self.run_routine)
        self.actionOpen.triggered.connect(self.open_tdmsfile)
        self.actionOpen_Eventlog.triggered.connect(self.open_eventlog)
        self.actionReload_ppr.triggered.connect(self.reloadppr)
        self.selectGroup.itemClicked.connect(self.update_channel_display)
        self.combo_module.currentIndexChanged.connect(self.update_functionlist)
        self.combo_function.currentIndexChanged.connect(self.update_docstring)
        self.btn_cutinternalinloc.clicked.connect(self.cutinternalinloc)
        self.select_eventtickdisplay.itemClicked.connect(self.plotwidget.update_eventticks)

        regex = QtCore.QRegExp("[0-9_]+")
        validator = QtGui.QRegExpValidator(regex)
        self.numpointsedit.setValidator(validator)
        self.numpointsedit.textChanged.connect(self.numpoints_edited)

        self.update_modulelist()
        self.update_vlines()
        
    ###Widget updating###


    #---time updating funcitons: insures that order is correct depending on which input was updated--- Note that the 'vlines_updated function' is handled within MPLCanvas.on_release
    def timeinput_edited(self):
        self.update_vlines()
        self.update_numpoints()

    def numpoints_edited(self):
        if self.timearray is not None:
            numpoints_text = self.numpointsedit.text()
            if numpoints_text != '':
                idx1 = timefuncs.nearest_timeind(self.timearray,self.time1)
                idx2 = idx1 + int(numpoints_text)
                time2 = self.timearray[idx2]
                timestamp1 = timefuncs.np64_to_unix(self.time1)   
                timestamp2 = timefuncs.np64_to_unix(time2)   
                self.update_time_inputs(timestamp1, timestamp2)
                self.update_vlines()

    def update_fig(self):
        """Update the figure"""
        if(self.Logfiletdms != None):
            selgroup = self.selectGroup.currentRow()
            channels = self.Logfiletdms.group_channels(self.groups[selgroup])
            selchannel = self.selectChannel.currentRow()

            if (self.channel == None) or (self.channel != channels[selchannel]):
                self.channel = channels[selchannel]
                self.plotwidget.update_data(self.channel)
                
            self.update_stats(self.channel)
        self.update_eventlog_display()
        
    def update_modulelist(self):
        """Pull public post processing modules from mhd.post and list in the module combo box"""
        self.combo_module.clear()

        self.modulelist = []
        moduleliststr = []

        for module in inspect.getmembers(pp,inspect.ismodule):
            if(module[0][0] != '_'):
                self.modulelist.extend([module[1]])
                moduleliststr.extend([module[0]])
        
        self.combo_module.insertItems(0,moduleliststr)
        self.update_functionlist()

    def update_functionlist(self):
        """Obtain a list of public functions in the selected module and list them"""
        self.combo_function.clear()
        self.functionlist = []
        functionliststr = []

        module = self.modulelist[self.combo_module.currentIndex()]

        members = inspect.getmembers(module,inspect.isfunction)
        self.functionlist.extend(func[1] for func in members if func[0][0] != '_')
        functionliststr.extend(func[0] for func in members if func[0][0] != '_')

        self.combo_function.insertItems(0,functionliststr)
        self.update_docstring()

    def update_docstring(self):
        """Updates the docstring display for selected post processing function"""
        self.text_docstring.clear()
        function = self.functionlist[self.combo_function.currentIndex()]
        docstring = function.__doc__
        if docstring is None:
            docstring = 'Missing Docstring'
        else:
            if(docstring[0] == '\n'):
                docstring = docstring[1:]

        self.text_docstring.insertPlainText(docstring)

    def update_vlines(self):
        """pull the time from the inputs and update the gray lines on the display"""
        self.time1 = self.startTimeInput.dateTime().toPyDateTime()
        self.time1 = self.time1.replace(tzinfo = None).astimezone(pytz.utc)
        self.time1 = np.datetime64(self.time1).astype('M8[us]')
        
        self.time2 = self.endTimeInput.dateTime().toPyDateTime()
        self.time2 = self.time2.replace(tzinfo = None).astimezone(pytz.utc)
        self.time2 = np.datetime64(self.time2).astype('M8[us]')
        
        self.plotwidget.timeline1.set_xdata([self.time1,self.time1])
        self.plotwidget.timeline2.set_xdata([self.time2,self.time2])
        
        self.plotwidget.draw()

    def update_time_inputs(self, timestamp1, timestamp2):
        """Update the time inputs based on timestamps. timestamps should be altered to numpy64"""

        startdatetime = QtCore.QDateTime()
        startdatetime.setTime_t(timestamp1)
        enddatetime = QtCore.QDateTime()
        enddatetime.setTime_t(timestamp2)

        #update the time selectors, but don't signal to update_fig
        self.startTimeInput.blockSignals(True)
        self.endTimeInput.blockSignals(True)
        self.startTimeInput.setDateTime(startdatetime)
        self.endTimeInput.setDateTime(enddatetime)
        self.startTimeInput.blockSignals(False)
        self.endTimeInput.blockSignals(False)

    def update_numpoints(self):
        if self.timearray is not None:
            idx1 = timefuncs.nearest_timeind(self.timearray,self.time1)
            idx2 = timefuncs.nearest_timeind(self.timearray,self.time2)
            numpoints = abs(idx2 - idx1)
            self.numpointsedit.blockSignals(True)
            self.numpointsedit.setText(str(numpoints))
            self.numpointsedit.blockSignals(False)

    def update_stats(self,channel):
        """update the statistics calculations and display"""
        idx1 = timefuncs.nearest_timeind(self.timearray,self.time1)
        idx2 = timefuncs.nearest_timeind(self.timearray,self.time2)
        if len(channel.data[idx1:idx2]) > 0:
            self.t_mean.setText('{0:.3f}'.format(np.mean(channel.data[idx1:idx2])))
            self.t_med.setText('{0:.3f}'.format(np.median(channel.data[idx1:idx2])))
            self.t_skew.setText('{0:.3f}'.format(stats.skew(channel.data[idx1:idx2])))
            self.t_std.setText('{0:.3f}'.format(np.std(channel.data[idx1:idx2])))
            self.t_min.setText('{0:.3f}'.format(np.min(channel.data[idx1:idx2])))
            self.t_max.setText('{0:.3f}'.format(np.max(channel.data[idx1:idx2])))

    def reloadppr(self):
        """reloads the mhdpy package and updates the module list"""
        reload_package(pp)
        self.update_modulelist()

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

        self.timearray = channels[0].time_track(absolute_time = True)
        self.timearray = self.timearray.astype('M8[us]')
        
        timestamp1 = timefuncs.np64_to_unix(self.timearray[0])
        timestamp2 = timefuncs.np64_to_unix(self.timearray[-1])

        self.update_time_inputs(timestamp1,timestamp2)
        self.timeinput_edited()

    def update_eventticklist(self):
        """Updates the event to display channels in selected group"""
        eventtypelist = []
        for event in self.jsonfile:
            eventtypelist.append(event['event']['type'])
        
        eventtypelist = list(set(eventtypelist))
        eventtypelist.sort()
        self.select_eventtickdisplay.clear()
        self.select_eventtickdisplay.insertItems(0,eventtypelist)
        



    def update_eventlog_display(self):
        """update the cut eventlog in the text display and update the folder and filename inputs"""
        
        self.eventlog_cut = el.geteventinfo(self.jsonfile,cuttimes = [self.time1,self.time2])
        if self.eventlog_cut != self.eventlog_latest:
            self.eventlog_latest = self.eventlog_cut

            string = ''

            for time, event in self.eventlog_cut.items():
                time = time.astype(datetime.datetime).replace(tzinfo = None).astimezone(pytz.utc)
                string += time.strftime('%H:%M:%S') + ' - '
                string += json.dumps(event)
                string += '\r\n'
            
            self.text_events.setText(string)
            if(self.Logfiletdms != None):
                basefilename = os.path.splitext(os.path.split(self.logfilepath)[1])[0]
                event_before = el.event_before(self.jsonfile, self.time1)
                if event_before != None:
                    folder, filename = el.gen_fileinfo(event_before)
                    filename = basefilename + filename
                else:
                    folder, filename = "",""
                self.folderEdit.setText(folder)    
                self.filenameEdit.setText(filename)

    ###Loading of files###

    def newfile_update(self):
        self.update_eventticklist()
        self.plotwidget.update_eventticks()
        self.update_fig()

    def open_eventlog(self, filepath= 0):
        if(filepath == 0):
            paths = QtWidgets.QFileDialog.getOpenFileName(MainWindow, 'Open File', self.ppsettings['defaultpath'])
            filepath = paths[0]
        if(filepath == ''):
            pass
        else:
            with open(filepath) as file_read:
                self.jsonfile = json.load(file_read)
            folder = os.path.split(filepath)[0]
            self.datefolder = folder
        
        timestamp1 = self.jsonfile[0]['dt']
        timestamp2 = self.jsonfile[-1]['dt']
        self.update_time_inputs(timestamp1,timestamp2)
        self.newfile_update()

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
            self.newfile_update()
        
    ###Running post processing routines###
    def run_routine(self):
        """Runs a post processing routine, passing in information from the main window as **kwargs"""
        index = self.combo_function.currentIndex()
        pp_function = self.functionlist[index]
        
        kwargs = {'MainWindow': MainWindow, 'ui' : ui} # Default kwargs to send to all post processing functions

        args = inspect.getfullargspec(pp_function).args # grab arguments of the funciton

        if args.__contains__('fileinpaths'):
            #if the ppfunction takes in a file path
            isinternalfile = not (self.combo_files.currentIndex())

            #Get the list of files to parse
            if(isinternalfile):
                fileinpaths = [self.logfilepath]
            else:
                fileinpaths = QtWidgets.QFileDialog.getOpenFileNames(MainWindow, 'Open File', self.ppsettings['defaultpath'], 'All Files (*)')[0]

            if fileinpaths == [None]:
                print('fileinpaths was empty')
            else:
                #if file in paths were correctly determined
                kwargs = {**kwargs, 'fileinpaths':fileinpaths}              
                if args.__contains__('times') or args.__contains__('fileoutpaths_list'):
                    #Get the list of output files and times for parsing. There is a list of output files and times for each input file     
                    times = self.gen_times()
                    timetype = self.combo_times.currentText()
                    if(isinternalfile and timetype == "Markers"): #if parsing an internal file with the markers, you can use custom filenames
                        fileoutpaths_list = [[os.path.join(self.datefolder, self.folderEdit.text(), self.filenameEdit.text()) + '.tdms']]
                    else:
                        fileoutpaths_list = self.gen_fileout(fileinpaths,times)
                    kwargs = {**kwargs, 'times': times, 'fileoutpaths_list':fileoutpaths_list}
                
                pp_function(**kwargs)
        else:
            
            pp_function(**kwargs) # need to figure how to to remove this redundant call and also allow for abort on empty fileinpaths
            
    def cutinternalinloc(self):
        """cuts up the internal logfile and places the cut file within the logfile location appending _cut """
        pp_function = pp.logfiles.cut_log_file
        fileinpaths = [self.logfilepath]
        times = self.gen_times(timetype = 0)

        folder = os.path.split(self.logfilepath)[0]

        basefilename = os.path.splitext(os.path.split(fileinpaths[0])[1])[0]

        fileoutpaths_list = [[os.path.join(folder,basefilename+'_cut.tdms')]]

        kwargs = {'MainWindow': MainWindow, 'ui' : ui}
        kwargs = {**kwargs, 'fileinpaths':fileinpaths, 'times': times, 'fileoutpaths_list':fileoutpaths_list}
        pp_function(**kwargs)      

    ###Post processing utilitiy###
    def gen_times(self, timetype = None):
        """Generate a list of times, based on the time combo list in the mainwindow"""
        if timetype == None:
            timetype = self.combo_times.currentText()
        
        times = []
        if timetype == 'Markers': 
            #Parse all files based on internal time (graph) 
            times = [(self.time1,self.time2)]
        elif timetype == "Eventlog in Time Window" or timetype == "Entire Eventlog":
            #Parse each file based on event log
            if timetype == "Eventlog in Time Window":
                cuttimes = [self.time1,self.time2]
            else:
                cuttimes = None
            tci = el.geteventinfo(self.jsonfile,cuttimes = cuttimes,eventstr='TestCaseInfoChange')
            timelist = list(tci.keys())
            for i in range(len(tci)-1):
                times.append((timelist[i],timelist[i+1]))
            
            #Add a time like 30 years in the future to just encapsulate the last data point...super janky.
            times.append((timelist[-1],timelist[-1] + np.timedelta64(1000))) 
        elif timetype == "PIMAX1 Savetimes":
            saveevents = el.geteventinfo(self.jsonfile,eventstr='VISavingChange')
            camsaveevents = []
            timeslist = []
            for time, saveevent in saveevents.items():
                if saveevent['name'] == "PIMAX_1":
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
                folder, filename = el.gen_fileinfo(el.event_before(self.jsonfile,timepair[0]))
                fileoutpaths.append(os.path.join(self.datefolder, folder, basefilename + filename) + '.tdms')
            fileoutpaths_list.append(fileoutpaths)

        return fileoutpaths_list
    
def reload_package(package):
    """
    reloads a package and all subpackages

    Found from: https://stackoverflow.com/questions/28101895/reloading-packages-and-their-submodules-recursively-in-python
    """
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


#ui.update_fig()

sys.exit(app.exec_())
