# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import spe2py as spe
import spe_loader as sl

import numpy as np

import matplotlib.pyplot as plt
from nptdms import TdmsFile as TF
from nptdms import TdmsWriter, RootObject, GroupObject, ChannelObject

import os


#loaded_files = spe.load()

##spectrum test

#folder = 'C:/Users/aspit/OneDrive/Data/'
#file = 'Test' 

#spe_file = sl.load_from_files([folder + file + '.spe'])

def SPEtoTDMS_seq_spectra(spefilepath):
    
    folder = os.path.splitext(os.path.dirname(spefilepath))[0]
    base = os.path.splitext(os.path.basename(spefilepath))[0]
    
    tdmsfilepath = folder + "/" +base + ".tdms"
    
    spe_file = sl.load_from_files([spefilepath])

    frames  = spe_file.data
    
    wavelength = spe_file.wavelength
    
    num_frames = spe_file.nframes
    
    
    #starting_gate = spe_file.footer.SpeFormat.Calibrations.SensorInformation['height']
    
    Gatinginfo = spe_file.footer.SpeFormat.DataHistories.DataHistory.Origin.Experiment.Devices.Cameras.Camera.Gating.Sequential
    
    start_gatedelay = int(Gatinginfo.StartingGate.Pulse['delay'])
    end_gatedelay = int(Gatinginfo.EndingGate.Pulse['delay'])
    
    gatedelays = np.linspace(start_gatedelay, end_gatedelay, num_frames)
    
    
    root_object = RootObject(properties={
        "prop1": "foo",
    })
    
    rawdata_group_object = GroupObject("Raw Data", properties={
    })
    
    common_group_object = GroupObject("Common", properties={
    })
    
    framenum = 0
    
    
    
    with TdmsWriter(tdmsfilepath) as tdms_writer:   
        channel_object = ChannelObject("Common", "Gate Delays" ,gatedelays, properties={})
        tdms_writer.write_segment([root_object,common_group_object,channel_object])
    
        for frame in frames:
            channel_object = ChannelObject("Raw Data", "Frame" + str(framenum), frame[0][0], properties={})
            tdms_writer.write_segment([root_object,rawdata_group_object,channel_object])
            framenum = framenum +1
    
    
def SPEtoTDMS_seq_image(spefilepath):
    
    folder = os.path.splitext(os.path.dirname(spefilepath))[0]
    base = os.path.splitext(os.path.basename(spefilepath))[0]
    
    tdmsfilepath = folder + "/" +base + ".tdms"
    
    spe_file = sl.load_from_files([spefilepath])

    frames  = spe_file.data
    
    num_frames = spe_file.nframes
    
    
    #starting_gate = spe_file.footer.SpeFormat.Calibrations.SensorInformation['height']
    
    Gatinginfo = spe_file.footer.SpeFormat.DataHistories.DataHistory.Origin.Experiment.Devices.Cameras.Camera.Gating.Sequential
    
    start_gatedelay = int(Gatinginfo.StartingGate.Pulse['delay'])
    end_gatedelay = int(Gatinginfo.EndingGate.Pulse['delay'])
    
    gatedelays = np.linspace(start_gatedelay, end_gatedelay, num_frames)
    
    
    root_object = RootObject(properties={
        "prop1": "foo",
    })
    

    
    common_group_object = GroupObject("Common", properties={
    })
    
    framenum = 0
    
    
    
    
    with TdmsWriter(tdmsfilepath) as tdms_writer:
        channel_object = ChannelObject("Common", "Gate Delays" ,gatedelays, properties={})
        tdms_writer.write_segment([root_object,common_group_object,channel_object])
        for frame in frames:      
            rawdata_group_object = GroupObject("Frame" + str(framenum), properties={}) 
            linenum = 0
            for line in frame[0]:
                channel_object = ChannelObject("Frame" + str(framenum), "line" + str(linenum) , line, properties={})
                tdms_writer.write_segment([root_object,rawdata_group_object,channel_object])
                linenum = linenum +1
            framenum = framenum +1    

#spefilepath = 'C:/Users/aspit/OneDrive/Data/Test.spe'
#SPEtoTDMS_seq_spectra(spefilepath)

##image test
            
spefilepath = 'C:/Users/aspit/OneDrive/Data/Testimage.spe'
SPEtoTDMS_seq_image(spefilepath)
    
#spe_image = sl.load_from_files(['C:/Users/aspitarl/OneDrive/Data/TestImage.spe'])   


#spe_tools = spe.load()
#spe_tools.image()  # images the first frame and region of interest