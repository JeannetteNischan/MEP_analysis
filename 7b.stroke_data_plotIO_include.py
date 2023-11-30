'''7.1. MEP analysis script
preceeded by stroke_data_plots

followed by 8.1.stroke_data_stats
or 8.2. stroke_data_requested_plots
Author: Jeannette Nischan
Date of 1st Version: 14th Mar 2023
-> alternative timepoint naming <-
'''

#%%import tools and libraries
import os
from os.path import join
import matplotlib.pyplot as plt
import collections
import json
from math import log
from scipy import stats
#import statistics as stat
import numpy as np


#%% define paths and fixed variables if needed
phases = ['0','180']
target_direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/phase_plots/plots/'
direct_IO = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/group_phase/'
#timepoints = ['pre1','post1','pre3','post3','post5']
timepoints = ['V2','V3','V4','V5','V6']



#%% define functions
# 1. plot MEP size developement for each participant (intensity over time) and save images
def plot_IoT(data, data2, timepoints, alias):
    for intensity in data.keys():
        x = timepoints
        y = data[intensity]
        plt.figure()
        plt.plot(x,y, 'bd-')
        plt.title('Input/Output curve for patient: ' + alias + ' at: ' + intensity + '% RMT')
        plt.ylabel('average MEP (peak to peak amplitude) in µV')
        plt.axhline(y=0, xmin=0, xmax=1)
        plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        if os.path.exists(join(target_direct + alias[0:3], 'IO/')): # check if folder already exists
            plt.savefig(join(target_direct + alias[0:3], 'IO', 'IoT_' + intensity + '%RMT.png'), format = 'png')  
        else:
            os.makedirs(join(target_direct + alias[0:3],'IO/')) # otherwise create folder
            plt.savefig(join(target_direct + alias[0:3], 'IO', 'IoT_' + intensity + '%RMT.png'), format = 'png')
        plt.close()

        #plot MEP occurence (relative to all accepted trials) over time
        y = data2[intensity]
        plt.figure()
        plt.plot(x,y, 'gd-')
        plt.title('Relative MEP occurrence for patient: ' + alias + ' at: ' + intensity + '% RMT')
        plt.ylabel('amount of MEP occurrences in all accepted trials')
        plt.axhline(y=0, xmin=0, xmax=1)
        plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        if os.path.exists(join(target_direct + alias[0:3], 'IO/')): # check if folder already exists
            plt.savefig(join(target_direct + alias[0:3], 'IO', 'occurrence_' + intensity + '%RMT.png'), format = 'png')  
        else:
            os.makedirs(join(target_direct + alias[0:3],'IO/')) # otherwise create folder
            plt.savefig(join(target_direct + alias[0:3], 'IO', 'occurrence_' + intensity + '%RMT.png'), format = 'png')
        plt.close()

        #log transform MEP sizes
        y_log = []
        for val in y:
            if val == 0:
                y_log.append(0)
            elif val == -1:
                y_log.append(-1)
            else:
                y_log.append(log(val))

        #plot with log transformed MEP sizes            
        plt.figure()
        plt.plot(x,y_log, 'rd-')
        plt.title('Logarithmic Input/Output curve for patient: ' + alias + ' at: ' + intensity + '% RMT')
        plt.ylabel('average MEP (log of peak to peak amplitude)')
        plt.axhline(y=0, xmin=0, xmax=1)
        plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
        plt.savefig(target_direct + alias + '/IO/' +  'IoT_' + intensity + '%RMT_log.png', format = 'png')
        plt.close()
    

