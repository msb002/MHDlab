
from nptdms import TdmsFile as TF
import numpy as np
import os
import re
import pandas as pd


class TDMS():
    def __init__(self):
        self.samples = []
        self.pathnames = []
        self.imports = {}

        
        ##pathnames is the full pathnames to get to each tdms file (there maybe multiple tdms files associated to different samples)
        ##imports is a dictionary, using the pathnames as the word and the imported tdms file as its definition
        ##           this step is necessary as importing the data is the longest process, but pulling data to arrays is almost immediate
    
    #get the paths of the files. This function takes a path, a regular expression for the filenames, and a flag for wether you want to recursively
    #search through the file directories. 
    def set_pathnames(self, path, regExp= ".*\.tdms$", searchNested = True):
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
        self.pathnames = pd.Series(pathnames, index = filenames)
        return
    
        ##sets the path to the main folder with subfolders and tdms files in those subfolders
        ##uses the names of folders as samples and filepaths as pathnames
        ##filestr is a string with regular expressions defining the files to include in the path list. example: "*_together.tdms"
        
    def import_data(self, string):
        #Will import all data in the defined file path with substring input
        pathnames = self.pathnames
        imports = self.imports
        for pathname in pathnames:
            if string in pathname:
                imports[pathname] = TF(pathname)
        
        self.imports = imports
        return

    def create_ref(self,):
        dic = {}
        for impor in self.imports:
            file = self.imports[impor]
            break
        groups = file.groups()
        for group in groups:
            dic[group] = []
            for channel in file.group_channels(group):
                channelname = channel.channel
                dic[group] = np.append(dic[group], channelname)
        self.groups = dic
        return

    ##imports tdms files that contain the given string. for example: the molybdenum rod experiments had 9mm, 11mm, and 13mm runs
    ##folder and file paths were organized as such
    ##runs get_times(), makes it easier to stack arrays of data and line them up with time
    
    def resize(self, arr, length):
        if len(arr)>length:
            arr = arr[1:]
        elif len(arr)<length:
            arr = np.append(arr, 0)
        else:
            print("error")
        return arr   
    
class TDMS_pd():
    def __init__(self, ):
        #TDMS.__init__(self)
        self.datapdframes = {}
        self.datapseries = {}
        
    
    def get_data_pdframe(self,file, groupname):
        groups = file.groups()
        for group in groups:
            if(group == groupname):
                data = file.object(groupname).as_dataframe()
        
        self.datapdframes[groupname] = data
        return data
    
class TDMS_np():
    def __init__(self):
        #TDMS.__init__(self)
        self.data = {}
        self.tracks = {}
        
        ##data is a dictionary, using the pathnames as the word and a 2D array with all data stored, useful for plotting
        ##tracks is meant to track what data has already been pulled from the imported file, and track what position in the data array certain 
        ##data are
        ##           tracks uses channelnames as the word and an integer as its definition
    
    def get_custom(self, channelname):
        tctrack = channelname
        self.get_data(tctrack)
        return
        ##allows you to get data from a custom channel, given an input channel name
          
    def get_data(self, track, group=10):
        imports = self.imports
        tracks = self.tracks
        groups = self.groups
        
        if track not in tracks:     
            tracks[track] = len(tracks)
            for string in imports:
                file = imports[string]
                if group == 10:
                    for item in groups:
                        if track in groups[item]:
                            group = item
                subdata = file.object(group,track).data    
                self.store_data(string, subdata)
        
        self.tracks = tracks
        return
        
        ##searches all groups for a channel with the channelname
        ##gets data from this channel, runs store_data() to update the respective data array
        
    def store_data(self, string, array):
        data = self.data
        
        length = len(np.transpose(data[string]))
        if len(array) != length:
            array = self.resize(array, length)
        data[string] = np.vstack((data[string], array))
        
        self.data = data
        return
        
        ##as implied, stores data. stacks the array with time, updates the data dictionary, and stores data position in tracks
        ##the else statement prevents the data arrays from storing duplicate data
        
