# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import spe2py as spe
import spe_loader as sl

import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams.update({'font.size': 18})



from nptdms import TdmsFile as TF
from nptdms import TdmsWriter, RootObject, GroupObject, ChannelObject

import pandas as pd

import os
import sys

#Make sure Python Analysis folder in in PYTHONPATH and import the MHDpy module
PythonAnalysisPath = 'C:\\Users\\aspit\\Git\\MHDLab\\Python Analysis'
if not PythonAnalysisPath in sys.path:
    sys.path.append(PythonAnalysisPath)

import MHDpy.importing

from nptdms import TdmsFile as TF


def get_gatedelays(spe_file):
    num_frames = spe_file.nframes
    
    Gatinginfo = spe_file.footer.SpeFormat.DataHistories.DataHistory.Origin.Experiment.Devices.Cameras.Camera.Gating.Sequential
    
    start_gatedelay = int(Gatinginfo.StartingGate.Pulse['delay'])
    end_gatedelay = int(Gatinginfo.EndingGate.Pulse['delay'])
    
    gatedelays = np.linspace(start_gatedelay, end_gatedelay, num_frames)

    return gatedelays

def SPE2df_seq_spect(spefilepath):
    spe_file = sl.load_from_files([spefilepath])

    frames  = spe_file.data
    gatedelays = get_gatedelays(spe_file)
    wavelength = spe_file.wavelength
    
    datamatrix = np.zeros((len(wavelength),len(gatedelays)))
    
    i = 0
    for frame in frames:
        datamatrix[:,i] = frame[0]
        i = i+1
        
    spectraldf = pd.DataFrame(datamatrix, index = wavelength, columns = gatedelays)    
    
    return spectraldf


            
def SPEtoTDMS_seq(spefilepath,meastype):
    if isinstance(spefilepath,bytes): #The labview addin passes a bytes instead of string. 
        spefilepath = spefilepath.decode("utf-8")
    
    folder = os.path.splitext(os.path.dirname(spefilepath))[0]
    base = os.path.splitext(os.path.basename(spefilepath))[0]
    tdmsfilepath = os.path.join(folder,base + ".tdms")

    spe_file = sl.load_from_files([spefilepath])

    frames  = spe_file.data   
    gatedelays = get_gatedelays(spe_file)
    
    root_object = RootObject(properties={})    
    common_group_object = GroupObject("Common", properties={})
    
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
    
    
def getlaserdata():
    pathnames_laser= MHDpy.importing.get_pathnames("C:\\Users\\aspit\\OneDrive\\Data\\LaserProfile")
    file_laser = TF(pathnames_laser['Test1_20Hz.tdms'])
    
    
    laser_common = file_laser.object('Raw').as_dataframe()
    laser_data = file_laser.object('Average').as_dataframe()
    
    
    laser_time = laser_common['Time1']
    laser_data = laser_data['Mean']
    laser_data_norm = laser_data/laser_data.max()
    #offset_time = 870
    offset_time = 35
    laser_time_off = laser_time - offset_time
    
    laserseries = pd.Series(laser_data_norm.values, index = laser_time_off)
    
    return laserseries
    

def cutSpectraldf(spectraldf, wl1 = None,wl2 = None):
    
        if wl1 == None:
            wl1 = spectraldf.index.min()
        if wl2 == None:
            wl2 = spectraldf.index.max()
        wavelength = spectraldf.index

        idx1 = wavelength.get_loc(wl1, method = 'nearest')
        idx2 = wavelength.get_loc(wl2, method = 'nearest')
        
        wavelength_cut = wavelength[idx1:idx2]
        spectra_cut = spectraldf.iloc[idx1:idx2]
        
        return wavelength_cut, spectra_cut

def maxandarea(wavelength_cut, spectra_cut):
    areas = pd.Series(index = spectra_cut.columns)
    maximums = pd.Series(index = spectra_cut.columns)
    
    for gatedelay in spectra_cut.columns:
        areas[gatedelay] = np.trapz(spectra_cut[gatedelay],wavelength_cut)
        maximums[gatedelay] = spectra_cut[gatedelay].max()      
        
    return areas, maximums

