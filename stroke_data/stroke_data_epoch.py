'''3. script for MEP analysis
loads prepared data from script 2 'stroke_data_load' and 2.1 'stroke_data_complete'
and cuts into epochs of specified length. 
Followed by script 4. 'stroke_data_visualize'
Author: Jeannette Nischan
Date of first version: July 12th 2022'''

#import all tools
from matplotlib import markers
import pandas as pd
import numpy as np
import json
import os
from pathlib import Path
import collections

#%% predefine paths and varialbes (specifications)
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/' #folder with processed data
target_direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/Epochs/'
# Create a list of file names as subject id
subject_ids = []
for ID in os.listdir(direct):
    if ID.endswith('.json'):
        subject_ids.append(Path(direct + ID).stem)



#set boundaries for epochs
before_stim = -100   # time where epoch starts, needs to be negative integer or 0
after_stim = 100     # time where epoch ends (after TMS_pulse pulse), needs to be an integer

# function to epoch the data around markers
def epoch_data (MEP_data, upper, lower, timepoint, alias):
    '''function to cut continuous data into epochs of predefined length around a marker.
    Needs dictionary with data, upper and lower boundry of epoch in ms and
    timepoint of measurement as input.'''
    epoch = collections.defaultdict(dict) #create empty nested dict
    i = 1          #set number for epochs
    if alias in ['011', '014', '015'] and timepoint == 'pre1':
        for artefact in MEP_data[timepoint]['pre1_0']['TMS_pulse']: # iterate over marker
            if MEP_data[timepoint]['pre1_0']['stim_intens'] is not None:
                epoch[str(i)]['intensity'] = MEP_data[timepoint]['pre1_0']['stim_intens'][i-1]
            epoch[str(i)]['Marker'] = artefact
            epoch[str(i)]['MEP'] = MEP_data[timepoint]['pre1_0']['MEP_data'][artefact + before_stim : artefact + after_stim +1]
            epoch[str(i)]['Time'] = list(range(before_stim, after_stim + 1))     
            i += 1 #update epoch number
        for artefact in MEP_data[timepoint]['pre1_180']['TMS_pulse']:
            if MEP_data[timepoint]['pre1_180']['stim_intens'] is not None:
                epoch[str(i)]['intensity'] = MEP_data[timepoint]['pre1_180']['stim_intens'][i-1]
            epoch[str(i)]['Marker'] = artefact
            epoch[str(i)]['MEP'] = MEP_data[timepoint]['pre1_180']['MEP_data'][artefact + before_stim : artefact + after_stim +1]
            epoch[str(i)]['Time'] = list(range(before_stim, after_stim + 1))     
            i += 1 #update epoch number

    else:
        for artefact in MEP_data[timepoint]['TMS_pulse']: # iterate over marker
            if MEP_data[timepoint]['stim_intens'] is not None:
                epoch[str(i)]['intensity'] = MEP_data[timepoint]['stim_intens'][i-1]
            epoch[str(i)]['Marker'] = artefact
            epoch[str(i)]['MEP'] = MEP_data[timepoint]['MEP_data'][artefact + before_stim : artefact + after_stim +1]
            epoch[str(i)]['Time'] = list(range(before_stim, after_stim + 1))     
            i += 1 #update epoch number

    return epoch  


for alias in subject_ids: #iterate over subjects and load files
    if len(alias) == 3:
        MEP_data = pd.read_json('/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/' 
                               + alias + '.json').to_dict()
        timepoints = MEP_data.keys() # get measurement number from dictionary
        #print(MEP_data['pre1'].keys())
        print(alias)
        for timepoint in timepoints: #iterate over measurements
            epoch = epoch_data(MEP_data, after_stim, before_stim, timepoint, alias)
            # create dataframe from dict and store as json file
            df = pd.DataFrame.from_dict(epoch) 
            if os.path.exists(target_direct + timepoint): # check if folder already exists
                df.to_json (target_direct + timepoint + '/' + alias + '.json')
            else:
                os.makedirs(target_direct + timepoint) # otherwise create folder
                df.to_json (target_direct + timepoint + '/' + alias + '.json')
