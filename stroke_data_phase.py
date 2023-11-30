'''5. MEP analysis script
for extraction of the phase (0 or 180°) from the matfiles
preceeded by script 4 'stroke_data_visual' and followed by 
6 'stroke_data_sort'
Author: Jeannette Nischan
Date of first version: August 31st 2022'''

#%% 1.Import all needed libraries and modules

import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import io
import collections
import json
import pandas as pd

#%% 2. key of interest (recorded physiological data)
direct  = '/home/jeanettenischan/Data/data_INTENS_TMS/data/' #main folder with all subject subfolder
target_direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/labelled_phase/'#folder to store processed data
direct_dict = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO/labelled/'

# Create a list of folder names as subject id
subject_ids = os.listdir(direct)
timepoints = os.listdir(direct_dict)

# Create a file where possible problems are documented
error_messages = collections.defaultdict(dict) #predefine empty nested dictionary



def load_matfiles(alias, timepoint):
    datapath = direct + alias + '/' + timepoint + '/IO_ipsilesional.mat'
    if os.path.isfile(datapath):
        data = io.loadmat(datapath)
        print(alias + ' at ' + timepoint)
        if 'spongebob_timeseries' in data.keys():
            sp_marker = data["spongebob_timeseries"]
            sp_marker = np.squeeze(sp_marker)
            phase180 = np.where(sp_marker[:,12] == 180)
            plt.figure()
            plt.plot(sp_marker[:,12])
            plt.plot(sp_marker[:,11])
            plt.show()
            if len(phase180[0]) > 1:
                tms = data['tms_artifact'].size
                trigger = np.where(sp_marker[:,11] == 1)
                diff = trigger[0].size -tms
                trigger = trigger[0][diff:]
                phase = np.where(sp_marker[:,12] == 180)
                phase_change = phase[0][0]
                index = np.where(trigger >= phase_change)
                trigger_0 = trigger[0:index[0][0]]
                trigger0 = len(trigger_0)
                trigger_180 = trigger[index[0][0]:]
                trigger180 = len(trigger_180)
            else:
                print(' No phase 180° for '+ alias +' at ' + timepoint) 
                error_messages[timepoint][alias] = 'No phase 180 for '+ alias 
            
        else:
            print('No datastream with markers for ' + alias + ' at ' + timepoint) 
            error_messages[timepoint][alias] = 'No datastream with markers for ' + alias     

    else:
        print('No data available for {} at {}'.format(alias,timepoint)) 
        error_messages[timepoint][alias] = 'No data for ' + alias 
        trigger0 = []
        trigger180 = []

    return error_messages, trigger0, trigger180    


def load_dict(alias, timepoint, trigger0):
    dict_0 = []
    dict_180 = []
    subject_dict = pd.read_json( direct_dict + timepoint + '/' + alias).to_dict()
    list0 = range(1,trigger0)
    list180 = range(trigger0+1,len(subject_dict))
    for trial in subject_dict.keys():
        if trial in list0:
            dict_0.append(subject_dict[trial])
        elif trial in list180:
            dict_180.append(subject_dict[trial])
    print(len(dict_0))
    print(len(dict_180))
        


#%% loop over all patient files

for timepoint in timepoints:
    for alias in subject_ids:
        error_meassages, trigger0, trigger180 = load_matfiles(alias, timepoint)
        print('There are {} values for phase 0'.format(trigger0))
        print('There are {} values for phase 180'.format(trigger180))
        with open('/home/jeanettenischan/Data/data_INTENS_TMS/problems.json' , 'w') as outfile:
            json.dump(error_messages, outfile) 

        alias = alias +'.json'
        directory = os.listdir(direct_dict + timepoint)
        if alias in directory:
            load_dict(alias, timepoint, trigger0)
        