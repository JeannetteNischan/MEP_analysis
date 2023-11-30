'''2. script for MEP analysis
   prepares, loads, filters and epochs MEP data
   preceeded by script 1 'stroke_data_prepare'
   followed by script 3 'stroke_data_visualinspection' 
   Author: Jeannette Nischan
   Date of first working version: 27. May 2022'''

#%% 1. import tools and libraries
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import glob
from scipy import stats
import pandas as pd
import itertools
from scipy import io
import scipy
import keyboard
import math


# %% 2. Define used information
# paretic side of each patient
p_EDC_left = ['015', '016', '009', '002', '019', '012', '001', '010', '007', '017', '005', '006', '018']
p_EDC_right = ['011', '014', '003', '004', '013', '008']

# key of interest (recorded physiological data)
direct  = '/home/jeanettenischan/Data/data_INTENS_TMS/data/' #main folder with all subject subfolder
target_direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/' #folder to store processed data
data    = 'BrainVisionRDA_series'  
channel = 'EDC'
tms     = 'tms_artifact'
stim_intens = 'localite_timeseries'

#set boundaries for epochs
before_stim = -100   # time where epoch starts, needs to be negative integer or 0
after_stim = 100     # time where epoch ends (after TMS_pulse pulse), needs to be an integer

# Create a list of folder names as subject id
import os
subject_ids = os.listdir(direct)


# %% 3. Define functions needed to load, filter and epoch the data 
from scipy.io import loadmat
import ast

# 3.1. function to find index of channel of interest
def get_chan_idx(array_ch, target_chan):
    '''returns the index of a channel of interest from a given array
    input: array of channel names, channel of interest as string
    output: index of target channel
    uses numpy where and looks for target channel in array. 
    Returns an array so indexing of 0 (twice) is necessary to return an integer
    see also https://thispointer.com/find-the-index-of-a-value-in-numpy-array/'''
    return np.where(array_ch == target_chan)[0][0]

#3.2. define function to extract stim intensity from aary of strings
def extract_intens (string_array):
    '''extracts the value of a dictionary that was stored as string
    iterates over an array of dict strings and converts each into actual dict
    then takes the value of the key/value pair in the dict and stores it in an array
    Input: string_array (array of dictionary strings)
    Output: intensity
    https://stackoverflow.com/questions/7002429/how-can-i-extract-all-values-from-a-dictionary-in-python
    https://stackoverflow.com/questions/988228/convert-a-string-representation-of-a-dictionary-to-a-dictionary '''
    intensity = [] # define empty list for intensity values
    for i in range(0,len(string_array)):
        temp = ast.literal_eval(string_array[i]) # convert string into dict
        intensity.append(temp.values())[0] # extract value from dict and store in array
    return intensity