#2. plot I/O curve for all intensities for one timepoint and save images
def plot_IO(data, data2, alias):
    x= []
    y = {'pre1' : [], 'post1' : [], 'pre3' : [], 'post3' : [], 'post5' : []}
    y2 = {'pre1' : [], 'post1' : [], 'pre3' : [], 'post3' : [], 'post5' : []}
    y_log = {'pre1' : [], 'post1' : [], 'pre3' : [], 'post3' : [], 'post5' : []}
    
    for intensity in range(80,161,10):
        x.append(str(intensity))
        ind = 0
        for time in y.keys():
            y[time].append(data[str(intensity)][ind])
            y2[time].append(data2[str(intensity)][ind])
            if data[str(intensity)][ind] == 0:
                y_log[time].append(0)
            elif data[str(intensity)][ind] == -1:
                y_log[time].append(-1)
            else:
                y_log[time].append(log(data[str(intensity)][ind])) 
            if ind<= 3:
                ind += 1    

    for time in y.keys():
        plt.figure()
        plt.plot(x,y[time], 'bd-')  
        plt.title('Input/Output curve for patient: ' + alias + ' at: ' + time)
        plt.ylabel('average MEP (peak to peak amplitude) in µV')
        plt.axhline(y=0, xmin=0, xmax=1)
        plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle() 
        if os.path.exists(join(target_direct + alias[0:3], 'IO/')): # check if folder already exists
            plt.savefig(join(target_direct + alias[0:3], 'IO', 'IO_' + time + '.png'), format = 'png')  
        else:
            os.makedirs(join(target_direct + alias[0:3],'IO/')) # otherwise create folder
            plt.savefig(join(target_direct + alias[0:3], 'IO', 'IO_' + time + '.png'), format = 'png')  
        plt.close() 

        #plot occurences for intensities at one timepoint
        plt.figure()
        plt.plot(x,y2[time], 'gd-')  
        plt.title('Relative MEP occurrence for patient: ' + alias + ' at: ' + time)
        plt.ylabel('MEP occurrence (relative to all accepted trials)')
        plt.axhline(y=0, xmin=0, xmax=1)
        plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
        if os.path.exists(join(target_direct + alias[0:3], 'IO/')): # check if folder already exists
            plt.savefig(join(target_direct + alias[0:3], 'IO', 'occurrence_' + time + '.png'), format = 'png')  
        else:
            os.makedirs(join(target_direct + alias[0:3],'IO/')) # otherwise create folder
            plt.savefig(join(target_direct + alias[0:3], 'IO', 'occurrence_' + time + '.png'), format = 'png')       
        plt.close()

        #plot with log transformed MEP sizes
        plt.figure()
        plt.plot(x,y_log[time], 'rd-')  
        plt.title('Logarithmic Input/Output curve for patient: ' + alias + ' at: ' + time)
        plt.ylabel('average MEP (log peak to peak amplitude)')
        plt.axhline(y=0, xmin=0, xmax=1)
        plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
        if os.path.exists(join(target_direct + alias[0:3], 'IO/')): # check if folder already exists
            plt.savefig(join(target_direct + alias[0:3], 'IO', 'IO_' + time + '_log.png'), format = 'png')  
        else:
            os.makedirs(join(target_direct + alias[0:3],'IO/')) # otherwise create folder
            plt.savefig(join(target_direct + alias[0:3], 'IO', 'IO_' + time + '_log.png'), format = 'png')       
        plt.close()


