# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import json
import time

Eventlogfile = ""

def writeevent(event):
    with open(Eventlogfile, "a") as write_file:
        json.dump(event, write_file)
        write_file.write('\n')

def initialize():
    global Eventlogfile
    if isinstance(Eventlogfile,bytes): #The labview addin passes a bytes instead of string. 
        Eventlogfile = Eventlogfile.decode("utf-8")

    event = {
    "dt": time.time(),
    "event": {
        "type" : "MonitorVIStarted"
    } 
    }

    writeevent(event)



def shutdown():
    event = {
    "dt": time.time(),
    "event": {
        "type" : "MonitorVIClosed"
    } 
    }

    writeevent(event)


def TestCaseInfoChange(TestDataInfo):
    for idx, string in  enumerate(TestDataInfo):
        TestDataInfo[idx] = string.decode("utf-8")
    
    project = TestDataInfo[0]
    subfolder = TestDataInfo[1]
    filename = TestDataInfo[2]
    measurementnumber = TestDataInfo[3]

    event = {
    "dt": time.time(),
    "event": {
        "type" : "TestCaseInfoChange",
        "event info": {
            "project": project,
            "subfolder": subfolder,
            "filename": filename,
            "measurementnumber": measurementnumber 
            }
        }
    }

    writeevent(event)


def RunningVIsChange(VIname,OnOff):
    event = {
    "dt": time.time(),
    "event": {
        "type" : "VIRunningChange",
        "event info": {
            "name" : VIname.decode("utf-8"),
            "newstate" : OnOff
            }
        }
    }

    writeevent(event)


def SavingVIsChange(VIname,OnOff):
    event = {
    "dt": time.time(),
    "event": {
        "type" : "VISavingChange",
        "event info": {
            "name" : VIname.decode("utf-8"),
            "newstate" : OnOff
            }
        }
    }

    writeevent(event)