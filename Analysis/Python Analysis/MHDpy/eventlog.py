# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import json

Eventlogfile = ""

def fixeventlogfile():
    global Eventlogfile
    if isinstance(Eventlogfile,bytes): #The labview addin passes a bytes instead of string. 
        Eventlogfile = Eventlogfile.decode("utf-8")


def TestCaseInfoChange(TestDataInfo, time):
    for idx, string in  enumerate(TestDataInfo):
        TestDataInfo[idx] = string.decode("utf-8")
    
    project = TestDataInfo[0]
    subfolder = TestDataInfo[1]
    filename = TestDataInfo[2]
    measurementnumber = TestDataInfo[3]

    event = {
    "dt": time,
    "event": {
        "TestCaseInfoChange": {
            "project": project,
            "subfolder": subfolder,
            "filename": filename,
            "measurementnumber": measurementnumber 
            }
        }
    }

    print(event)

    with open(Eventlogfile, "a") as write_file:
        json.dump(event, write_file)
        write_file.write('\n')