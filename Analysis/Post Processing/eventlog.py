# -*- coding: utf-8 -*-
import json
import time

Eventlogfile = ""

def writeevent(event):
    with open(Eventlogfile, "a") as write_file:
        write_file.write(',\n')
        json.dump(event, write_file)

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

    with open(Eventlogfile,'r') as read_file:
        contents = read_file.read()

    with open(Eventlogfile,'a') as write_file:
        if(len(contents) > 0):
            if(contents[-1] == ']'):
                length = write_file.seek(0,2)
                write_file.seek(length-2)
                write_file.truncate()
                write_file.write(',\n')
        else:
            write_file.write('[\n')
        json.dump(event, write_file)

def shutdown():
    event = {
    "dt": time.time(),
    "event": {
        "type" : "MonitorVIClosed"
    } 
    }

    writeevent(event)

    with open(Eventlogfile,'a') as write_file:
        write_file.write('\n]')




def TestCaseInfoChange(TestDataInfo):
    for idx, string in  enumerate(TestDataInfo):
        TestDataInfo[idx] = string.decode("utf-8")

    # with open(Eventlogfile,'r') as read_file:
    #     contents = read_file.read()

    # print(contents)

    # existing_tci_arr = []
    # for event in contents:
    #     if event['event']['type'] == 'TestCaseInfoChange':
    #         eventinfo = event['event']['event info']
    #         existing_tci_arr.append([eventinfo['project'],eventinfo['subfolder'],eventinfo['filename'],eventinfo['measurementnumber']])
            
    # for existing_tci in existing_tci_arr:
    #     if(existing_tci == TestDataInfo):
    #         return 0
    
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

    return 1


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