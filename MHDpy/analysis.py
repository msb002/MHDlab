# -*- coding: utf-8 -*-
"""
Functions for use in Data Analysis
"""
import numpy as np


def find_nearest(a, a0):
    "Element in nd array `a` closest to the scalar value `a0`"
    idx = np.abs(a - a0).argmin()
    return idx


def PL_peakmax(data, wavelength, wlmin,wlmax):
    idx_l = find_nearest(wavelength,wlmin)
    idx_r = find_nearest(wavelength,wlmax)
    
    wavelength_cut = wavelength[idx_l:idx_r]
    
    data_cut = data[idx_l:idx_r]
    
    data_cut_max = []
    
    for frame in data_cut:
        maximum = data_cut[frame].max()
        data_cut_max = np.append(data_cut_max, maximum)
        
    return data_cut_max, wavelength_cut, data_cut

def PL_fit_powerdep(data, fits, NDF,idx_l,idx_r):
    timedata = data['Time'][NDF]
    data_p1_ln = np.log(data['Data_p1_max_norm'][NDF])
    fits['Fit_p1_param'][NDF] =np.polyfit(timedata[idx_l:idx_r], data_p1_ln[idx_l:idx_r], 1)
    fits['Fit_p1_time'][NDF] = np.linspace(timedata[idx_l], timedata[idx_r], 100)
    fits['Fit_p1'][NDF] = np.poly1d(fits['Fit_p1_param'][NDF])
    fits['Fit_p1'][NDF] = np.exp(fits['Fit_p1'][NDF](fits['Fit_p1_time'][NDF]))
    
    data_p2_ln = np.log(data['Data_p2_max_norm'][NDF]) 
    fits['Fit_p2_param'][NDF] =np.polyfit(timedata[idx_l:idx_r], data_p2_ln[idx_l:idx_r], 1)
    fits['Fit_p2_time'][NDF] = np.linspace(timedata[idx_l], timedata[idx_r], 100)
    fits['Fit_p2'][NDF] = np.poly1d(fits['Fit_p2_param'][NDF])
    fits['Fit_p2'][NDF] = np.exp(fits['Fit_p2'][NDF](fits['Fit_p2_time'][NDF]))
