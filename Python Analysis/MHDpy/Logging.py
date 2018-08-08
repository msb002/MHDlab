# -*- coding: utf-8 -*-
"""
This program pulls data from the logging files to copy the 'control VI' files
"""


import numpy as np


from nptdms import TdmsFile as TF
from nptdms import TdmsWriter, RootObject, GroupObject, ChannelObject

import pandas as pd

import os
import sys

from nptdms import TdmsWriter, RootObject, GroupObject, ChannelObject

def nearest_ind(items, pivot):
    time_diff = np.abs([date - pivot for date in items])
    return time_diff.argmin(0)


#Make sure Python Analysis folder in in PYTHONPATH and import the MHDpy module
PythonAnalysisPath = 'C:\\Users\\aspit\\Git\\MHDLab\\Python Analysis'
if not PythonAnalysisPath in sys.path:
    sys.path.append(PythonAnalysisPath)

from nptdms import TdmsFile as TF

samplerate = 100


DataPath = 'C:/Labview Test Data/2018-08-08'

os.chdir(DataPath)

Logfiles = []
ProjectFolders = []
for (dirpath, dirnames, filenames) in os.walk(DataPath):
    for f in filenames:
        f, ext = os.path.splitext(f)
        suffixstr = "_Log"
        if(ext == '.tdms'):
            f = f[:len(f)-len(suffixstr)]
            Logfiles.extend([f])
    ProjectFolders.extend(dirnames)
    break


Fileinfo = []
for Project in ProjectFolders:
    for dirpath,_,filenames in os.walk(os.path.join(DataPath, Project)):
        for f in filenames:
            fname, ext = os.path.splitext(f)
            prefixstr = "Control"
            if(fname.startswith(prefixstr) and ext == '.tdms'):
                path = os.path.join(dirpath,f)
                controltdms = TF(os.path.join(dirpath,f))
                timedata = controltdms.channel_data('Global', 'Time')
                suf = fname[len(prefixstr):]
                Fileinfo.append((suf,dirpath,timedata))

Fileinfo = pd.DataFrame(Fileinfo, columns = ['suffix','folder','time'])






root_object = RootObject()
group_object = GroupObject("group_1", properties={
    "prop1": 1.2345,
    "prop2": False,
})
data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
channel_object = ChannelObject("group_1", "channel_1", data, properties={})



i = 0
for Logfile in Logfiles:
    Logfiletdms = TF(os.path.join(DataPath,Logfile + '_Log.tdms'))
    Logfiledf = Logfiletdms.as_dataframe()
    Logfiletime = Logfiletdms.channel_data('Time','Time')
    for Fileinforow in Fileinfo.iterrows():
        mintimeidx = nearest_ind(Logfiletime,Fileinforow[1]['time'][0])
        maxtimeidx = nearest_ind(Logfiletime,Fileinforow[1]['time'][-1])
        
        
        
        newfile = os.path.join(Fileinforow[1]['folder'], Logfile + Fileinforow[1]['suffix'] + '.tdms')
        with TdmsWriter(newfile) as tdms_writer:
            tdms_writer.write_segment([
                root_object,
                group_object,
                channel_object])

