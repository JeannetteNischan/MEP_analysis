'''5. MEP analysis script
sorts and stores data accoring to label and intensity
!! -> This special script includes trials with no MEP as ptp_amp and latency 0 <- !!
followed by stroke_data_plots_include
Author: Jeannette Nischan
Date of 1st Version: 22nd Dec 2022
'''

#%%import tools and libraries
import pandas as pd
import os
import collections
import json

#%% define paths and fixed variables
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO/labelled_phase/'
target_direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/sorted_phase/'
phases = os.listdir(direct)
trial_info = collections.defaultdict(dict)


#%%define functions
def sort_tag(subject_data,alias):
    accept = collections.defaultdict(dict)
    reject = collections.defaultdict(dict)
    no_MEP = collections.defaultdict(dict)
    i = 0
    for epoch in subject_data.keys():
        trials = len(subject_data.keys())
        trial = subject_data[epoch].copy()

        if trial['label'] == 'accept':

            if trial['latency'] < 15 :
                trial['latency'] = 15
            del trial['label']
            accept[i]= trial
    
        elif trial['label'] == 'reject':
            del trial['label']
            reject[i]= trial   

        elif trial['label'] == 'no MEP':
            del trial['label']
            no_MEP[i]= trial
            accept[i] = trial
            if accept[i]['latency'] < 15 :
                accept[i]['latency'] = 15
            accept[i]['ptp_amp'] = 0
            accept[i]['latency'] = 0       
        else:
            print('No label available') 
        i += 1       

    t_MEP = len(accept.keys())
    tn_MEP = len(no_MEP.keys())
    t_rej = len(reject.keys())
    if t_MEP == 0:
        accept = {'NaN'}
    print('Of {allTrials} trials for {subject}, {trialAccept} remain, {trialMEP} with MEP. \n {trialReject} trials were rejected due to artefacts (preactivation) or noisy data'.format(subject = alias, allTrials = trials, trialAccept = t_MEP, trialMEP = t_MEP-tn_MEP, trialReject = t_rej))
    string = ('Of {allTrials} trials for {subject}, {trialAccept} remain, {trialMEP} with MEP. {trialReject} trials were rejected due to artefacts (preactivation) or noisy data'.format(subject = alias, allTrials = trials, trialAccept = t_MEP, trialMEP = t_MEP-tn_MEP, trialReject = t_rej))
    return accept, reject, no_MEP, string          

def sort_intensity(accepted):
    accept_sort = collections.defaultdict(dict)
    for i in range (80,161,10):
            accept_sort[i] = []
    for trial in accepted.keys():
        for i in range (80,161,10):
            if accepted[trial]['stim_intens'] == i:
                accept_sort[i].append(accepted[trial]) 
            

    return accept_sort

#def avg_MEP(data):
    #avgMEP = []
    #for trial in data.keys():
        #avgMEP.append(data[trial]['ptp_amp'])
    #avgMEP = sum(avgMEP)/len(avgMEP)
    #data['avgMEP'] = avgMEP

    #return data


#%% loop over all patient files
for phase in phases:
    timepoints = os.listdir(direct + phase + '/')
    for timepoint in timepoints: 
        subjects = os.listdir(direct + phase + '/' + timepoint)
        trial_info[timepoint] = []
        for alias in subjects:
            subject_data = pd.read_json( direct + phase + '/' + timepoint + '/' + alias ).to_dict()
            print('For subject ' + alias[0:3] + ' at timepoint ' + timepoint + ' :')
            accept, reject, no_MEP, string = sort_tag(subject_data, alias[0:3])
            trial_info[timepoint].append(string)
            if accept != {'NaN'}:
                accept = sort_intensity(accept)
                #accept = avg_MEP (accept)

            # create dataframe from dict and store as json file 
            #first check if dict is empty
            if reject:
                df_rej = pd.DataFrame.from_dict(reject)
                if os.path.exists(target_direct + 'rejected/' + timepoint): # check if folder already exists
                    df_rej.to_json (target_direct + 'rejected/' +  timepoint + '/' + alias )
                else:
                    os.makedirs(target_direct +  'rejected/' + timepoint) # otherwise create folder
                    df_rej.to_json (target_direct + 'rejected/' +  timepoint + '/' + alias )
        
            if no_MEP:
                df_no = pd.DataFrame.from_dict(no_MEP)
                if os.path.exists(target_direct + 'no_MEP/' + timepoint): # check if folder already exists
                    df_no.to_json (target_direct + 'no_MEP/' +  timepoint + '/' + alias )
                else:
                    os.makedirs(target_direct +  'no_MEP/' + timepoint) # otherwise create folder
                    df_no.to_json (target_direct + 'no_MEP/' +  timepoint + '/' + alias )

            for intensity in range(80,161,10): 
                data = {}
                if accept == {'NaN'} or accept[intensity] == []:
                    data[intensity] = list({'NaN'})
                    df_intens = pd.DataFrame.from_dict(data)
                    intensity = str(intensity) + 'RMT' 
                    if os.path.exists(target_direct + phase + '/accepted/' + intensity+ '/' + timepoint  ): # check if folder already exists
                        df_intens.to_json (target_direct + phase + '/accepted/' +  intensity + '/' + timepoint + '/' +  alias )
                    else:
                        os.makedirs(target_direct + phase + '/accepted/' + intensity+ '/' + timepoint) # otherwise create folder
                        df_intens.to_json (target_direct + phase + '/accepted/' +  intensity + '/' + timepoint + '/' + alias )
                else:
                    data[intensity] = accept[intensity]
                    df_intens = pd.DataFrame.from_dict(data)
                    intensity = str(intensity) + 'RMT' 
                    if os.path.exists(target_direct + phase + '/accepted/' + intensity+ '/' + timepoint  ): # check if folder already exists
                        df_intens.to_json (target_direct + phase + '/accepted/' +  intensity + '/' + timepoint + '/' +  alias )
                    else:
                        os.makedirs(target_direct +  phase + '/accepted/' + intensity+ '/' + timepoint) # otherwise create folder
                        df_intens.to_json (target_direct + phase + '/accepted/' +  intensity + '/' + timepoint + '/' + alias )

with open('/home/jeanettenischan/Data/data_INTENS_TMS/trial_info.json', 'w') as file:
            json.dump(trial_info, file)