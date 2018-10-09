# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 14:33:38 2017

@author: aspitarl
"""
from skimage import data
import numpy as np
import matplotlib.pyplot as plt
import csv

import timeit

#import Tkinter, tkFileDialog

#root = Tkinter.Tk()
#root.withdraw()

#file_path = tkFileDialog.askopenfilename()

folder = "C:/Users/aspitarl/Documents/LightField/9-12-17 camera/Time1/"

size = 50
xdim = 1024
ydim = 1024

image = np.zeros((xdim,ydim),dtype = "int16")
#result = np.zeros((xdim,ydim,size))
maximum = np.zeros(size,dtype = "int16")

linecut = np.zeros((ydim,size),dtype = "int16")
linex = 283  

t0 = 930
dt = 0.3
time = np.arange(t0, t0 + size*dt, dt)

for i in range(1, size):
    
    start_time = timeit.default_timer()
    
    filename = "2017 September 12 13_38_10-Frame-" + str('{0:03}'.format(i)) + ".csv"
    file_path = folder + filename
    #reader = csv.reader(open(file_path, "rb"), delimiter=",")
    image = np.loadtxt(open(file_path, "r"), delimiter=",", skiprows=1, usecols = range(1,1024) , dtype = "int16")
    
    elapsed1 = timeit.default_timer() - start_time
    
    #x = list(reader)
    #del image[0]
    
    
    
    #for row in x:
    #    del row[0]
        

     
    #image =  np.array(x).astype("int16")
    
    
    
    #result[:,:,i] = image
    maximum[i] = np.amax(image)
    linecut[:,i] = image[linex,:]
    
    elapsed2 = timeit.default_timer() - elapsed1 - start_time
    
#del image


#plt.plot(maximum,time)


#plt.imshow(result[:,:,size-1])
#print type(result)