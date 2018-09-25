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
from PyQt5 import QtCore, QtWidgets, QtGui

### High level post processing (processes multiple types of files in a predefined way)
def parse_lasertiming(MainWindow, ui, **kwargs):
    #QtWidgets.QFileDialog.getOpenFileNames(MainWindow, 'Open Files', 'C:\\Labview Test Data')
    print(ui.logfilepath)

def test(fileinpaths, fileoutpaths, times, **kwargs):
    print(fileinpaths)
    print(fileoutpaths)
    print(times)


# Mid level post processing (processes a specific type of file)
def cut_log_file(fileinpath, fileoutpath, time1, time2, **kwargs):
    tdmsfile = TF(fileinpath)

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

def cut_powermeter(fileinpath, fileoutpath, time1, time2, **kwargs):
    tdmsfile = TF(fileinpath)
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
        timearray = channel.time_track(absolute_time = True)
        timedata = list(map(lambda x: various.np64_to_utc(x),timearray))
        waveform = True

    idx1, idx2 =  _get_indextime(timedata, time1,time2)

    if(idx1 == idx2): #times are not within file
        raise ValueError('times not in file ' + channel.tdms_file.object().properties['name'])

    props = channel.properties
    if(waveform):
        start= props['wf_start_time']
        offset = datetime.timedelta(milliseconds = props['wf_increment']*1000*idx1)
        props['wf_start_time'] = start + offset

    return ChannelObject(channel.group, channel.channel, channel.data[idx1:idx2], properties=props)


def _get_indextime(timedata, time1,time2):
    if(time2 > time1):
        idx1 = various.nearest_timeind(timedata,time1)
        idx2 = various.nearest_timeind(timedata,time2)
    else:
        idx2 = various.nearest_timeind(timedata,time1)
        idx1 = various.nearest_timeind(timedata,time2)

    return idx1,idx2

if __name__ == '__main__':
    pass
