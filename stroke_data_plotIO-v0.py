'''7. MEP analysis script
preceeded by stroke_data_plots


Author: Jeannette Nischan
Date of 1st Version: 19th Dec 2022
'''

#%%import tools and libraries
import pandas as pd
import os
import matplotlib.pyplot as plt
import collections
import json
from math import log

#%% define paths and fixed variables if needed
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO/sorted/accepted/'
target_direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO/plots/'
subjects = [name for name in os.listdir(direct) if name.endswith('.json')]
timepoints = ['pre1','post1','pre3','post3','post5']


#%% define functions
# 1. plot I/O curves for each participant(intensity over time) and save images
def plotIOintens(data, timepoints, alias):
    for intensity in data.keys():
        x = timepoints
        y = data[intensity]
        plt.figure()
        plt.plot(x,y)
        plt.title('Input/Output curve for patient: ' + alias + ' at: ' + intensity + '% RMT')
        plt.ylabel('average MEP (peak to peak amplitude) in µV')
        plt.savefig(target_direct + alias + '/' + 'IO_' + intensity + '%RMT.png', format = 'png')
        plt.close()


#2. plot I/O curve for all intensities for one timepoint and save images
def plotIOtime(data):
    x= []
    y = {'pre1' : [], 'post1' : [], 'pre3' : [], 'post3' : [], 'post5' : []}
    ind = 0
    for intensity in range(80,161,10):
        x.append(str(intensity))
        for time in y.keys():
            y[time].append(data[str(intensity)][ind])
        if ind<= 3:
            ind += 1    
    for time in y.keys():
        plt.figure()
        plt.plot(x,y[time])  
        plt.title('Input/Output curve for patient: ' + alias + ' at: ' + time)
        plt.ylabel('average MEP (peak to peak amplitude) in µV')  
        plt.savefig(target_direct + alias + '/' + 'IO_' + time + '.png', format = 'png')    
        plt.close() 

      



#3. plot I/O curves for group average per intensity (over time) and save images



#%% Loop over all patients
for subject in subjects:
    alias = subject[0:3]
    with open(direct + alias + '_intensity_over_time.json') as json_file:
                    int_over_time = json.load(json_file)

    plotIOintens(int_over_time, timepoints, alias)  
    plotIOtime(int_over_time)              

