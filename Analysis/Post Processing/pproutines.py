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

import layout



def parse_tdms_file(self, internalfile):
    #parse a file based on the seleted times, internal or external
    folder = self.folderEdit.text()
    filename = self.filenameEdit.text()

    if(internalfile):
        filepath = os.path.join(self.datefolder, folder, filename)
        filepath =   filepath + '.tdms'
        cut_tdms_file(self.time1,self.time2,filepath,self.Logfiletdms)
    else:
        paths = QtWidgets.QFileDialog.getOpenFileName(MainWindow, 'Open File', 'C:\\Labview Test Data')
        filepathext = paths[0]
        tdmsfile = TF(filepathext)
        origfilename = os.path.splitext(os.path.split(filepathext)[1])[0]
        filepath = os.path.join(self.datefolder, folder, origfilename)
        filepath =   filepath + '.tdms'
        cut_tdms_file(self.time1,self.time2,filepath,tdmsfile)

def parse_tdms_eventlog(self):
    #parse internal tdms file based on the test case info array
    self.tci = self.gettestcaseinfo()
    tci = []
    times = []
    i=0
    for event in self.jsonfile:
        if event['event']['type'] == 'TestCaseInfoChange':
            time = datetime.datetime.utcfromtimestamp(event['dt'])
            time = time.replace(tzinfo=pytz.utc)
            times.append(time)
            tci.append(event['event']['event info'])
    i=0
    for i in range(len(times)-1):
        folder = tci[i]['project'] + '\\'+ tci[i]['subfolder']
        filename = self.origfilename + '_' + tci[i]['filename'] + '_'+ tci[i]['measurementnumber'] + '_cut'
        filepath = os.path.join(self.datefolder, folder, filename)
        filepath =   filepath + '.tdms'
        cut_tdms_file(times[i],times[i+1],filepath,self.Logfiletdms)

def hello(string):
    print('hello' , string)
