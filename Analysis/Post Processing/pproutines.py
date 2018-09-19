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

import various


def cut_log_file(fileinpath, fileoutpath, time1, time2):
    tdmsfile = TF(fileinpath)
    direc = os.path.split(fileoutpath)[0]
    if not os.path.exists(direc):
        os.makedirs(direc)

    root_object = RootObject(properties={ #TODO root properties
    })

    timearray = None
    delete = False
    with TdmsWriter(fileoutpath,mode='w') as tdms_writer:
        for group in tdmsfile.groups():
            channels = tdmsfile.group_channels(group)
            for channel in channels:

                if (timearray != channel.time_track(absolute_time = True)).all():
                    timearray = channel.time_track(absolute_time = True)
                    timedata = list(map(lambda x: various.np64_to_utc(x),timearray))

                if(time2 > time1):
                    idx1 = various.nearest_timeind(timedata,time1)
                    idx2 = various.nearest_timeind(timedata,time2)
                else:
                    idx2 = various.nearest_timeind(timedata,time1)
                    idx1 = various.nearest_timeind(timedata,time2)

                if(idx1 == idx2): #times are not within file
                    print('times not in file ' + tdmsfile.object().properties['name'])
                    delete = True
                    break

                props = channel.properties
                start= props['wf_start_time']
                offset = datetime.timedelta(milliseconds = props['wf_increment']*1000*idx1)
                props['wf_start_time'] = start + offset

                channel_object = ChannelObject(group, channel.channel, channel.data[idx1:idx2], properties=props)
                tdms_writer.write_segment([
                    root_object,
                    channel_object])

    if delete:
        os.remove(fileoutpath)

