# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from nptdms import TdmsFile as TF
from nptdms import TdmsWriter, RootObject, GroupObject, ChannelObject
#import spe2py as spe
import spe_loader as sl
import pandas as pd
import os
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from dateutil import parser
import datetime

mpl.rcParams.update({'font.size': 18})

def get_gatedelays(spe_file):
    #pull a gate delay array a sequential SPE file. 
    num_frames = spe_file.nframes
    
    Gatinginfo = spe_file.footer.SpeFormat.DataHistories.DataHistory.Origin.Experiment.Devices.Cameras.Camera.Gating.Sequential
    
    start_gatedelay = int(Gatinginfo.StartingGate.Pulse['delay'])
    end_gatedelay = int(Gatinginfo.EndingGate.Pulse['delay'])
    
    gatedelays = np.linspace(start_gatedelay, end_gatedelay, num_frames)

    return gatedelays

def get_starttimes(spe_file):
    #pulls an array of exposure start times for each file
    abstimestr = spe_file.footer.SpeFormat.MetaFormat.MetaBlock.TimeStamp[0]['absoluteTime']
    abstime = parser.parse(abstimestr)
    timestamp_idx = spe_file.metanames.index('ExposureStarted')
    starttimestamps = np.array(list(map( lambda x: x[timestamp_idx], spe_file.metadata)))
    res = int(spe_file.footer.SpeFormat.MetaFormat.MetaBlock.TimeStamp[0]['resolution'])
    starttimestamps = starttimestamps/res
    starttimedeltas = list(map(lambda x:datetime.timedelta(seconds = x),starttimestamps))
    starttimes = [abstime + starttime for starttime in starttimedeltas] 
    starttimes = [time.timestamp() for time in starttimes]
    return starttimes


    




def SPE2df_seq_spect(spefilepath):
    #convert a sequential spectral SPE file to a pandas dataframe with one axis wl and other axis gate delay.
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
    #convert a sequential SPE file (image or spectral) into a Tdms file. 
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
    #subroutine for writing a series of images to a tdms file. 
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
    #subroutine for writing a series of spectra to a tmds file. 
    framenum = 0
    
    rawdata_group_object = GroupObject("Raw Data", properties={})
    
    with TdmsWriter(tdmsfilepath, mode = 'a') as tdms_writer:   
        for frame in frames:
            channel_object = ChannelObject("Raw Data", "Frame" + str(framenum), frame[0][0], properties={})
            tdms_writer.write_segment([root_object,rawdata_group_object,channel_object])
            framenum = framenum +1


def cutSpectraldf(spectraldf, wl1 = None,wl2 = None):
    #cut up a spectral dataframe between two wavelenghts.
    wavelength = spectraldf.index
    if wl1 == None:
        wl1 = wavelength.min()
    if wl2 == None:
        wl2 = wavelength.max()
    
    idx1 = wavelength.get_loc(wl1, method = 'nearest')
    idx2 = wavelength.get_loc(wl2, method = 'nearest')

    spectra_cut = spectraldf.iloc[idx1:idx2]
    
    return spectra_cut

def maxandarea(spectra_cut):
    #calculate the area and maximum of a peak in a cut sepectral dataframe
    areas = pd.Series(index = spectra_cut.columns)
    maximums = pd.Series(index = spectra_cut.columns)

    wavelength_cut = spectra_cut.index
    for gatedelay in spectra_cut.columns:
        areas[gatedelay] = np.trapz(spectra_cut[gatedelay],wavelength_cut)
        maximums[gatedelay] = spectra_cut[gatedelay].max()      
        
    return areas, maximums

def fitdecay(spectraldf, wl1 = None, wl2 = None, wl1_fit = None, wl2_fit = None):
    #fit the log of a PL decay to a line, and return the fit line and coefficients
    spectra_cut = cutSpectraldf(spectraldf,wl1,wl2)
    areas, maximums = maxandarea(spectra_cut)
    
    if wl1_fit == None:
        wl1_fit = maximums.index.min()
    if wl2_fit == None:
        wl2_fit = maximums.index.max()
    
    idx1 = maximums.index.get_loc(wl1_fit, method = 'nearest')
    idx2 = maximums.index.get_loc(wl2_fit, method = 'nearest')
    
    gatedelays = maximums.index[idx1:idx2]
    maximums = np.log(maximums.iloc[idx1:idx2])
    
    fitcoef = np.polyfit(gatedelays,maximums,1)
    
    gatedelays_fit = np.linspace(gatedelays.min(),gatedelays.max(),100)
    fit = fitcoef[1] + fitcoef[0]*gatedelays_fit
    
    fit = np.exp(fit)
    
    return fit, gatedelays_fit, fitcoef


