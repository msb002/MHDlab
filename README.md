# MHDlab
MHDLab is a collection of labview and python programs used for the data aquisition and analysis in the MHD Lab at NETL. 


# Installation

## Prerequisites
The MHDLab software utilizes Labview and Python. The following software is required:

### Labview
* Labview 2018
* Daqmx 18.1
* Enthought Python integration toolkit - Standard Edition v1.2.1.79
* OpenG Labview Toolkit (Only required for TDMS concatenating at the moment)

### Python 
* Anaconda 5.2 (Make sure to install the Python 3 version) 

## Downloading the repository
To use the software, you can simply download this repository using the clone or download button on the [main page of the repository](https://github.com/aspitarl/MHDlab). Then unzip the contents and follow the setup instructions below. 

### Using Git
For any extended use of the software that will include the addition of new Vis and analysis scripts, it is preferable that researchers utilize Git, so that the new code can be easily integrated into this software library. 

1. Download and install Git [here](https://git-scm.com/downloads). 
2. Then create a Git folder in the location of your choice. This typically is in the home directory (C:\Users\yourusername\Git)
3. When in that folder right click and select "Git Bash Here"

Github is a website used to store Git repositiories. You can run Git and setup the MHDLab repository locally without creating a Github account but it is needed for collaboration at this point. Skip to step 6 if you do not want to use github. 

4. Create a Github account
5. Once you have done so press 'fork' in the upper right of the page.

Next, you need to clone the remote (github) repository onto your computer.

6. In the command prompt type `git clone https://github.com/yourusername/MHDlab`. Use yourusername = aspitarl if you did not create a github account.
5. type `cd MHDlab` to have git bash enter the new directory.

Once you have added any code or made changes, you should should get some basic knowledge of how to use git to stage and commit changes so those codes can be shared with the rest of the group. I recommend the [Git Book](https://git-scm.com/book/en/v2) 

## Setup 
Once you have a folder setup, run setup.bat. This should do two things: 1) run setup.py in python, which will install the 'MHDpy' python module. 

Currently this is installed in 'develop' mode which allows for changes to the MHDpy module to show up without having to reinstall. 2) Runs Setup_GlobalVariable.vi, which will update the Labview global variable with the correct path to your repository. 

# Using MHDLab

The information on the use and further development of the MHDlab software is outlined in the wiki. Read the wiki [overview](https://github.com/aspitarl/MHDlab/wiki/Overview) or read [Data Acquisition, Visualization, and Logging](https://github.com/aspitarl/MHDlab/wiki/Data-Acquisition,-Visualization,-and-Logging) to jump to acquiring data. 

