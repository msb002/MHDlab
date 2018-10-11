# -*- coding: utf-8 -*-
"""
PyQt 5 matplotlib canvas ojbect for plotting of data in the post processor GUI.
"""

from __future__ import unicode_literals
import numpy as np
import time
import pandas as pd
import os
import sys
import pytz
import tzlocal
import datetime

import matplotlib as mpl
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtWidgets, QtGui


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import mhdpy.timefuncs as timefuncs

progname = os.path.basename(sys.argv[0])
progversion = "0.1"



class MyDynamicMplCanvas(FigureCanvas):
    def __init__(self, mainwindow, parent = None, width =5, height = 4, dpi = 100):
        self.mainwindow = mainwindow #reference of main window so that those class funcitons can be called

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
        self.dataline, = self.axes.plot([], [], 'r')
        self.timeline1 = self.axes.axvline(0, linestyle = '--', color = 'gray')
        self.timeline2 = self.axes.axvline(0, linestyle = '--', color = 'gray')
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
            press = mpl.dates.num2date(event.xdata)
            self.press = x0, press
            clickedonartist = True
        
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
                    datetime.setTime_t(timefuncs.datetime_to_unix(time[0])+1) # Add one second to make sure on right side of test case info

                    if(self.lastselectedline == self.timeline1):
                        self.mainwindow.startTimeInput.setDateTime(datetime)
                    elif(self.lastselectedline == self.timeline2):
                        self.mainwindow.endTimeInput.setDateTime(datetime)


        if clickedonartist == False: 
            # didn't click on anything 

            self.annot.set_visible(False)
            self.update_eventticks()
            self.lastselectedline =  None
            self.timeline1.set_color('gray')
            self.timeline2.set_color('gray')

        self.draw()
        
    def onmotion(self,event):
        if self.press == None: return
        if self.selectedline == None: return

        #calculate new position of the vertical line and draw it. 
        x0, xpress = self.press
        dx = mpl.dates.num2date(event.xdata) - xpress
        newtime = x0 + dx
        self.selectedline.set_xdata([newtime,newtime])
        self.selectedline.figure.canvas.draw()


    def onrelease(self,event):
        if self.selectedline != None:
            #if letting go of a line, update the relevant time display.

            x0, xpress = self.press
            dx = mpl.dates.num2date(event.xdata) - xpress
            newtime = x0 + dx
            startdatetime = QtCore.QDateTime()
            startdatetime.setTime_t(newtime.timestamp())
            if self.selectedline == self.timeline1:
                self.mainwindow.startTimeInput.setDateTime(startdatetime)
            elif self.selectedline == self.timeline2:
                self.mainwindow.endTimeInput.setDateTime(startdatetime)
            self.mainwindow.refresh()
            self.selectedline.figure.canvas.draw()
            self.selectedline = None
            
        self.press = None 
        



    def update_data(self,channel):
        #updates the figure with a new channel. 

        timearray = channel.time_track(absolute_time = True)
        timearray = list(map(lambda x: timefuncs.np64_to_utc(x).replace(tzinfo=pytz.utc).astimezone(tzlocal.get_localzone()),timearray))
        data = channel.data

        if self.dataline in self.axes.lines:
            self.axes.lines.remove(self.dataline)

        self.dataline, = self.axes.plot(timearray,data, linestyle = '-', color = 'b', picker = 5)
        
        x_label  = 'Time'
        y_label = channel.properties['NI_ChannelName'] + ' (' + channel.properties['unit_string'] + ')'
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)

        self.zoom('all')
        self.fig.tight_layout()
        self.draw()



    def update_eventticks(self):
        #removes and replaces the event tick markers.
        for line in self.eventticks:
            if line in self.axes.lines:
                self.axes.lines.remove(line)
                
        self.eventticks = []
        for event in self.mainwindow.jsonfile:
            time = datetime.datetime.utcfromtimestamp(event['dt'])
            time = time.replace(tzinfo=pytz.utc)
            label = event['event']['type'] + '\n'
            eventinfo = event['event']['event info']
            for key in eventinfo:
                #label = tc['project'] + '\\\n' + tc['subfolder'] + '\\\n' + tc['filename'] + '_' + tc['measurementnumber']
                label = label + key + ': ' +  str(eventinfo[key]) + '\n'

            colordict = {
                'VIRunningChange': 'orange',
                'TestCaseInfoChange': 'r'
            }

            try:
                color = colordict[event['event']['type']]
            except:
                color = 'black'
            
            self.eventticks.append(self.axes.axvline(time, ymin = 0.9, ymax = 1, color = color,label = label,picker = 5, linewidth = 5))
            ##these vertical lines do not need to be in local time for some reason
        self.draw()
    
    def zoom(self,option):
        #change the x window size, depending on the option
        timearray = self.dataline.get_xdata()
        ydata = self.dataline.get_ydata()
        if(option == 'sel'):
            #vertical line selection
            self.axes.set_xlim(self.timeline1.get_xdata()[0],self.timeline2.get_xdata()[0])
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

        self.fig.autofmt_xdate()
        self.axes.set_ylim(min(ydata),max(ydata))
        self.draw()