class SpectraPlot():
    #plot of a simple intensity vs wavelength spectra
    def __init__(self,spectra,wavelength):
        self.fig, self.ax1 = plt.subplots(figsize = (8,6))
        self.ax1.plot(wavelength,spectra)
        self.ax1.set_xlabel("Wavelength (nm)")
        self.ax1.set_ylabel("Intensity (a.u.)")

    
class PLplot_new():
    #plot of a PL decay. First initializes the figure by adding a laser profile, then you call add_decay to add further PL decay plots
    def __init__(self, laserseries):
        self.fig, self.ax1 = plt.subplots(figsize = (8,6))
        
        self.ax1.set_xlabel("Gate Delay (ns)")
        self.ax1.set_ylabel("$Delta$ PL Intensity (Normalized)")
        self.ax1.tick_params('y')
        self.ax1.set_yscale('log')
        
        self.ax2 = self.ax1.twinx()
        self.ax2.set_ylabel("Laser Intensity (Normalized)")
        self.ax2.tick_params('y')
        self.ax2.set_yscale('log')
        
        self.lns = self.ax2.plot(laserseries.index, laserseries, '--', color = 'gray', label = 'Laser profile')
        
        self.setlegend()
        self.fig.suptitle('PL Plot', y = 1)
        self.fig.tight_layout()
        
    def add_decay(self,spectraldf, label,method = "max", wl1 = None ,wl2 = None, color = None):
        spectra_cut = cutSpectraldf(spectraldf, wl1,wl2)
        
        areas, maximums = maxandarea(spectra_cut)
        
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

    def setlegend(self):
        #iterate through lines and make a label
        labs = [l.get_label() for l in self.lns]
        self.legend = self.ax1.legend(self.lns, labs, loc=0)
        
        # Make the y-axis label, ticks and tick labels match the line color.

def parse_lasertiming(filepaths):
    #folderpath = os.path.split(filepaths[0])
    #filenames = [f for f in os.listdir(folderpath) if os.path.isfile(os.path.join(folderpath,f))]
    #filenames = [os.path.split(filepath) for filepath in filepaths if os.path.splitext(filepaths)[1] == '.spe']

    spe_files = sl.load_from_files(filepaths)
    if type(spe_files) != type(list()):
        spe_files = [spe_files]
    gatedelays = get_gatedelays(spe_files[0])
    intensities = pd.DataFrame(index = gatedelays, columns = range(len(filepaths)))
    timestamps = pd.DataFrame(index = gatedelays, columns = range(len(filepaths)))
    i=0    
    for spe_file in spe_files:
        frames  = spe_file.data
        intensity = list(map(lambda x: x[0].max(), frames))
        try:
            intensities.iloc[:,i] = pd.Series(intensity, index = intensities.index)
            timestamps.iloc[:,i] = pd.Series(get_starttimes(spe_file), index = timestamps.index)
            i=i+1
        except ValueError: #comes up if there is an incomplete file. 
            print(spe_file, ' did not have correct number of data points')
    intensities = intensities.truncate(after = i, axis = 'columns')
    return intensities, timestamps


#parse_lasertiming('C:\\Users\\aspit\\OneDrive\\Data\\2018-09-19\\Logfiles\\test')


#TRPL lifetime pseudo code
# inputs: SPE TRPL sequence, powermeter tdms file, SPE file of camera 2 sequence (laser timing)
# parse SPE file to obtain spectra dataframe
# normalize the dataframe to power 
# plot the time decay along with the power meter and laser timing to make sure that there is steady state
# Use time sequence to parse the power meter file

# make this a modular funciton so that the code can be used to parse series of test cases
# returns fitparameters
    
   