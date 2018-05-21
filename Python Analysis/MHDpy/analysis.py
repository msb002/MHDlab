# -*- coding: utf-8 -*-
"""
Created on Sun May 20 11:52:12 2018

@author: aspit
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

