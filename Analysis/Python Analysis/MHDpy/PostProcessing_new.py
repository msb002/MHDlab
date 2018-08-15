# -*- coding: utf-8 -*-
"""
This program pulls data from the logging files to copy the 'control VI' files
"""

"""
This program pulls data from the logging files to copy the 'control VI' files
"""


import numpy as np
from nptdms import TdmsFile as TF
import time
import pandas as pd
import os
import sys
from nptdms import TdmsWriter, RootObject, GroupObject, ChannelObject
import datetime
import pytz

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




#Make sure Python Analysis folder in in PYTHONPATH and import the MHDpy module
PythonAnalysisPath = 'C:\\Users\\aspit\\Git\\MHDLab\\Python Analysis'
if not PythonAnalysisPath in sys.path:
    sys.path.append(PythonAnalysisPath)


samplerate = 100

DataPath = 'C:/Labview Test Data/2018-08-13/Sensors'
os.chdir(DataPath)

Fileinfo = []

for (dirpath, dirnames, filenames) in os.walk(DataPath):
    for f in filenames:
        f, ext = os.path.splitext(f)
        suffixstr = "_Log"
        if(ext == '.tdms'):
            Logfiletdms = TF(os.path.join(dirpath,f+ext))
            Fileinfo.append((f,Logfiletdms))
    break


Fileinfo = pd.DataFrame(Fileinfo, columns = ['filename','TDMSfile'])

timedata = combine_channels(Fileinfo,'Global','Time')

time1 = datetime.datetime(2018, 8, 14, 2, 21, 45,tzinfo=pytz.timezone('UTC'))
time2 = datetime.datetime(2018, 8, 14, 4, 34, 20,tzinfo=pytz.timezone('UTC'))

idx1 = nearest_timeind(timedata,time2)

#time.strptime()