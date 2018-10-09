# MHDlab
MHDlab labview library

A library of labview programs for the data aquisition equipment in the MHD Lab at NETL. There is a VI corresponding to each instrument that can be run independently, or called alongside other VIs by a 'main' master program. The main VI programatically calls the instrument VIs and synchronizes their outputs into a TDMS format file.

These are the instruments being recorded:

### Spectrometers

  Aquires data from Oceanoptics Flame and NIR-512 spectrometers as well as switching a OceanOptics Multiplexer
  
### Motor Control

  Controls a Galil 4-axis PLC motor system
  
### Power meters

  Aquires data from the data from Ophir pulse energy meters
  
### Sensors

  Aquires data from a NI PXI system (VI is generalized for any DAQmx tast) and Alicat flow meters
  
### Keithley

  Aqires data from Keithley 2812 and 6221 pair
  
### Lightfield

  Operate PI-max4 cameras and ISOplane spectrograph by controlling Lightfield through Labview.
  
### Image Analysis

  Use labview to process images for data analysis.

