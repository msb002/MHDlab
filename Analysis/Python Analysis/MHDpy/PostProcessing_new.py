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

    data = data[idx1*samplerate:idx2*samplerate][:]

    f, ext = os.path.splitext(filepath)

    newfile = f + '_cut.tdms'

    root_object = RootObject(properties={
    "prop1": "foo",
    "prop2": 3,
    })


    with TdmsWriter(newfile) as tdms_writer:
        channel_object = ChannelObject('Global', 'Time', timedata[idx1:idx2], properties={})
        
        tdms_writer.write_segment([
            root_object,
            channel_object])

        for channelstr in data.columns:
            strsplit = channelstr.split('/')
            group = strsplit[1].replace("\'","")
            channel = strsplit[2].replace("\'","")
            if(group == 'Data'):
                channel_object = ChannelObject('Data' , channel, data[channelstr].as_matrix(), properties={})
                tdms_writer.write_segment([
                    root_object,
                    channel_object])


    
    




# DataPath = 'C:/Labview Test Data/2018-08-13/Sensors/Log_Sensors_DAQ_0.tdms'

# Logfiletdms = TF(DataPath)

# timedata = np.array(Logfiletdms.channel_data('Global','Time'))



# timestamps = [1534213306, 1534213315]

# time1 = datetime.datetime.utcfromtimestamp(timestamps[0]).replace(tzinfo=pytz.UTC)

# time2 = datetime.datetime.utcfromtimestamp(timestamps[1]).replace(tzinfo=pytz.UTC)

# data = cut_tdms_file(DataPath,timestamps,100)