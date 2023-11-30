'''6. MEP analysis script
preceeded by stroke_data_sort
followed by stroke_data_plotIO

Author: Jeannette Nischan
Date of 1st Version: 19th Dec 2022
'''

#%%import tools and libraries
import pandas as pd
import os
import matplotlib.pyplot as plt
import collections
import json
import math
from math import log


#%% define paths and fixed variables if needed
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/sorted/accepted/'
target_direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/plots/'
intensities = [name for name in os.listdir(direct) if os.path.isdir(os.path.join(direct, name))]
chrono = {'pre1' : 0, 'post1' : 1, 'pre3' : 2, 'post3' : 3, 'post5' : 4}

#%% define function to plot data for each participant, timepoint and intensity and save images
def plot_data(data, alias, timepoint, intensity):
    x = []
    x_time = []
    y = []
    y_log = []
    for i in data[intensity].keys(): 
        y.append(data[intensity][i]['ptp_amp'])
        x.append(data[intensity][i]['latency'])
        x_time.append(int(i))
        if data[intensity][i]['ptp_amp'] != 0:
            y_log.append(log(data[intensity][i]['ptp_amp']))
        else:
             y_log.append(0)   
    avgMEP = sum(y)/len(y)
    avgMEP_log = sum(y_log)/len(y_log)
    avgLat = sum(x)/len(x)
    occurrence = [val for val in y if val !=0]

    #plot MEP size against latency with average
    plt.figure()
    plt.scatter(x,y)
    plt.title(f"Patient: {alias[0:3]}, at: {timepoint}, intensity: {intensity} % RMT")
    plt.scatter(avgLat,avgMEP)
    plt.xlabel('Latency in ms')
    plt.ylabel('MEP (peak to peak amplitude) in µV')
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    if os.path.exists(target_direct + alias[0:3]+ '/' + 'latency/'): # check if folder already exists
        plt.savefig(target_direct + alias[0:3] + '/' + 'latency/' + timepoint + str(intensity) + '%RMT.png', format = 'png')
    else:
        os.makedirs(target_direct + alias[0:3]+ '/' +'latency/') # otherwise create folder
        plt.savefig(target_direct + alias[0:3] + '/' + 'latency/' + timepoint + str(intensity) + '%RMT.png', format = 'png')
    plt.close()

    #plot MEP size againts trial number
    plt.figure()
    plt.scatter(x_time,y)
    plt.title(f"Patient: {alias[0:3]}, at: {timepoint}, intensity: {intensity} % RMT")
    avgX = sum(x_time)/len(x_time)
    plt.scatter(avgX,avgMEP)
    plt.xlabel('Trial number')
    plt.ylabel('MEP (peak to peak amplitude) in µV')
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle() # funktioniert nicht!
    if os.path.exists(target_direct + alias[0:3]+ '/' + 'time/'): # check if folder already exists
        plt.savefig(target_direct + alias[0:3] + '/' + 'time/' + timepoint + str(intensity) + '%RMT.png', format = 'png')
    else:
        os.makedirs(target_direct + alias[0:3]+ '/' +'time/') # otherwise create folder
        plt.savefig(target_direct + alias[0:3] + '/' + 'time/' + timepoint + str(intensity) + '%RMT.png', format = 'png')
    plt.close()

    #plot log MEP size against time
    plt.figure()
    plt.scatter(x_time,y_log)
    plt.title(f"Patient: {alias[0:3]}, at: {timepoint}, intensity: {intensity} % RMT")
    plt.scatter(avgX,avgMEP_log)
    plt.xlabel('Trial number')
    plt.ylabel('MEP (log peak to peak amplitude)')
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    if os.path.exists(target_direct + alias[0:3]+ '/' + 'log/'): # check if folder already exists
        plt.savefig(target_direct + alias[0:3] + '/' + 'log/' + timepoint + '_' + str(intensity) + '%RMT.png', format = 'png')
    else:
        os.makedirs(target_direct + alias[0:3]+ '/' +'log/') # otherwise create folder
        plt.savefig(target_direct + alias[0:3] + '/' + 'log/' + timepoint + '_' + str(intensity) + '%RMT.png', format = 'png')
    plt.close()

    return avgMEP, len(occurrence)/len(y)



#%% loop over all patient files

for intensity in intensities: #make sure to handle special case of 80 and 90 intensity
    timepoints = os. listdir(direct + intensity)
    if len(intensity) == 6:
        intens = intensity[0:3]
    elif len(intensity) == 5:
        intens = intensity[0:2]    
    
    for timepoint in timepoints: 
        subjects = os.listdir(direct + intensity + '/' + timepoint)
       
        for alias in subjects:
            #if dict already exists, load it
            if os.path.exists(direct + alias[0:3] + '_intensity_over_time.json'): 
                with open(direct + alias[0:3] + '_intensity_over_time.json') as json_file:
                    int_over_time = json.load(json_file)
                    #predefine list for timepoints if not yet present
                    if intens not in int_over_time.keys():
                        int_over_time[intens] =[-1,-1,-1,-1,-1]

            #otherwise create empty nested dict
            else:
                int_over_time = collections.defaultdict(dict)
                int_over_time[intens] =[-1,-1,-1,-1,-1]

            #load or create dict with amount of MEPs (occurrence) per timepoint and intensity
            if os.path.exists(direct + alias[0:3] + '_MEP_occurrences.json'): 
                with open(direct + alias[0:3] + '_MEP_occurrences.json') as json_file:
                    MEP_occ = json.load(json_file)
                    #predefine list for timepoints if not yet present
                    if intens not in MEP_occ.keys():
                        MEP_occ[intens] =[-1,-1,-1,-1,-1]

            #otherwise create empty nested dict
            else:
                MEP_occ = collections.defaultdict(dict)
                MEP_occ[intens] =[-1,-1,-1,-1,-1]
                
            subject_data = pd.read_json( direct +  intensity + '/' + timepoint + '/' + alias ).to_dict()
            #check if values are available in dict or if it is NaN 
            if type(subject_data[int(intens)][0]) is dict:
                avgMEP, occurrence = plot_data (subject_data, alias, timepoint, int(intens))
                MEP_occ[intens][chrono[timepoint]] = occurrence
                int_over_time[intens][chrono[timepoint]] = avgMEP
            #If it is NaN:    
            else:    
                print('No data available for {alias}, intensity {intens} %RMT at timepoint {timepoint}'.format(alias = alias[0:3], timepoint= timepoint, intens= intens))

            with open(direct + alias[0:3] + '_intensity_over_time.json','w') as outfile:
                json.dump(int_over_time, outfile)

            with open(direct + alias[0:3] + '_MEP_occurrences.json','w') as outfile:
                json.dump(MEP_occ, outfile)
            

