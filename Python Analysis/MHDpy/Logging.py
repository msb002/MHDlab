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
    Logfiles.extend(filenames)
    ProjectFolders.extend(dirnames)
    break



Files = []
Folders = []
for Project in ProjectFolders:
    for dirpath,_,filenames in os.walk(os.path.join(DataPath, Project)):
        for f in filenames:
            #print(os.path.abspath(os.path.join(dirpath, f)))
            Files = np.append(Files,f)
            Folders = np.append(Folders,dirpath)


DataFiles = pd.Series(Folders, index = Files)

print(DataFiles)
