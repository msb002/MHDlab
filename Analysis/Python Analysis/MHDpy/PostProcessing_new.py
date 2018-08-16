# -*- coding: utf-8 -*-
"""
This program pulls data from the logging files to copy the 'control VI' files
"""

"""
This program pulls data from the logging files to copy the 'control VI' files
"""


import numpy as np
import time
import pandas as pd
import os
import sys
from nptdms import TdmsFile as TF
from nptdms import TdmsWriter, RootObject, GroupObject, ChannelObject
import datetime
import pytz

#Make sure Python Analysis folder in in PYTHONPATH and import the MHDpy module
PythonAnalysisPath = 'C:\\Users\\aspit\\Git\\MHDLab\\Python Analysis'
if not PythonAnalysisPath in sys.path:
    sys.path.append(PythonAnalysisPath)


def nearest_timeind(timearray, pivot):   
    diff = timearray - pivot
    seconds = np.array(list(map(lambda x: abs(x.total_seconds()),diff)))
    return seconds.argmin()

def combine_channels(Fileinfo,group,channel):
    combined = np.empty(0)
    for TDMSfile in Fileinfo['TDMSfile']:
        data = TDMSfile.channel_data(group,channel)
        combined = np.append(combined,data)
    return combined

def cut_tdms_file(filepath,timestamps,samplerate):
    if isinstance(filepath,bytes): #The labview addin passes a bytes instead of string. 
        filepath = filepath.decode("utf-8")

    Logfiletdms = TF(filepath)

    timedata = np.array(Logfiletdms.channel_data('Global','Time'))

    #time1 = timedata[10]
    #time2 = timedata[20]

    time1 = datetime.datetime.utcfromtimestamp(timestamps[0]).replace(tzinfo=pytz.UTC)
    time2 = datetime.datetime.utcfromtimestamp(timestamps[1]).replace(tzinfo=pytz.UTC)

    idx1 = nearest_timeind(timedata,time1)
    idx2 = nearest_timeind(timedata,time2)

    data = Logfiletdms.as_dataframe()

    data = data[idx1:idx2][:]

    f, ext = os.path.splitext(filepath)

    newfile = f + '_cut.tdms'

    root_object = RootObject(properties={
    "prop1": "foo",
    "prop2": 3,
    })
    group_object = GroupObject("group_1", properties={
        "prop1": 1.2345,
        "prop2": False,
    })
    
    
    channel_object = ChannelObject("group_1", "channel_1", data[:]["/'Data'/'Current_1'"], properties={})

    with TdmsWriter(newfile) as tdms_writer:
        tdms_writer.write_segment([
            root_object,
            group_object,
            channel_object])


DataPath = 'C:/Labview Test Data/2018-08-13/Sensors/Log_Sensors_DAQ_0.tdms'

Logfiletdms = TF(DataPath)

timedata = np.array(Logfiletdms.channel_data('Global','Time'))



timestamps = [1534213304, 1534213317]

time1 = datetime.datetime.utcfromtimestamp(timestamps[0]).replace(tzinfo=pytz.UTC)

time2 = datetime.datetime.utcfromtimestamp(timestamps[1]).replace(tzinfo=pytz.UTC)

data = cut_tdms_file(DataPath,timestamps,100)
