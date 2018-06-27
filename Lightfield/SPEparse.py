# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import spe2py as spe
import spe_loader as sl

import matplotlib.pyplot as plt


#loaded_files = spe.load()

##spectrum test

spe_file = sl.load_from_files(['C:/Users/aspitarl/OneDrive/Data/Test.spe'])

frames  = spe_file.data

for frame in frames:
    frame = frame[0]
    spectrum = plt.plot(spe_file.wavelength.transpose(), frame.transpose())


##image test
    
#spe_image = sl.load_from_files(['C:/Users/aspitarl/OneDrive/Data/TestImage.spe'])   


#spe_tools = spe.load()
#spe_tools.image()  # images the first frame and region of interest