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
import matplotlib.pyplot as plt
import scipy.stats as stats

import MHDpy.various as various
import MHDpy.SPEparse
from PyQt5 import QtCore, QtWidgets, QtGui

### High level post processing (processes multiple types of files in a predefined way)
def parse_lasertiming(fileinpaths, **kwargs):
    intensities, timestamps = MHDpy.SPEparse.parse_lasertiming(fileinpaths)
    folder = os.path.split(fileinpaths[0])[0]
    fileoutpath = os.path.join(folder, 'PIMax_Timing_Parsed.tdms')

    root_object = RootObject(properties={})

    with TdmsWriter(fileoutpath,mode = 'w') as tdms_writer:
        _write_dataframe(tdms_writer, intensities ,"MaxIntensities")
        _write_dataframe(tdms_writer, timestamps ,"Timestamps")

# Mid level post processing (processes a specific type of file)
def cut_log_file(fileinpaths, times, fileoutpaths_list, **kwargs):
    for i in range(len(fileinpaths)):
        fileinpath = fileinpaths[i]
        fileoutpaths = fileoutpaths_list[i]
        tdmsfile = TF(fileinpath)
        for j in range(len(times)):
            time1 = times[j][0]
            time2 = times[j][1]
            fileoutpath = fileoutpaths[j]
            
            direc = os.path.split(fileoutpath)[0]
            if not os.path.exists(direc):
                os.makedirs(direc)

            root_object = RootObject(properties={ #TODO root properties
            })

            try:
                with TdmsWriter(fileoutpath,mode='w') as tdms_writer:
                    for group in tdmsfile.groups():
                        for channel in tdmsfile.group_channels(group):
                            channel_object = _cut_channel(channel,time1,time2, timedata = None)
                            tdms_writer.write_segment([
                                root_object,
                                channel_object])
            except ValueError as error:
                print(error)
                print('removing the file at: \n', fileoutpath)
                os.remove(fileoutpath)

def cut_powermeter(fileinpaths, times, fileoutpaths_list, **kwargs):
    for i in range(len(fileinpaths)):
        fileinpath = fileinpaths[i]
        fileoutpaths = fileoutpaths_list[i]
        tdmsfile = TF(fileinpath)
        for j in range(len(times)):
            time1 = times[j][0]
            time2 = times[j][1]
            fileoutpath = fileoutpaths[j]

            direc = os.path.split(fileoutpath)[0]
            if not os.path.exists(direc):
                os.makedirs(direc)

            root_object = RootObject(properties={ #TODO root properties
            })
            try:
                with TdmsWriter(fileoutpath,mode='w') as tdms_writer:
                    for group in tdmsfile.groups():
                        timedata = tdmsfile.channel_data(group,'Time_LV')
                        for channel in tdmsfile.group_channels(group):
                            if type(channel.data_type.size) == type(None): break #skips over non numeric channels
                            channel_object = _cut_channel(channel,time1,time2, timedata = timedata)
                            tdms_writer.write_segment([
                                root_object,
                                channel_object])
            except ValueError as error:
                print(error)
                print('removing the file at: \n', fileoutpath)
                os.remove(fileoutpath)

#Low level post processing (Functions inside a file)

def _cut_channel(channel,time1,time2, timedata = None):

    waveform = False
    if(timedata == None): #if no timedata is passed, assume channel is a waveform
        timedata = channel.time_track(absolute_time = True)
        time1 = np.datetime64(time1)
        time2 = np.datetime64(time2)
        #print(time1)
        #print(timedata)
        idx1, idx2 =  _get_indextime(timedata, time1,time2, dtype = 'np64')
        waveform = True
    else:
        idx1, idx2 =  _get_indextime(timedata, time1,time2)

    if(idx1 == idx2): #times are not within file
        raise ValueError('times not in file ' + channel.tdms_file.object().properties['name'])

    props = channel.properties
    if(waveform):
        start= props['wf_start_time']
        offset = datetime.timedelta(milliseconds = props['wf_increment']*1000*idx1)
        props['wf_start_time'] = start + offset

    return ChannelObject(channel.group, channel.channel, channel.data[idx1:idx2], properties=props)
    
def _get_indextime(timedata, time1,time2,dtype = 'datetime'):
    if(time2 > time1):
        idx1 = various.nearest_timeind(timedata,time1,dtype)
        idx2 = various.nearest_timeind(timedata,time2,dtype)
    else:
        idx2 = various.nearest_timeind(timedata,time1,dtype)
        idx1 = various.nearest_timeind(timedata,time2,dtype)

    return idx1,idx2    

def _write_dataframe(tdms_writer, dataframe, name):

    root_object = RootObject(properties={ })
    i=0
    for column in dataframe.iteritems():
        column = column[1].as_matrix()
        channel_object = ChannelObject(name, name + "_" + str(i) , column)
        tdms_writer.write_segment([root_object,channel_object])
        i=i+1
if __name__ == '__main__':
    fileinpaths = ['C:/Labview Test Data/2018-09-19/Logfiles/Sensors_DAQ/Log_Sensors_DAQ_0.tdms']
    time1 = datetime.datetime(2018, 9, 19, 21, 21,tzinfo = pytz.utc)
    #time1 = time1.replace(tzinfo = None).astimezone(pytz.utc)
    time2 = datetime.datetime(2018, 9, 19, 21, 32, 16,tzinfo = pytz.utc)
    #time2 = time2.replace(tzinfo = None).astimezone(pytz.utc)
    times = [(time1 ,time2 )]
    fileoutpaths_list = [['C:\\Labview Test Data\\2018-09-19\\UnspecifiedProj\\Temp Dependence\\Log_Sensors_DAQ_0_400C_0.tdms']]
    cut_log_file(fileinpaths, times, fileoutpaths_list)
    pass
