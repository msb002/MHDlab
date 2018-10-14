# -*- coding: utf-8 -*-

import os
import nptdms

def create_tcdict(filepaths, loadfn, prefix = None ):
    """takes in a list of files and a lod function, and creates a dict of a df for each file. If a prefix is passed, that is removed from the filename (typically the instrument name so only the test case is left as the dict key)"""

    dfs = {}

    for filepath in filepaths:
        filename = os.path.split(filepath)[1]
        testcase = os.path.splitext(filename)[0]

        if prefix != None:
            testcase = _remove_prefix(testcase,prefix)

        df =  loadfn(filepath)
        dfs[testcase] =df
    
    return dfs

def tdms2df(filepath):
    tdmsfile = nptdms.TdmsFile(filepath)
    df = tdmsfile.as_dataframe()

    #test if a waveform channel
    channel1 = tdmsfile.group_channels(tdmsfile.groups()[0])[0]
    waveform = True
    try:
        channel1.time_track()
    except KeyError:
        waveform = False
    #find the longest waveform
    if waveform:
        longestchannel = None
        length = 0
        for group in tdmsfile.groups():
            for channel in tdmsfile.group_channels(group):
                newlength = len(channel.data)
                if newlength > length:
                    length = newlength
                    longestchannel = channel
        timedata = longestchannel.time_track(absolute_time = True) 
        df = df.set_index(timedata)

    return df


def _remove_prefix(s, prefix):
    return s[len(prefix):] if s.startswith(prefix) else s