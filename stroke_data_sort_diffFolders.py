'''5. MEP analysis script
sorts and stores data accoring to label and intensity

Author: Jeannette Nischan
Date of 1st Version: 15th Dec 2022
'''

#%%import tools and libraries
import pandas as pd
import os
import collections

#%% define paths and fixed variables
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO/labelled/'
target_direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO/sorted/'
timepoints = os.listdir(direct)


#%%define functions
def sort_tag(subject_data):
    accept = collections.defaultdict(dict)
    reject = collections.defaultdict(dict)
    no_MEP = collections.defaultdict(dict)
    i = 0
    for epoch in subject_data.keys():
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
        else:
            print('No label available') 
        i += 1       

    return accept, reject, no_MEP           

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

for timepoint in timepoints: 
    subjects = os.listdir(direct + timepoint)
    for alias in subjects:
        subject_data = pd.read_json( direct + timepoint + '/' + alias ).to_dict()
        accept, reject, no_MEP = sort_tag(subject_data)
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
            data[intensity] = accept[intensity]
            df_intens = pd.DataFrame.from_dict(data)
            intensity = str(intensity) + 'RMT'
            if df_intens.empty == False: 
                if os.path.exists(target_direct + 'accepted/' + intensity+ '/' + timepoint  ): # check if folder already exists
                    df_intens.to_json (target_direct + 'accepted/' +  intensity + '/' + timepoint + '/' +  alias )
                else:
                    os.makedirs(target_direct +  'accepted/' + intensity+ '/' + timepoint) # otherwise create folder
                    df_intens.to_json (target_direct + 'accepted/' +  intensity + '/' + timepoint + '/' + alias )

