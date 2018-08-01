# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 12:15:03 2018

@author: aspit
"""

import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta as td
import pandas as pd
import sys
#Make sure Python Analysis folder in in PYTHONPATH and import the MHDpy module
PythonAnalysisPath = 'C:\\Users\\aspit\\Documents\\Git\\MHDLab\\Python Analysis'
if not PythonAnalysisPath in sys.path:
    sys.path.append(PythonAnalysisPath)
    
import MHDpy.importing
import MHDpy.plotting
import MHDpy.analysis
import MHDpy.SPEparse
from nptdms import TdmsFile as TF

import importlib

mpl.rcParams.update({'font.size': 18})
    