def fitdecay(spectraldf, wl1 = None, wl2 = None, wl1_fit = None, wl2_fit = None):
    wavelength_cut, spectra_cut = cutSpectraldf(spectraldf,wl1,wl2)

    areas, maximums = maxandarea(wavelength_cut, spectra_cut)
    
    if wl1_fit == None:
        wl1_fit = maximums.index.min()
    if wl2_fit == None:
        wl2_fit = maximums.index.max()
    
    idx1 = maximums.index.get_loc(wl1_fit, method = 'nearest')
    idx2 = maximums.index.get_loc(wl2_fit, method = 'nearest')
    
    gatedelays = maximums.index[idx1:idx2]
    maximums = np.log(maximums.iloc[idx1:idx2])
    
    gatedelays
    maximums
    
    fitcoef = np.polyfit(gatedelays,maximums,1)
    
    gatedelays_fit = np.linspace(gatedelays.min(),gatedelays.max(),100)
    fit = fitcoef[1] + fitcoef[0]*gatedelays_fit
    
    fit = np.exp(fit)
    
    return fit, gatedelays_fit, fitcoef


class SpectraPlot():
    
    def __init__(self,spectra,wavelength):
        self.fig, self.ax1 = plt.subplots(figsize = (8,6))
        self.ax1.plot(wavelength,spectra)
        self.ax1.set_xlabel("Wavelength (nm)")
        self.ax1.set_ylabel("Intensity (a.u.)")

    
class PLplot_new():
    
    def __init__(self, laserseries):
        self.laserseries = laserseries
        
        self.fig, self.ax1 = plt.subplots(figsize = (8,6))
        
        self.ax1.set_xlabel("Gate Delay (ns)")
        self.ax1.set_ylabel("$Delta$ PL Intensity (Normalized)")
        self.ax1.tick_params('y')
        
        self.ax2 = self.ax1.twinx()
        
        self.ax2.set_ylabel("Laser Intensity (Normalized)")
        self.ax2.tick_params('y')
        
        self.laserline = self.ax2.plot(self.laserseries.index, self.laserseries, '--', color = 'gray', label = 'Laser profile')
        
        self.ax2.set_yscale('log')
        self.ax1.set_yscale('log')
        
        self.lns = self.laserline
        
        self.setlegend()
        
        
        self.fig.suptitle('PL Plot', y = 1)
        self.fig.tight_layout()
        
    def add_decay(self,spectraldf, label,method = "max", wl1 = None ,wl2 = None, color = None):
        


        wavelength_cut, spectra_cut = cutSpectraldf(spectraldf, wl1,wl2)
        
        areas, maximums = maxandarea(wavelength_cut, spectra_cut)
        
        if color == None:
            colorlist = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
            color = colorlist[len(self.lns)]
            
        if method == "max":
            ln = self.ax1.plot(spectra_cut.columns, maximums, '.-', color = color , label = label)    
        elif method == "area":
            ln = self.ax1.plot(spectra_cut.columns, areas, '.-', color = color , label = label)    
        
        self.lns = self.lns + ln
        
        self.legend.remove()
        self.setlegend()
        #self.legend.remove()
        #self.legend(self.lns)
        

    def setlegend(self):
        labs = [l.get_label() for l in self.lns]
        self.legend = self.ax1.legend(self.lns, labs, loc=0)
        #self.ax1.legend(self.lns,labs)
        
        
        
        # Make the y-axis label, ticks and tick labels match the line color.


    #TRPL lifetime pseudo code
    # inputs: SPE TRPL sequence, powermeter tdms file, SPE file of camera 2 sequence (laser timing)
    # parse SPE file to obtain spectra dataframe
    # normalize the dataframe to power 
    # plot the time decay along with the power meter and laser timing to make sure that there is steady state
    # Use time sequence to parse the power meter file
    
    # make this a modular funciton so that the code can be used to parse series of test cases
    # returns fitparameters
    
   