# 3.3. function to load all I/O data for every subject and timepoint
def load_files (alias, channel):
    '''loads the ipsolesional I/O data from paretic side for set subject (alias) 
    for all timepoints (pre1,post1,pre3,post3,post5) into a dictionary
    input: subject number, EMG channel  (of interest)
    output: subject_dict with I/O information (MEP_data, stim intensity, marker,...) for each timepoint'''
 
    #[f"{alias}"] = {} #predefine empty dictionary for subject
    subject_dict = {}
    
    # check if file exsits and load data for each timepoint
    if os.path.isfile(direct + alias + '/pre1/IO_ipsilesional.mat'):
        pre1  = loadmat(direct + alias + '/pre1/IO_ipsilesional.mat')
    else:
        pre1  = {}    
    if os.path.isfile(direct + alias + '/post1/IO_ipsilesional.mat'):    
        post1 = loadmat(direct + alias + '/post1/IO_ipsilesional.mat')
    else:
        post1 = {}
    if os.path.isfile(direct + alias + '/pre3/IO_ipsilesional.mat'):
        pre3  = loadmat(direct + alias + '/pre3/IO_ipsilesional.mat')
    else:
        pre3  = {}
    if os.path.isfile(direct + alias + '/post3/IO_ipsilesional.mat'):
        post3 = loadmat(direct + alias + '/post3/IO_ipsilesional.mat')
    else:
        post3  = {}
    if os.path.isfile(direct + alias + '/post5/IO_ipsilesional.mat'):   
        post5 = loadmat(direct + alias + '/post5/IO_ipsilesional.mat')
    else:
        post5 = {}    

    if (alias in p_EDC_left):
        chan = channel+'_L' # if subject id is in list of paretic side left, set channel for left side
        #store data of interest (defined earlier), from channel of interest, as value for timepoint key
        #check channel index in every dataset with get_chan_idx function
        subject_dict = {'pre1': {}, 'post1': {}, 'pre3' : {}, 'post3' : {}, 'post5' : {}}
        if pre1:    
            subject_dict['pre1']['MEP_data']     = pre1[data][:,get_chan_idx(pre1['channel_label'], chan)]
            subject_dict['pre1']['TMS_pulse']          =  pre1[tms][0]
        #subject_dict['pre1']['stim_intens']  = extract_intens(pre1[stim_intens]) 
        if post1:
            subject_dict['post1']['MEP_data']    = post1[data][:,get_chan_idx(post1['channel_label'], chan)]
            subject_dict['post1']['TMS_pulse']         =  post1[tms][0]
        #subject_dict['post1']['stim_intens'] = extract_intens(post1[stim_intens]) 
        if pre3:
            subject_dict['pre3']['MEP_data']     = pre3[data][:,get_chan_idx(pre3['channel_label'], chan)]
            subject_dict['pre3']['TMS_pulse']          =  pre3[tms][0]
        #subject_dict['pre3']['stim_intens']  = extract_intens(pre3[stim_intens]) 
        if post3:
            subject_dict['post3']['MEP_data']    = post3[data][:,get_chan_idx(post3['channel_label'], chan)]
            subject_dict['post3']['TMS_pulse']         =  post3[tms][0]
        #subject_dict['post3']['stim_intens'] = extract_intens(post3[stim_intens]) 
        if post5:
            subject_dict['post5']['MEP_data']    = post5[data][:,get_chan_idx(post5['channel_label'], chan)]
            subject_dict['post5']['TMS_pulse']         =  post5[tms][0]
        #subject_dict['post5']['stim_intens'] = extract_intens(post5[stim_intens]) 
            
        print('loading data for subject ' + alias + ' successful')   
        return subject_dict 

    elif (alias in p_EDC_right):
        chan = channel+'_R' # if paretic side is right
        #store data of interest (defined earlier), from channel of interest, as value for timepoint key
        #check channel index in every dataset with get_chan_idx function
        subject_dict = {'pre1': {}, 'post1': {}, 'pre3' : {}, 'post3' : {}, 'post5' : {}}
        if pre1:    
            subject_dict['pre1']['MEP_data']     = pre1[data][:,get_chan_idx(pre1['channel_label'], chan)]
            subject_dict['pre1']['TMS_pulse']          =  pre1[tms][0]
        #subject_dict['pre1']['stim_intens']  = extract_intens(pre1[stim_intens]) 
        if post1:
            subject_dict['post1']['MEP_data']    = post1[data][:,get_chan_idx(post1['channel_label'], chan)]
            subject_dict['post1']['TMS_pulse']         =  post1[tms][0]
        #subject_dict['post1']['stim_intens'] = extract_intens(post1[stim_intens]) 
        if pre3:
            subject_dict['pre3']['MEP_data']     = pre3[data][:,get_chan_idx(pre3['channel_label'], chan)]
            subject_dict['pre3']['TMS_pulse']          =  pre3[tms][0]
        #subject_dict['pre3']['stim_intens']  = extract_intens(pre3[stim_intens]) 
        if post3:
            subject_dict['post3']['MEP_data']    = post3[data][:,get_chan_idx(post3['channel_label'], chan)]
            subject_dict['post3']['TMS_pulse']         =  post3[tms][0]
        #subject_dict['post3']['stim_intens'] = extract_intens(post3[stim_intens]) 
        if post5:
            subject_dict['post5']['MEP_data']    = post5[data][:,get_chan_idx(post5['channel_label'], chan)]
            subject_dict['post5']['TMS_pulse']         =  post5[tms][0]
        #subject_dict['post5']['stim_intens'] = extract_intens(post5[stim_intens]) 
            
        print('loading data for subject ' + alias + ' successful')
        return subject_dict
    else:
        print('Subject ID not found')
            
    
# 3.3 function to filter the data as specified in part 2.

#3.4 function to epoch the data around markers
#def epoch_data (MEP_data):

# %% 4. iterate over list of subjects apply the functions to load, filter and epoch
# and save processed data
for alias in subject_ids:
    subject_dict = load_files (alias, channel) # load all data of interest with function
    #filter_data()
    #epoch_data
    filename = target_direct + alias + '.csv'
    df = pd.DataFrame.from_dict(subject_dict) 
    df.to_csv (filename) 