#3. plot MEP size development for group average per intensity (over time) and save images
def group_plots(group_avg, MEP_occ, timepoints):
    groupAVG = collections.defaultdict(dict)

    for time in timepoints:
        for intensity in range(80,161,10):
            groupAVG[time][intensity] = []
            
            
    
    x_avg = timepoints
    for intensity in group_avg.keys():
        y =[]
        y_avg = []
        y_occ = []
        x = []
        x_occ = []
        for time in group_avg[intensity].keys():
            for i in range(0,len(group_avg[intensity][time])):
                y.append(group_avg[intensity][time][i]) # do not append list!!!
                y_occ.append(MEP_occ[intensity][time][i])
            y_avg.append(sum(group_avg[intensity][time])/len(group_avg[intensity][time]))
            groupAVG[time][intensity].append(sum(group_avg[intensity][time])/len(group_avg[intensity][time]))
            groupAVG[time][intensity].append(stats.sem(group_avg[intensity][time]))
            for i in range(0,len(group_avg[intensity][time])):
                x.append(time)
            for i in range(0,len(MEP_occ[intensity][time])):
                x_occ.append(time)   
            print('There are occurrence values for {} subjects at {} and {} %RMT and phase {}'.format(len(MEP_occ[intensity][time]), time, intensity, phase))     
            
        #3.1 plot Input/Output curve for each intensity over time with group average
        plt.figure()
        plt.scatter(x,y, marker='o', color = 'b')
        plt.plot(x_avg, y_avg, marker='D', color = 'orange', linestyle='-')
        plt.title('Input/Output curve for ' + str(intensity) + '% RMT (ipsilesional/contralateral)')
        plt.ylabel('average MEP size (peak to peak amplitude) in µV')
        plt.axhline(y=0, xmin=0, xmax=1)
        plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
        #plt.show()
        if os.path.exists(direct_IO): # check if folder already exists
            plt.savefig(join(direct_IO + str(intensity) + '_group_IoT.png'), format = 'png')  
        else:
            os.makedirs(direct_IO) # check if folder already exists
            plt.savefig(join(direct_IO + str(intensity) + '_group_IoT.png'), format = 'png') 
        plt.close() 


        #3.2 plot logarithmic MEP sizes
        y_log = []
        y_logavg = []
        for val in y:
            if val == 0:
                y_log.append(0)
            elif val == -1:
                y_log.append(-1)
            else:
                y_log.append(log(val))

        for time in timepoints:
            x = np.array(x)
            y_log = np.array(y_log)
            ind = np.where(x == time)
            ind = list(ind[0])
            log_time = list(y_log[ind])
            y_logavg.append(sum(log_time)/len(log_time)) 
                 

        plt.figure()
        plt.scatter(x,y_log, marker='o', color = 'g')
        plt.plot(x_avg, y_logavg, marker='D', color = 'r', linestyle='-')
        plt.title('Logarithmic Input/Output curve for ' + str(intensity) + '% RMT (ipsilesional/contralateral)')
        plt.ylabel('log of average MEP size (peak to peak amplitude) in µV')
        plt.axhline(y=0, xmin=0, xmax=1)
        plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
        #plt.show()
        if os.path.exists(direct_IO): # check if folder already exists
            plt.savefig(join(direct_IO + str(intensity) + '_log_MEPs.png'), format = 'png')  
        else:
            os.makedirs(direct_IO) # check if folder already exists
            plt.savefig(join(direct_IO + str(intensity) + '_log_MEPs.png'), format = 'png')
        plt.close()


        #3.3 plot relative MEP occurrences
        y_occavg = []
        for time in timepoints:
            x_occ = np.array(x_occ)
            y_occ = np.array(y_occ)
            ind = np.where(x == time)
            ind = list(ind[0])
            occ_time = list(y_occ[ind])
            y_occavg.append(sum(occ_time)/len(occ_time))
            groupAVG[time][intensity].append((sum(occ_time)/len(occ_time)))
            groupAVG[time][intensity].append(stats.sem(occ_time))


        plt.figure()
        plt.scatter(x_occ,y_occ, marker='o', color = 'c')
        plt.plot(x_avg, y_occavg, marker='D', color = 'y', linestyle='-')
        plt.title('Relative MEP occurrences for ' + str(intensity) + '% RMT (ipsilesional/contralateral)')
        plt.ylabel('relative MEP occurrences for all accepted trials')
        plt.axhline(y=0, xmin=0, xmax=1)
        plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
        #plt.show()
        if os.path.exists(direct_IO): # check if folder already exists
            plt.savefig(join(direct_IO + str(intensity) + '_MEP_occ.png'), format = 'png')  
        else:
            os.makedirs(direct_IO) # check if folder already exists
            plt.savefig(join(direct_IO + str(intensity) + '_MEP_occ.png'), format = 'png')
        plt.close()

    return groupAVG


