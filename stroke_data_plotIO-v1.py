'''7. MEP analysis script
preceeded by stroke_data_plots


Author: Jeannette Nischan
Date of 1st Version: 19th Dec 2022
'''

#%%import tools and libraries
import pandas as pd
import os
from os.path import join
import matplotlib.pyplot as plt
import collections
import json
from math import log

#%% define paths and fixed variables if needed
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO/sorted/accepted/'
target_direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO/plots/'
subjects = [name for name in os.listdir(direct) if name.endswith('.json')]
timepoints = ['pre1','post1','pre3','post3','post5']
group_avg = collections.defaultdict(dict)


#%% define functions
# 1. plot I/O curves for each participant(intensity over time) and save images
def plotIO_intens(data, timepoints, alias):
    for intensity in data.keys():
        x = timepoints
        y = data[intensity]
        plt.figure()
        plt.plot(x,y, 'bd')
        plt.title('Input/Output curve for patient: ' + alias + ' at: ' + intensity + '% RMT')
        plt.ylabel('average MEP (peak to peak amplitude) in µV')
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        if os.path.exists(join(target_direct + alias[0:3], 'IO/')): # check if folder already exists
            plt.savefig(join(target_direct + alias[0:3], 'IO', 'IO_' + intensity + '%RMT.png'), format = 'png')  
        else:
            os.makedirs(join(target_direct + alias[0:3],'IO/')) # otherwise create folder
            plt.savefig(join(target_direct + alias[0:3], 'IO', 'IO_' + intensity + '%RMT.png'), format = 'png')
        plt.close()

        #y_log = [log(val) for val in y]  #-> doesn't work if value is 0 (Rewrite code!)
        #plt.figure()
        #plt.plot(x,y_log, 'bd')
        #plt.title('Logarithmic Input/Output curve for patient: ' + alias + ' at: ' + intensity + '% RMT')
        #plt.ylabel('average MEP (log of peak to peak amplitude)')
        #plt.savefig(target_direct + alias + '/' + 'IO_' + intensity + '%RMT_log.png', format = 'png')
        #plt.close()
    

#2. plot I/O curve for all intensities for one timepoint and save images
def plotIO_time(data,alias):
    x= []
    y = {'pre1' : [], 'post1' : [], 'pre3' : [], 'post3' : [], 'post5' : []}
    #y_log = {'pre1' : [], 'post1' : [], 'pre3' : [], 'post3' : [], 'post5' : []}
    ind = 0
    for intensity in range(80,161,10):
        x.append(str(intensity))
        for time in y.keys():
            y[time].append(data[str(intensity)][ind])
            #y_log[time].append(log(data[str(intensity)][ind])) 
        if ind<= 3:
            ind += 1    
    for time in y.keys():
        plt.figure()
        plt.plot(x,y[time], 'bd')  
        plt.title('Input/Output curve for patient: ' + alias + ' at: ' + time)
        plt.ylabel('average MEP (peak to peak amplitude) in µV')
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle() 
        if os.path.exists(join(target_direct + alias[0:3], 'IO/')): # check if folder already exists
            plt.savefig(join(target_direct + alias[0:3], 'IO', 'IO_' + time + '.png'), format = 'png')  
        else:
            os.makedirs(join(target_direct + alias[0:3],'IO/')) # otherwise create folder
            plt.savefig(join(target_direct + alias[0:3], 'IO', 'IO_' + time + '.png'), format = 'png')  
        plt.close() 

        #plt.figure()
        #plt.plot(x,y_log[time], 'bd')  
        #plt.title('Logaritmic Input/Output curve for patient: ' + alias + ' at: ' + time)
        #plt.ylabel('average MEP (log peak to peak amplitude)')
        #if os.path.exists(join(target_direct + alias[0:3], 'IO/')): # check if folder already exists
        #    plt.savefig(join(target_direct + alias[0:3], 'IO', 'IO_' + time + '_log.png'), format = 'png')  
        #else:
        #    os.makedirs(join(target_direct + alias[0:3],'IO/')) # otherwise create folder
        #    plt.savefig(join(target_direct + alias[0:3], 'IO', 'IO_' + time + '_log.png'), format = 'png')       
        #plt.close()




#3. plot I/O curves for group average per intensity (over time) and save images
def groupIO(group_avg, timepoints):
    y =[]
    y_avg = []
    x = []
    for intensity in group_avg.keys():
        for time in group_avg[intensity].keys():
            for i in range(0,len(group_avg[intensity][time])):
                y.append(group_avg[intensity][time][i]) # do not append list!!!
            y_avg.append(sum(group_avg[intensity][time])/len(group_avg[intensity][time]))
            x_avg = timepoints
            for i in range(0,len(group_avg[intensity][time])):
                x.append(time)
            

        plt.figure()
        plt.scatter(x,y)
        plt.plot(x_avg, y_avg)
        plt.title('Input/Output curve for ' + intensity + '% RMT')
        plt.ylabel('average MEP size (peak to peak amplitude) in µV')
        plt.show()



#%% Loop over all patients

#prepare dictionary to collect data for group average
for intensity in range(80,161,10):
        for time in timepoints:
            group_avg[intensity][time] = []


for subject in subjects:
    alias = subject[0:3]
    with open(direct + alias + '_intensity_over_time.json') as json_file:
                    int_over_time = json.load(json_file)

    for intensity in range(80,161,10):
        if str(intensity) not in int_over_time.keys():
            int_over_time[str(intensity)] = [0,0,0,0,0]                

    #plotIO_intens(int_over_time, timepoints, alias)  
    #plotIO_time(int_over_time,alias)

    for intens in int_over_time.keys():
        for time in timepoints:
            if int_over_time[intens][timepoints.index(time)] != 0:
                group_avg[int(intens)][time].append(int_over_time[intens][timepoints.index(time)])

groupIO(group_avg, timepoints)

    


