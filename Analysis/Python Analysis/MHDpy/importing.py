
from nptdms import TdmsFile as TF
import numpy as np
import os
import re
import pandas as pd

    #get the paths of the files. This function takes a path, a regular expression for the filenames, and a flag for wether you want to recursively
    #search through the file directories. 
def get_pathnames(path, regExp= ".*\.tdms$", searchNested = True):
    pathnames = []
    filenames = []

    i = 0
    for root, subdirs, files in os.walk(path):
        if((searchNested == True) or (i == 0)):  #Checks if you want to search subdirectories or if we are still in 'path' (first iteration)
            for filename in files:
                if(re.match(regExp,filename)):
                    file_path = os.path.join(root, filename)
                    filenames = np.append(filenames, filename)
                    pathnames = np.append(pathnames, file_path)
        i = i+1
    pathnames = pd.Series(pathnames, index = filenames)
    return pathnames


def import_data(pathnames, filename):
    #Will import all data in the defined file path with substring input
    return TF(pathnames[filename])

def to_dframe(file, groupname):
    return file.object(groupname).as_dataframe()


def create_ref(file):
    dic = {}
    groups = file.groups()
    for group in groups:
        dic[group] = []
        for channel in file.group_channels(group):
            channelname = channel.channel
            dic[group] = np.append(dic[group], channelname)
    return dic
