# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import numpy as np


from nptdms import TdmsFile as TF
from nptdms import TdmsWriter, RootObject, GroupObject, ChannelObject

import pandas as pd

import os
import sys

#Make sure Python Analysis folder in in PYTHONPATH and import the MHDpy module
PythonAnalysisPath = 'C:\\Users\\aspit\\Git\\MHDLab\\Python Analysis'
if not PythonAnalysisPath in sys.path:
    sys.path.append(PythonAnalysisPath)

from nptdms import TdmsFile as TF

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



Filesuffix = []
Filepaths = []
for Project in ProjectFolders:
    for dirpath,_,filenames in os.walk(os.path.join(DataPath, Project)):
        for f in filenames:
            #print(os.path.abspath(os.path.join(dirpath, f)))
            f, ext = os.path.splitext(f)
            prefixstr = "Control"
            if(f.startswith(prefixstr) and ext == '.tdms'):
                f = f[len(prefixstr):]
                Filesuffix = np.append(Filesuffix,f)
                Filepaths = np.append(Filepaths,dirpath)





from nptdms import TdmsWriter, RootObject, GroupObject, ChannelObject

root_object = RootObject(properties={
    "prop1": "foo",
    "prop2": 3,
})
group_object = GroupObject("group_1", properties={
    "prop1": 1.2345,
    "prop2": False,
})
data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
channel_object = ChannelObject("group_1", "channel_1", data, properties={})



i = 0
for Logfile in Logfiles:
    for i in range(len(Filepaths)):
        newfile = os.path.join(Filepaths[i], Logfile + Filesuffix[i] + '.tdms')
        with TdmsWriter(newfile) as tdms_writer:
            tdms_writer.write_segment([
                root_object,
                group_object,
                channel_object])