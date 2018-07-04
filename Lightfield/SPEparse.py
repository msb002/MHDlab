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


            
def SPEtoTDMS_seq(spefilepath,meastype):
    if isinstance(spefilepath,bytes): #The labview addin passes a bytes instead of string. 
        spefilepath = spefilepath.decode("utf-8")
    
    folder = os.path.splitext(os.path.dirname(spefilepath))[0]
    base = os.path.splitext(os.path.basename(spefilepath))[0]

    tdmsfilepath = os.path.join(folder,base + ".tdms")
    spe_file = sl.load_from_files([spefilepath])

    frames  = spe_file.data
    
    num_frames = spe_file.nframes
    
    Gatinginfo = spe_file.footer.SpeFormat.DataHistories.DataHistory.Origin.Experiment.Devices.Cameras.Camera.Gating.Sequential
    
    start_gatedelay = int(Gatinginfo.StartingGate.Pulse['delay'])
    end_gatedelay = int(Gatinginfo.EndingGate.Pulse['delay'])
    
    gatedelays = np.linspace(start_gatedelay, end_gatedelay, num_frames)
    
    
    root_object = RootObject(properties={
        "prop1": "foo",
    })
    
    common_group_object = GroupObject("Common", properties={
    })
    
    with TdmsWriter(tdmsfilepath) as tdms_writer:   
        channel_object = ChannelObject("Common", "Gate Delays" ,gatedelays, properties={})
        tdms_writer.write_segment([root_object,common_group_object,channel_object])
    
    if(meastype == 0): 
        wavelength = spe_file.wavelength
        with TdmsWriter(tdmsfilepath, mode = 'a') as tdms_writer: 
            channel_object = ChannelObject("Common", "Wavelength" ,wavelength, properties={})
            tdms_writer.write_segment([root_object,common_group_object,channel_object])   
        write_spectra(tdmsfilepath, root_object, frames,wavelength )
    if(meastype == 1):
        write_image(tdmsfilepath, root_object, frames )
    
def write_image(tdmsfilepath, root_object, frames ):
    framenum = 0
    
    with TdmsWriter(tdmsfilepath, mode = 'a') as tdms_writer:
        for frame in frames:
            rawdata_group_object = GroupObject("Frame" + str(framenum), properties={}) 
            linenum = 0
            for line in frame[0]:
                channel_object = ChannelObject("Frame" + str(framenum), "line" + str(linenum) , line, properties={})
                tdms_writer.write_segment([root_object,rawdata_group_object,channel_object])
                linenum = linenum +1
            framenum = framenum +1   
            
def write_spectra(tdmsfilepath, root_object, frames, wavelength ):
    framenum = 0
    
    rawdata_group_object = GroupObject("Raw Data", properties={
    })
    
    with TdmsWriter(tdmsfilepath, mode = 'a') as tdms_writer:   
        for frame in frames:
            channel_object = ChannelObject("Raw Data", "Frame" + str(framenum), frame[0][0], properties={})
            tdms_writer.write_segment([root_object,rawdata_group_object,channel_object])
            framenum = framenum +1
    
    
spefilepath = "C:/Users/aspit/Documents/TestData/Testimage.spe"
SPEtoTDMS_seq(spefilepath,1)
#SPEtoTDMS_seq_spectra(spefilepath)

##image test
            
#spefilepath = 'C:\\Users\\aspitarl\\OneDrive\\Data\\Testimage.spe'
#SPEtoTDMS_seq_image(spefilepath)
    
#spe_image = sl.load_from_files(['C:/Users/aspitarl/OneDrive/Data/TestImage.spe'])   


#spe_tools = spe.load()
#spe_tools.image()  # images the first frame and region of interest