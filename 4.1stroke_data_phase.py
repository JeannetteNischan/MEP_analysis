'''4.1. MEP analysis script
for extraction of the phase (0 or 180°) from the matfiles
preceeded by script 4 'stroke_data_visual' and followed by 
5 'stroke_data_sort'
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
from os.path import join

#%% 2. key of interest (recorded physiological data)
direct  = '/home/jeanettenischan/Data/data_INTENS_TMS/data/' #main folder with all subject subfolder
target_direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO/labelled_phase/'#folder to store processed data
direct_dict = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO/labelled/'
direct_plot = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/phase_plots/'

# Create a list of folder names as subject id
subject_ids = os.listdir(direct)
timepoints = os.listdir(direct_dict)

# Create a file where possible problems are documented
error_messages = collections.defaultdict(dict) #predefine empty nested dictionary



def load_matfiles(alias, timepoint):
    #alias = '010'    #for test purposes in case of crashes
    #timepoint = 'pre1'
    datapath = direct + alias + '/' + timepoint + '/IO_ipsilesional.mat'
    if os.path.isfile(datapath):
        data = io.loadmat(datapath)
        print('--> ' + alias + ' at ' + timepoint + ' <--')
        if 'spongebob_timeseries' in data.keys():
            sp_marker = data["spongebob_timeseries"]
            sp_marker = np.squeeze(sp_marker)
            phase180 = np.where(sp_marker[:,12] == 180)
            phase0 = np.where(sp_marker[:,12] == 0)
            plt.figure()
            plt.plot(sp_marker[:,12])
            plt.plot(sp_marker[:,11])
            plt.title('Subject {} at timepoint {}'.format(alias,timepoint))
            #plt.show()
            if os.path.exists(direct_plot): # check if folder already exists
                plt.savefig(join(direct_plot + str(alias) + '_phase.png'), format = 'png')  
            else:
                os.makedirs(direct_plot) # check if folder already exists
                plt.savefig(join(direct_plot + str(alias) + '_phase.png'), format = 'png') 
            plt.close()
            if len(phase180[0]) >= 10 and len(phase0[0]) >= 10:
                tms = data['tms_artifact'].size
                if tms > 180:
                    tms = 180
                    print('More than 180 trials/trigger for {} at {}'.format(alias, timepoint))
                    error_meassages[timepoint][alias] = 'There were more than 180 trials (trigger)'
                trigger = np.where(sp_marker[:,11] == 1)
                trigger_amount = len(trigger[0])
                if trigger_amount < 20:   #check if there is a sufficient amount of triggers
                    print('Less than 20 triggers')
                    error_messages[timepoint][alias] = 'Less than 20 triggers for '+ alias 
                    trigger0 = []
                    trigger180 = []
                    tms = []
                    go_on = 'no'
                    return error_messages, trigger0, trigger180, tms, go_on
                diff = trigger[0].size -tms
                trigger = trigger[0][diff:]
                phase_info = sp_marker[trigger[0]-100:,12]
                phase0 = np.where(phase_info == 0)
                phase180 = np.where(phase_info == 180)
                if len(phase180[0]) >= 10 and len(phase0[0]) >= 10:
                    phase_change = phase180[0][0]
                    trigger_diff = trigger[0]      #the difference between old and new trigger values is the first value of trigger (new 0)
                    trigger_new = [item - trigger_diff for item in trigger]  # substract this value from all items in trigger to 'reset'
                    index = np.where(trigger_new >= phase_change) #find the indices of 180
                    trigger_0 = trigger_new[0:index[0][0]] #all triggers from 0 to index of phase change belong to phase 0
                    trigger0 = len(trigger_0) # how many trials with phase 0 
                    i= 500
                    while trigger0 < 10: # if trigger is set too early and 0 values are interrupted
                        phase_info = sp_marker[trigger[0]+i :,12] # adjust cut point /shift forward
                        phase0 = np.where(phase_info == 0)
                        phase180 = np.where(phase_info == 180)
                        phase_change = phase180[0][0]
                        trigger_diff = trigger[0]      #the difference between old and new trigger values is the first value of trigger (new 0)
                        trigger_new = [item - trigger_diff for item in trigger]  # substract this value from all items in trigger to 'reset'
                        index = np.where(trigger_new >= phase_change) #find the indices of 180
                        trigger_0 = trigger_new[0:index[0][0]] #all triggers from 0 to index of phase change belong to phase 0
                        trigger0 = len(trigger_0) # how many trials with phase 0 
                        i += 500

                    trigger_180 = trigger_new[index[0][0]:]
                    trigger180 = len(trigger_180)
                    go_on = 'yes'

                else: 
                    print(' No phase 180° or 0° for '+ alias +' at ' + timepoint) 
                    error_messages[timepoint][alias] = 'No values phase 180 or 0 for '+ alias 
                    trigger0 = []
                    trigger180 = []
                    tms = []
                    go_on = 'no'

            else:
                print(' No phase 180° or 0° for '+ alias +' at ' + timepoint) 
                error_messages[timepoint][alias] = 'No values phase 180 or 0 for '+ alias 
                trigger0 = []
                trigger180 = []
                tms = []
                go_on = 'no'
            
        else:
            print('No datastream with markers for ' + alias + ' at ' + timepoint) 
            error_messages[timepoint][alias] = 'No datastream with markers for ' + alias     
            trigger0 = []
            trigger180 = []
            tms = []
            go_on = 'no'

    else:
        print('No data available for {} at {}'.format(alias,timepoint)) 
        error_messages[timepoint][alias] = 'No data for ' + alias 
        trigger0 = []
        trigger180 = []
        tms = []
        go_on = 'no'

    return error_messages, trigger0, trigger180, tms, go_on    


def load_dict(alias, timepoint, trigger0, tms):
    dict_0 = {}
    dict_180 = {}
    subject_dict = pd.read_json( direct_dict + timepoint + '/' + alias).to_dict()
    last_trial = len(subject_dict)
    print('There are {} trials in the dict of subject {} at {}'.format(len(subject_dict), alias, timepoint))
    if tms < len(subject_dict):
        diff = len(subject_dict) - tms
        for i in range(1,diff+1): # +1 due to python indexing (to include all values)
            del subject_dict[i]   # remove trial from the front until size matches
        list0 = range(diff+1,diff+trigger0+1)  #recalibrate list to trials, starts with first remaining trial
        list180 = range(diff+trigger0+2,last_trial)    
    else:
        list0 = range(1,trigger0+1)
        list180 = range(trigger0+1,len(subject_dict))
    print('{} trials remain'.format(len(subject_dict)))
    for trial in subject_dict.keys():
        if trial in list0:
            dict_0[str(trial)] = subject_dict[trial] 
        elif trial in list180:
            dict_180[str(trial)] = subject_dict[trial]
    print('There are {} values in the dictionary for phase 0'.format(len(dict_0)))
    print('There are {} values in the dictionary for phase 180'.format(len(dict_180)))

    return dict_0, dict_180

        


#%% loop over all patient files

for timepoint in timepoints:
    for alias in subject_ids:
        error_meassages, trigger0, trigger180, tms, go_on = load_matfiles(alias, timepoint)
        print('There are {} values for phase 0'.format(trigger0))
        print('There are {} values for phase 180'.format(trigger180))
        with open('/home/jeanettenischan/Data/data_INTENS_TMS/problems.json' , 'w') as outfile:
            json.dump(error_messages, outfile) 

        alias = alias +'.json'
        directory = os.listdir(direct_dict + timepoint)
        if go_on == 'yes'and alias in directory:
            dict_0 ,dict_180 = load_dict(alias, timepoint, trigger0, tms)
            df_0 = pd.DataFrame.from_dict(dict_0) 
            df_180 = pd.DataFrame.from_dict(dict_180) 
            if os.path.exists(target_direct + '0/' + timepoint): # check if folder already exists
                df_0.to_json (target_direct + '0/' + timepoint + '/' + alias )
            else:
                os.makedirs(target_direct + '0/' + timepoint) # otherwise create folder
                df_0.to_json (target_direct +  '0/' + timepoint + '/' + alias )

            if os.path.exists(target_direct + '180/' + timepoint): # check if folder already exists
                df_180.to_json (target_direct + '180/' + timepoint + '/' + alias )
            else:
                os.makedirs(target_direct + '180/' + timepoint) # otherwise create folder
                df_180.to_json (target_direct +  '180/' + timepoint + '/' + alias )    

        