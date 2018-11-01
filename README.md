# MHDlab
MHDLab is a collection of labview and python programs used for the data aquisition and analysis in the MHD Lab at NETL. 


# Installation

## Prerequisites
The MHDLab software utilizes Labview and Python. Most of this software should already be installed on the main data acquisition computer, but you should double check that each program is acessible by going through this list. 

1. [Labview 2018](http://www.ni.com/download/labview-development-system-2018/7413/en/) must be installed. Note that the group licence can be determined by opening NI license manger. 
2. [Daqmx 18.1](http://www.ni.com/download/ni-daqmx-18.1/7702/en/)

3. Next, use the VI package manager (installed with labview) to install the following packages
  * Enthought Python integration toolkit - Standard Edition v1.2.1.79
  * OpenG Labview Toolkit. Note: Only required for TDMS concatenating at the moment, and is not critical for data acquisition.

4. [Anaconda](https://www.anaconda.com/download/) (Make sure to install the Python 3 version) 

## Downloading the repository
To use the software, you can simply download this repository using the clone or download button on the [main page of the repository](https://github.com/aspitarl/MHDlab). Then unzip the contents and follow the setup instructions below. 

### Using Git
For any extended use of the software that will include the addition of new Vis and analysis scripts, it is preferable that researchers utilize Git, so that the new code can be easily integrated into this software library. Github is a website used to store Git repositiories. You can run Git and setup the MHDLab repository locally without creating a Github account but it is needed for collaboration at this point. Skip steps 4 and 5 if you do not want to use github. 

1. Download and install Git [here](https://git-scm.com/downloads). 
2. Then create a Git folder in the location of your choice. This typically is in the home directory (C:\Users\yourusername\Git)
3. When in that folder right click and select "Git Bash Here"
4. Create a Github account
5. Once you have done so press 'fork' in the upper right of the page.
6. Next, you need to clone the remote (github) repository onto your computer. Open Git Bash in windows and in the command prompt type `git clone https://github.com/yourusername/MHDlab`. Use yourusername = aspitarl if you did not create a github account.
5. Type `cd MHDlab` in Git Bash to have enter your new repository.

Once you have added any code or made changes, you should should get some basic knowledge of how to use git to stage and commit changes so those codes can be shared with the rest of the group. I recommend the [Git Book](https://git-scm.com/book/en/v2) 

## Setup 
Once you have a folder setup, run setup.bat. 

setup.bat does two things, some information about what it does in case there are errors: 

* runs setup.py in python, which will install the mhdpy python package. Currently this is installed in 'develop' mode which allows for changes to the MHDpy module to show up without having to reinstall.

* Runs `Common SubVis\Setup_GlobalVariable.vi`, which will update the repository path variable within `GlobalVariables.vi`

# Using MHDLab

The information on the use and further development of the MHDlab software is outlined in the wiki. Read the wiki [overview](https://github.com/aspitarl/MHDlab/wiki/Overview) or read [Data Acquisition](https://github.com/aspitarl/MHDlab/wiki/Data-Acquisition) to jump to acquiring data (read the Usage section, Development is for how to add VIs etc.). 

