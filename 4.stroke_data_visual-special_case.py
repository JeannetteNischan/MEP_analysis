'''4. MEP analysis script
for visual inspection and classification of the trials
preceeded by script 3.1 'stroke_data_cluster' and followed by 5 'stroke_data_sort'
Author: Jeannette Nischan
Date of first version: July 14th 2022'''

#%% Import all tools
from pickle import FALSE
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import collections
import json

#%% define paths and variables
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO/'
target_direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO/labelled/'

delay = 15  # delay after TMS pulse (at 0) for peak to peak search in miliseconds


#testdata = pd.read_json( direct + 'post1/007.json').to_dict()
#epoch = testdata[4]

#plt.plot(epoch['Time'], epoch['MEP'])
#plt.show()

#%% define functions

def baseline_correct(data):
    for epoch in data.keys():
        trial = data[epoch]
        base_mean = np.mean(trial['MEP'][0:91]) # mean of baseline data from -100 to -10 ms
        trial['MEP'] = [x - base_mean for x in trial['MEP']]  # substract mean from every value to center around 0
    
    return data    

def MEP_latency(trial, index_min):
    tmp_std = np.std(trial['MEP'][:96])
    tmp_mean = np.mean(trial['MEP'][:96])
    lat_search = trial['MEP'][index_min -10:index_min +10]
    # latency is index where the first MEP value is higher than the mean + standard deviation
    #np_where returns an array so [0][0] is neccessary to get first item
    latency_data = list(map(abs,(lat_search)))
    latency_index = np.where(latency_data > (tmp_mean + tmp_std))[0]
    if len(latency_index) > 1:
        latency_index = latency_index[0]
        latency = latency_index + (index_min -10) # take first value and add index of stimulus+delay to correct shift
    elif len(latency_index) == 0:
        latency_index = 0
        latency = 0   
    elif len(latency_index) == 1:
        latency_index = latency_index[0]
        latency = latency_index + (index_min -10)
    else:
        latency = latency_index + (index_min -10) # take first value and add index of stimulus+delay to correct shift        

    
    return latency

def find_index(trial, delay):
    '''finds index of delay value. Delay in ms after TMS Pulse sets the timepoint for
    latency and peak-to-peak (MEP) search'''
    index = trial['Time'].index(delay)
    
    return index    

def peak_to_peak(trial, delay):
    '''calculates the peak to peak distance value and returns values'''
    index = find_index (trial, delay)
    max_amp = max(trial['MEP'][index:])
    index_max = trial['MEP'][index:].index(max_amp) + index #correct for subset of list (shift)
    min_amp = min(trial['MEP'][index:])
    index_min = trial['MEP'][index:].index(min_amp) + index
    ptp =  abs(max_amp-min_amp)
    return max_amp, min_amp, index_max, index_min, ptp 

def trial_sort():
    key = 0
    while key != 1:
        choice = input('Please classify the trial. \n Press -k- to keep trial \n -r- to reject trial with artefact or noisy data \n and - to reject trial no MEP: \n')
        if choice == 'k':
            tag = 'accept'
            key = 1
        elif choice == 'r':
            tag = 'reject'
            key = 1
        elif choice == '-':
            tag = 'no MEP'
            key = 1    
        else:
            key = 0
    return tag        

        
def plot_trials(data, subject_data, delay, alias, timepoint):
    '''iterates over epochs in subject data and plots MEP signal'''
    for epoch_nr in data.keys():
        #epoch =                  # set epoch_nr for debugging
        trial = data[epoch_nr]
        subject_data[epoch_nr]['Trial_Nr'] = epoch_nr
        max_amp, min_amp, index_max, index_min, ptp = peak_to_peak (trial, delay)
        index = find_index (trial, delay)
        latency = MEP_latency (trial, index_min)
        subject_data[epoch_nr]['ptp_amp'] = ptp
        subject_data[epoch_nr]['latency'] = latency -100
        if trial['intensity']:
            intensity = trial['intensity']
        else:
            intensity = 'MISSING'
        subject_data[epoch_nr]['stim_intens'] = intensity
        print(alias[0:3] + ' at ' + timepoint + ', epoch ' + str(epoch_nr))
        plt.figure()
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        plt.plot(trial['Time'], trial['MEP']) # plot MEP data
        plt.vlines(0,-10,10, 'g') # indicate TMS pulseS
        plt.hlines(np.mean(trial['MEP'][:95]) + 10, -100, 0, linestyle = "dashed", color = 'k')# plot border of pre-activation 20µV
        plt.hlines(np.mean(trial['MEP'][:95]) - 10, -100, 0, linestyle = "dashed", color = 'k')# plot border of pre-activation 20µV
        plt.ylim([min_amp-10, max_amp+10])
        plt.title(f"Patient: {alias[0:3]}, {timepoint}, Trial: {str(epoch_nr)} \n Intensity: {str(intensity)}, MEP: {round(ptp,3)}, Latency: {str(trial['Time'][latency])}")
        plt.vlines(trial['Time'][latency],  trial['MEP'][latency] + 2.5, trial['MEP'][latency] -2.5 , color = 'r')
        plt.plot(trial['Time'][index_max], max_amp, marker = 'o', color = 'c') 
        plt.plot(trial['Time'][index_min], min_amp, marker = 'o', color = 'c')
        #plt.axis([trial['Time'][0], trial['Time'][-1], -30, 60])
        plt.draw()
        plt.pause(1)
        tag = trial_sort()
        subject_data[epoch_nr]['label'] = tag
        plt.close()

    return subject_data    


#%% loop over all patient files
timepoint = 'post5'
subjects = ['006.json','007.json'] #['006.json','008.json','011.json','014.json','015.json'] #014 reject all (bad data)

for alias in subjects:
    subject_data = collections.defaultdict(dict)
    data = pd.read_json( direct + timepoint + '/' + alias ).to_dict()
    data = baseline_correct(data)
    subject_data = plot_trials(data, subject_data, delay, alias, timepoint)
    # create dataframe from dict and store as json file
    df = pd.DataFrame.from_dict(subject_data) 
    if os.path.exists(target_direct + timepoint): # check if folder already exists
        df.to_json (target_direct + timepoint + '/' + alias )
    else:
        os.makedirs(target_direct +  timepoint) # otherwise create folder
        df.to_json (target_direct +  timepoint + '/' + alias )
