# MHDlab
MHDlab labview library

A library of labview programs for the data aquisition equipment in the MHD Lab at NETL. 


# Prerequisites
The MHDLab software utilizes Labview and Python. The following software is required:

### Labview
* Labview 2018
* Daqmx 18.1
* Enthought Python integration toolkit - Standard Edition v1.2.1.79
* OpenG Labview Toolkit (Only required for TDMS concatenating at the moment)

### Python 
* Anaconda 5.2 (Make sure to install the Python 3 version) 

# Installation

## Downloading the repository
To use the software, you can simply download this repository using the clone or download button on the [main page of the repository](https://github.com/aspitarl/MHDlab). Then unzip the contents and follow the setup instructions below. 

For any extended use of the software that will include the addition of new Vis and analysis scripts, it is preferable that researchers utilize Git, so that the new code can be easily integrated into this software library. 

1. Download and install Git [here](https://git-scm.com/downloads). 
2. Then create a Git folder in the location of your choice. This typically is in the home directory (C:\Users\yourusername\Git)
3. When in that folder right click and select "Git Bash Here"
4. In the command prompt type `git clone https://github.com/aspitarl/MHDlab`
5. type `cd MHDlab` to have git bash enter the new directory.

At this stage you are set to modify and use the software, but you should should get some basic knowledge of how to use git to stage and commit changes. I recommend the [Git Book](https://git-scm.com/book/en/v2) 

## Setup 
Once you have a folder setup, run setup.bat. This should do two things: 1) run setup.py in python, which will install the 'MHDpy' python module. Currently this is installed in 'develop' mode which allows for changes to the MHDpy module to show up without having to reinstall. 2) Runs Setup_GlobalVariable.vi, which will update the Labview global variable with the correct path to your repository. 