#4. plot I/O curves (all intensities) for each timepoint
def group_IO(group_avg, timepoints):
    groupLOG = collections.defaultdict(dict)
    for time in timepoints:
        for intensity in range(80,161,10):
            groupLOG[time][intensity] = []

    x = []
    y = []
    y_log = []
    x_avg = group_avg.keys()
    for time in timepoints:
        y_avg = []
        y_log_avg = []
        std_err = []
        std_err_log = []
        for intensity in group_avg.keys():
            for i in range(0,len(group_avg[intensity][time])):
                y.append(group_avg[intensity][time][i])
                y_log.append(log(group_avg[intensity][time][i] + 1))  # to avoid error of log(0) -> Maybe change to 2 because log(1) = 0 
                x.append(intensity)
            y_avg.append(sum(group_avg[intensity][time])/len(group_avg[intensity][time]))


        for intensity in group_avg.keys():
            y_sem_log = [log(val+1) for val in group_avg[intensity][time]]
            y_log_avg.append(sum(y_sem_log)/len(y_sem_log))
            groupLOG[time][intensity].append(sum(y_sem_log)/len(y_sem_log))
            std_err.append(stats.sem(group_avg[intensity][time]))
            std_err_log.append(stats.sem(y_sem_log))
            groupLOG[time][intensity].append(stats.sem(y_sem_log))
            print('There are ptp values for for {} subjects at {} and {} %RMT and phase {}'.format(len(group_avg[intensity][time]), time, intensity, phase))


        #for intensity in group_avg.keys():
        #    x = np.array(x)
        #    y_log = np.array(y_log)
        #    ind = np.where(x == time)
        #    ind = list(ind[0])
        #    log_time = list(y_log[ind])
        #   y_log_avg.append(sum(log_time)/len(log_time))

        plt.figure()
        plt.scatter(x,y, marker='o', color = 'orange')
        plt.plot(x_avg, y_avg, marker='D', color = 'b', linestyle = '-')
        plt.errorbar(x_avg,y_avg, yerr = std_err)
        plt.title('Input/Output curve for ' + str(time) + '\n individual means and group average(ipsilesional/contralateral)')
        plt.ylabel('average MEP size in µV')
        plt.xlabel('% RMT')
        plt.axhline(y=0, xmin=0, xmax=1)
        plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
        #plt.show()
        if os.path.exists(direct_IO): # check if folder already exists
            plt.savefig(join(direct_IO + str(time) + '_IO.png'), format = 'png')  
        else:
            os.makedirs(direct_IO) # check if folder already exists
            plt.savefig(join(direct_IO + str(time) + '_IO.png'), format = 'png')
        plt.close()

        plt.figure()
        plt.plot(x_avg,y_log_avg, marker='D', color = 'b', linestyle = '-')
        plt.errorbar(x_avg,y_log_avg, yerr = std_err_log)
        plt.title('logarithmic Input/Output curve for ' + str(time) + '\n group average(ipsilesional/contralateral)')
        plt.ylabel('log of MEP size')
        plt.xlabel('% RMT')
        plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
        #plt.show()
        if os.path.exists(direct_IO): # check if folder already exists
            plt.savefig(join(direct_IO + str(time) + '_logIO.png'), format = 'png')  
        else:
            os.makedirs(direct_IO) # check if folder already exists
            plt.savefig(join(direct_IO + str(time) + '_logIO.png'), format = 'png')
        plt.close()

    return groupLOG    

            

#%% Loop over all patients

#prepare dictionary to collect data for group average


for phase in phases:
    group_avg = collections.defaultdict(dict)
    group_MEP_occ = collections.defaultdict(dict)
    for intensity in range(80,161,10):
        for time in timepoints:
            group_avg[intensity][time] = []
            group_MEP_occ[intensity][time] = []
    
    direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/sorted_phase/' + phase + '/accepted/'
    subjects = [name for name in os.listdir(direct) if name.endswith('time.json')]
    for subject in subjects:
        alias = subject[0:3]
        with open(direct + alias + '_intensity_over_time.json') as json_file:
                        int_over_time = json.load(json_file)

        with open(direct + alias + '_MEP_occurrences.json') as json_file:
                        MEP_occ = json.load(json_file)

        for intensity in range(80,161,10):
            if str(intensity) not in int_over_time.keys():
                int_over_time[str(intensity)] = [0,0,0,0,0]                

    #plot_IoT(int_over_time, MEP_occ, timepoints, alias)  
    #plot_IO(int_over_time, MEP_occ, alias)

        for intens in int_over_time.keys():
            i = 0
            for time in timepoints:
                if int_over_time[intens][timepoints.index(time)] >= 0:
                    group_avg[int(intens)][time].append(int_over_time[intens][timepoints.index(time)])
                    i += 1

        for intens in MEP_occ.keys():
            i = 0
            for time in timepoints:
                if MEP_occ[intens][timepoints.index(time)] >= 0:
                    group_MEP_occ[int(intens)][time].append(MEP_occ[intens][timepoints.index(time)])
                    i += 1

    groupAVG = group_plots(group_avg, group_MEP_occ, timepoints)
    groupLOG = group_IO(group_avg, timepoints)

    with open('/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/phase' + phase + '_groupAVG.json','w') as outfile:
        json.dump(groupAVG,outfile)

    with open('/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/phase' + phase + '_groupLOG.json','w') as outfile:
        json.dump(groupLOG,outfile)    

    with open('/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/phase' + phase + '_group_avgs.json','w') as outfile:
        json.dump(group_avg,outfile)

    with open('/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/phase' + phase + '_group_MEP_occ.json','w') as outfile:
        json.dump(group_MEP_occ,outfile)
    


