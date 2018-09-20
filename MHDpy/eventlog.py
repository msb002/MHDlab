# -*- coding: utf-8 -*-
import json
import time
import pathlib
import datetime

def writeevent(Eventlogfile, event):
    eventnew = {}
    timestamp = time.time()
    eventnew['hrdt'] = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    eventnew['dt'] = timestamp
    eventnew['event'] = event

    with open(Eventlogfile, "r") as read_file:
        try:
            eventloglist = json.load(read_file)
        except ValueError: #Empty file
            eventloglist = []
    with open(Eventlogfile, "w") as write_file:
        eventloglist.append(eventnew)
        json.dump(eventloglist, write_file, indent=2) 

class Eventlog():
    def __init__(self,Eventlogfile):
        self.Eventlogfile = Eventlogfile
        if isinstance(self.Eventlogfile,bytes): #The labview addin passes a bytes instead of string. 
            self.Eventlogfile = self.Eventlogfile.decode("utf-8")


    def TestCaseInfoChange(self, TestDataInfo):
        for idx, string in  enumerate(TestDataInfo):
            TestDataInfo[idx] = string.decode("utf-8")

        with open(self.Eventlogfile,'r') as read_file:
            self.jsonfile = json.load(read_file)
        
        existing_tci_arr = []
        for event in self.jsonfile:
            if (event['event']['type'] == 'TestCaseInfoChange'):
                eventinfo = event['event']['event info']
                existing_tci_arr.append([eventinfo['project'],eventinfo['subfolder'],eventinfo['filename'],eventinfo['measurementnumber']])
                
        for existing_tci in existing_tci_arr:
            if(existing_tci == TestDataInfo).all():
                return False #Existing test case info
        
        project = TestDataInfo[0]
        subfolder = TestDataInfo[1]
        filename = TestDataInfo[2]
        measurementnumber = TestDataInfo[3]

        event = {
            "type" : "TestCaseInfoChange",
            "event info": {
                "project": project,
                "subfolder": subfolder,
                "filename": filename,
                "measurementnumber": measurementnumber 
                }
        }

        writeevent(self.Eventlogfile, event)

        return True #was no existing test case info

    def RunningVIsChange(self,VIname,OnOff):
        event = {
            "type" : "VIRunningChange",
            "event info": {
                "name" : VIname.decode("utf-8"),
                "newstate" : OnOff
                }
        }

        writeevent(self.Eventlogfile,event) 

    def SavingVIsChange(self, VIname,OnOff):
        event = {
            "type" : "VISavingChange",
            "event info": {
                "name" : VIname.decode("utf-8"),
                "newstate" : OnOff
                }
        }

        writeevent(self.Eventlogfile,event)

    def customevent(self, eventstr):
        eventstr = eventstr.decode("utf-8")
        event = {
            "type" : "CustomEvent",
            "event info": {
                "customeventstring" : eventstr
                }
        }

        writeevent(self.Eventlogfile,event)

