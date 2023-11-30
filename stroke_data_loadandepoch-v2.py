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
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/data/' #main folder with all subject subfolder
data = 'BrainVisionRDA_series'  
channel = 'EDC'
#set boundaries for epochs
before_stim = -100   # time where epoch starts, needs to be negative integer or 0
after_stim = 100     # time where epoch ends (after TMS pulse), needs to be an integer

# Create a list of folder names as subject id
import os
subject_ids = os.listdir(direct)


# %% 3. Define functions needed to load, filter and epoche the data 
from scipy.io import loadmat

# 3.1. function to find index of channel of interest
def get_chan_idx(array_ch, target_chan):
    '''returns the index of a channel of interest from a given array
    input: array of channel names, channel of interest as string
    output: index of target channel
    uses numpy where and looks for target channel in array. 
    Returns an array so indexing of 0 (twice) is necessary to return an integer
    see also https://thispointer.com/find-the-index-of-a-value-in-numpy-array/'''
    return np.where(array_ch == target_chan)[0][0]

# 3.2. function to load all I/O data for every subject and timepoint
def load_files (alias, channel):
    '''loads the ipsolesional I/O data from paretic side for set subject (alias) 
    for all timepoints (pre1,post1,pre3,post3,post5) into a dictionary
    input: subject number, EMG channel  (of interest)
    output: dict with I/O files for each timepoint'''
 
    globals()[f"subj_{alias}"] = {} #predefine empty dictionary for subject
    try:
        # load data for each timepoint
        pre1  = loadmat(direct + alias + '/pre1/IO_ipsilesional.mat')
        post1 = loadmat(direct + alias + '/post1/IO_ipsilesional.mat')
        pre3  = loadmat(direct + alias + '/pre3/IO_ipsilesional.mat')
        post3 = loadmat(direct + alias + '/post3/IO_ipsilesional.mat')
        post5 = loadmat(direct + alias + '/post5/IO_ipsilesional.mat')

        if (alias in p_EDC_left):
            chan = channel+'_L' # if subject id is in list of paretic side left, set channel for left side
           
            globals()[f"subj_{alias}"] = {
                #store data of interest (defined earlier), from channel of interest, as value for timepoint key
                #check channel index in every dataset with get_chan_idx function
                'pre1' : pre1[data][:,get_chan_idx(pre1['channel_label'], chan)], 
                'post1': post1[data][:,get_chan_idx(post1['channel_label'], chan)],
                'pre3' : pre3[data][:,get_chan_idx(pre3['channel_label'], chan)],
                'post3': post3[data][:,get_chan_idx(post3['channel_label'], chan)],
                'post5': post5[data][:,get_chan_idx(post5['channel_label'], chan)]
                }
            print('loading successful')    

        elif (alias in p_EDC_right):
            chan = channel+'_R' # if paretic side is right
            globals()[f"subj_{alias}"] = {
                #store data of interest (defined earlier), from channel of interest, as value for timepoint key
                #check channel index in every dataset with get_chan_idx function
                'pre1' : pre1[data][:,get_chan_idx(pre1['channel_label'], chan)], 
                'post1': post1[data][:,get_chan_idx(post1['channel_label'], chan)],
                'pre3' : pre3[data][:,get_chan_idx(pre3['channel_label'], chan)],
                'post3': post3[data][:,get_chan_idx(post3['channel_label'], chan)],
                'post5': post5[data][:,get_chan_idx(post5['channel_label'], chan)]
                }
            print('loading successful')
        else:
            print('Subject ID not found')
    except:
        print('loading for subject ' + alias + ' unsuccessful')
    finally:
        print('completed subject ' + alias)

# 3.3 function to filter the data as specified in part 2.

#3.4 function to epoch the data around markers

# %% 4. iterate over list of subjects apply the functions to load, filter and epoch
# and save processed data
for alias in subject_ids:
    try:
        load_files (alias, channel) # load all data of interes with function

    except:
        print('process failed')    