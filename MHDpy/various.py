# -*- coding: utf-8 -*-
"""
This program pulls data from the logging files to copy the 'control VI' files
"""

from __future__ import unicode_literals
import numpy as np
import time

import datetime
import pytz
import tzlocal


#time conversion.
def np64_to_utc(np64_dt):
    utc_dt = datetime.datetime.utcfromtimestamp(np64_to_unix(np64_dt)).replace(tzinfo=pytz.utc)
    return utc_dt

def np64_to_unix(timestamp):
    return (timestamp - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')

def datetime_to_unix(timestamp):
    return (timestamp - datetime.datetime(1970,1,1,tzinfo = pytz.utc)).total_seconds()

def labview_to_unix(timestamps):
    newtimestamps = list(map(lambda x: x -2082844800 ,timestamps))
    return newtimestamps

def nearest_timeind(timearray, pivot):
    diffs =   np.array(list(map(lambda x: abs(x - pivot),timearray))) 
    seconds = np.array(list(map(lambda x: x.total_seconds(),diffs)))
    return seconds.argmin()