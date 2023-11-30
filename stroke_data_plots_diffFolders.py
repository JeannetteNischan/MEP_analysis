'''6. MEP analysis script


Author: Jeannette Nischan
Date of 1st Version:  Dec 2022
'''

#%%import tools and libraries
import pandas as pd
import os
import matplotlib.pyplot as plt
import collections

#%% define paths and fixed variables if needed
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO/sorted/accepted/'
target_direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO/plots/'
intensities = os.listdir(direct)
chrono = {'pre1' : 0, 'post1' : 1, 'pre3' : 2, 'post3' : 3, 'post5' : 4}

#%% define function to plot data for each participant, timepoint and intensity and save images
def plot_data(data, alias, timepoint, intensity):
    x = []
    y = []
    for i in data[intensity].keys(): 
        y.append(data[intensity][i]['ptp_amp'])
        x.append(data[intensity][i]['latency'])
    avgMEP = sum(y)/len(y)
    avgLat = sum(x)/len(x)
    plt.scatter(x,y)
    plt.title(f"Patient: {alias[0:3]}, at: {timepoint}, intensity: {intensity} % RMT")
    plt.scatter(avgLat,avgMEP)
    plt.show()
    if os.path.exists(target_direct + alias[0:3]): # check if folder already exists
        plt.savefig(target_direct + alias[0:3] + '/' + timepoint + intensity + '%RMT.png', format = 'png')
    else:
        os.makedirs(target_direct + alias[0:3]) # otherwise create folder
        plt.savefig(target_direct + alias[0:3] + '/' + timepoint + intensity + '%RMT.png', format = 'png')
    
    return avgMEP

#%% define function to plot Input/Output curves in two different ways
def plot_IO():


#%% loop over all patient files

for intensity in intensities:
    timepoint = os. listdir(direct + intensity)
    
    for timepoint in timepoints: 
        subjects = os.listdir(direct + intensity + '/' + timepoint)
       
        for alias in subjects:
            if os.path.exists(direct + intensity + '/' + timepoint+ '/' + alias[0:3] + '_intensity_over_time.json'): 
                with open(direct + intensity + '/' + timepoint + '/' + alias[0:3] + '_intensity_over_time.json') as json_file:
                    int_over_time = json.load(json_file)
            else:
                int_over_time = collections.defaultdict(dict)
                
            subject_data = pd.read_json( direct +  intensity + '/' + timepoint + '/' + alias ).to_dict()
            avgMEP = plot_data (subject_data, alias, timepoint, int(intensity[0:3]))
            int_over_time[intensity[0:3]][chrono[timepoint]] = avgMEP