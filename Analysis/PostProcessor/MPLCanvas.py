# -*- coding: utf-8 -*-
"""
PyQt 5 matplotlib canvas ojbect for plotting of data in the post processor GUI.
"""

from __future__ import unicode_literals
import os
import sys
import pytz
import tzlocal
import datetime
import numpy as np
from PyQt5 import QtCore, QtWidgets

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter, FuncFormatter



import mhdpy.timefuncs as timefuncs

progname = os.path.basename(sys.argv[0])
progversion = "0.1"



class MyDynamicMplCanvas(FigureCanvas):
    def __init__(self, mainwindow, parent = None, width =5, height = 4, dpi = 100):
        self.mainwindow = mainwindow #reference of main window so that those class funcitons can be called

        mpl.rcParams.update({'font.size': 12})
        #setup the figure
        self.fig, self.axes= plt.subplots(figsize = (width,height), dpi=dpi)
        
        self.compute_initial_figure()
        FigureCanvas.__init__(self,self.fig)
        FigureCanvas.setSizePolicy(self,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.setParent(parent)

        #setup to detect mouse events
        self.cidpress = self.axes.figure.canvas.mpl_connect('button_press_event',self.onpress)
        self.cidmotion = self.axes.figure.canvas.mpl_connect('motion_notify_event',self.onmotion)
        self.cidrelease = self.axes.figure.canvas.mpl_connect('button_release_event',self.onrelease)
        self.press = None
        self.selectedline = None
        self.lastselectedline = None

    def compute_initial_figure(self):
        dataline, = self.axes.plot([], [], 'r')
        self.datalines = [dataline]
        self.timeline1 = self.axes.axvline(0, linestyle = '--', color = 'gray',zorder = 3)
        self.timeline2 = self.axes.axvline(0, linestyle = '--', color = 'gray',zorder = 3)
        self.eventticks = [mpl.lines.Line2D([0],[0])]
        bbox_props = dict(boxstyle="square", fc="white", ec="black", lw=2)
        self.annot = self.axes.text(0.25,0.25,'hello' ,visible = False, transform=self.axes.transAxes, backgroundcolor =  'w', bbox = bbox_props)

    def onpress(self, event):
        
        clickedonartist = False # not sure how to check that 'only the canvas without ticks' was clicked on (i.e. wihtout ticks)

        if(self.timeline1.contains(event)[0] or self.timeline2.contains(event)[0]):
            #clicked on a line

            self.timeline1.set_color('gray')
            self.timeline2.set_color('gray')
            if(self.timeline1.contains(event)[0]):
                self.selectedline = self.timeline1
                self.lastselectedline =  self.timeline1

            if(self.timeline2.contains(event)[0]):
                self.selectedline = self.timeline2
                self.lastselectedline =  self.timeline2

            self.selectedline.set_color('g')
            x0 = self.selectedline.get_xdata()[0]
            eventxdata = event.xdata
            press = np.datetime64(mpl.dates.num2date(eventxdata))
            self.press = x0, press
            clickedonartist = True
        if self.mainwindow.jsonfile != None:
            self.update_eventticks()
        for tick in self.eventticks:
            if(tick.contains(event)[0]):
                #clicked on an event tick
                
                self.annot.set_text(tick.get_label())
                self.annot.set_visible(True)
                tick.set_color('g')
                clickedonartist = True

                if (event.dblclick == True) and (self.lastselectedline != None):
                    self.annot.set_visible(False)
                    time = tick.get_xdata()
                    datetime = QtCore.QDateTime()
                    datetime.setTime_t(timefuncs.np64_to_unix(time[0])+1) # Add one second to make sure on right side of test case info

                    if(self.lastselectedline == self.timeline1):
                        self.mainwindow.startTimeInput.setDateTime(datetime)
                    elif(self.lastselectedline == self.timeline2):
                        self.mainwindow.endTimeInput.setDateTime(datetime)


        if clickedonartist == False: 
            # didn't click on anything 

            self.annot.set_visible(False)
            self.lastselectedline =  None
            self.timeline1.set_color('gray')
            self.timeline2.set_color('gray')
            if self.mainwindow.jsonfile != None:
                self.update_eventticks()

        self.draw()
        
    def onmotion(self,event):
        if self.press == None: return
        if self.selectedline == None: return

        #calculate new position of the vertical line and draw it. 
        x0, xpress = self.press
        dx = np.datetime64(mpl.dates.num2date(event.xdata)) - xpress
        newtime = x0 + dx
        self.selectedline.set_xdata([newtime,newtime])
        self.selectedline.figure.canvas.draw()


    def onrelease(self,event):
        if self.selectedline != None:
            #if letting go of a line, update the relevant time display.

            x0, xpress = self.press
            dx = np.datetime64(mpl.dates.num2date(event.xdata)) - xpress
            newtime = x0 + dx
            startdatetime = QtCore.QDateTime()
            startdatetime.setTime_t(timefuncs.np64_to_unix(newtime))
            if self.selectedline == self.timeline1:
                self.mainwindow.startTimeInput.setDateTime(startdatetime)
            elif self.selectedline == self.timeline2:
                self.mainwindow.endTimeInput.setDateTime(startdatetime)
            self.selectedline.figure.canvas.draw()
            self.mainwindow.update_eventlog_display()
            if (self.mainwindow.channel_data is not None):
                self.mainwindow.update_stats()
            self.selectedline = None
            
        self.press = None 
        
    def update_data(self,channel_array):
        #updates the figure with a new channel. 

        for dataline in self.datalines:
            if dataline in self.axes.lines:
                self.axes.lines.remove(dataline)
        self.datalines = []
        self.axes.set_prop_cycle(None)

        for channel in channel_array:
            timearray = channel.time_track(absolute_time = True)[::self.mainwindow.stride]
            timearray = timearray.astype('M8[us]').tolist()
            # timearray = mpl.dates.date2num(timearray) #need to try this
            
            data = channel.data[::self.mainwindow.stride]

            dataline, = self.axes.plot(timearray,data, linestyle = '-', picker = 5, label = channel.group + '\\' + channel.channel)
            self.datalines.append(dataline)

        self.axes.xaxis.set_major_formatter(FuncFormatter(dateformatter))
        x_label  = 'Time'
        y_label = channel.properties['NI_ChannelName'] + ' (' + channel.properties['unit_string'] + ')'
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)

        self.zoom('all')
        

        leg = self.axes.legend_
        if leg is not None:
            leg.remove()
            self.axes.legend()
        
        try:
            self.fig.tight_layout()
        except:
            print('could not run tight_layout, legend is probably too large')
        self.draw()

    def update_eventticks(self):
        #removes and replaces the event tick markers.
        for line in self.eventticks:
            if line in self.axes.lines:
                self.axes.lines.remove(line)

        sel_eventtypes = self.mainwindow.select_eventtickdisplay.selectedItems()
        sel_eventtypes = [event.text() for event in sel_eventtypes]
                
        self.eventticks = []
        for event in self.mainwindow.jsonfile:
            if event['event']['type'] in sel_eventtypes:
                time = np.datetime64(int(event['dt']),'s')
                label = event['event']['type'] + '\n'
                eventinfo = event['event']['event info']
                for key in eventinfo:
                    label = label + key + ': ' +  str(eventinfo[key]) + '\n'

                #Note: green is currently what is used for clicked items
                colordict = {
                    'VIRunningChange': 'orange',
                    'TestCaseInfoChange': 'r',
                    'VISavingChange' : 'c'
                }

                try:
                    color = colordict[event['event']['type']]
                except:
                    color = 'black'

                linestyle = '-'
                alpha = 1
                if(event['event']['type'] == 'VISavingChange'):
                    if(event['event']['event info']['name'] == 'PIMAX_2'):
                        alpha = 0.3
                self.eventticks.append(self.axes.axvline(time, ymin = 0.9, ymax = 1, color = color,alpha = alpha,linestyle = linestyle,label = label,picker = 2, linewidth = 3))
                ##these vertical lines do not need to be in local time for some reason
        self.draw()
    
    def zoom(self,option):
        #change the x window size, depending on the option
        
        if self.mainwindow.Logfiletdms == None:
            ydata = [0,1]
            time1 = datetime.datetime.utcfromtimestamp(self.mainwindow.jsonfile[0]['dt'])
            time2 = datetime.datetime.utcfromtimestamp(self.mainwindow.jsonfile[-1]['dt'])
            timearray = [time1,time2]
            
        else:
            dataline = self.datalines[0]
            ydata = dataline.get_ydata()
            timearray = dataline.get_xdata()

        #Autoscale the y axis before setting the x axis to the zoom
        # recompute the ax.dataLim
        self.axes.relim()
        # update ax.viewLim using the new dataLim
        self.axes.autoscale_view()        

        
        if(option == 'sel'):
            #vertical line selection
            mintime = self.timeline1.get_xdata()[0]
            maxtime = self.timeline2.get_xdata()[0]
            padtime = (maxtime-mintime)/10
            self.axes.set_xlim(mintime - padtime,maxtime + padtime)
        if(option == 'all'):
            #whole window
            mintime = min(timearray)
            maxtime = max(timearray)
            padtime = (maxtime-mintime)/10
            self.axes.set_xlim(mintime - padtime,maxtime + padtime)
        if(option == 'out'):
            #25 percent out
            mintime = self.axes.get_xlim()[0]
            maxtime = self.axes.get_xlim()[1]
            padtime = (maxtime-mintime)/4
            self.axes.set_xlim(mintime - padtime,maxtime + padtime)

        ##This is the old yscale code
        # miny = min(ydata)       
        # maxy = max(ydata)
        # pady = (maxy-miny)/10
        # self.axes.set_ylim(miny-pady,maxy+pady)


        self.fig.autofmt_xdate()
        self.draw()

    def legend_toggle(self):
        leg = self.axes.legend_
        if leg is None:
            self.axes.legend()
        else:
            leg.remove()
        self.draw()

def dateformatter(value, tick_number):
    time = mpl.dates.num2date(value)
    localtz = tzlocal.get_localzone()
    time = time.replace(tzinfo = pytz.utc).astimezone(localtz)
    string = time.strftime('%H:%M:%S') + ' - '
    
    return string