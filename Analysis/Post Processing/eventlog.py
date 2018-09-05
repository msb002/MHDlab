# -*- coding: utf-8 -*-
import json
import time

#Eventlogfile = ""

def writeevent(Eventlogfile, event):
    with open(Eventlogfile, "a") as write_file:
        write_file.write(',\n')
        json.dump(event, write_file)


class Eventlog():
    def __init__(self,Eventlogfile):
        #global Eventlogfile
        self.Eventlogfile = Eventlogfile
        if isinstance(self.Eventlogfile,bytes): #The labview addin passes a bytes instead of string. 
            self.Eventlogfile = self.Eventlogfile.decode("utf-8")

        event = {
        "dt": time.time(),
        "event": {
            "type" : "MonitorVIStarted"
        } 
        }

        with open(self.Eventlogfile) as fp:
            self.jsonfile = json.load(fp)

        with open(self.Eventlogfile,'r') as read_file:
            contents = read_file.read()

        with open(self.Eventlogfile,'a') as write_file:
            if(len(contents) > 0):
                if(contents[-1] == ']'):
                    length = write_file.seek(0,2)
                    write_file.seek(length-2)
                    write_file.truncate()
                    write_file.write(',\n')
            else:
                write_file.write('[\n')
            json.dump(event, write_file)  

    def shutdown(self):
        event = {
        "dt": time.time(),
        "event": {
            "type" : "MonitorVIClosed"
        } 
        }

        writeevent(self.Eventlogfile, event)

        with open(self.Eventlogfile,'a') as write_file:
            write_file.write('\n]')


    def TestCaseInfoChange(self, TestDataInfo):
        for idx, string in  enumerate(TestDataInfo):
            TestDataInfo[idx] = string.decode("utf-8")


        existing_tci_arr = []
        for event in self.jsonfile:
            if (event['event']['type'] == 'TestCaseInfoChange'):
                eventinfo = event['event']['event info']
                existing_tci_arr.append([eventinfo['project'],eventinfo['subfolder'],eventinfo['filename'],eventinfo['measurementnumber']])
                
        for existing_tci in existing_tci_arr:
            if(existing_tci == TestDataInfo).all():
                return False
        
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

        writeevent(self.Eventlogfile, event)

        return True


    def RunningVIsChange(self,VIname,OnOff):
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

        writeevent(self.Eventlogfile,event)


    def SavingVIsChange(self, VIname,OnOff):
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

        writeevent(self.Eventlogfile,event)