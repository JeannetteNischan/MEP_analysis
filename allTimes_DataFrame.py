#%%import tools and libraries
import pandas as pd
import json
from math import log10
import numpy as np
import os




#%% define paths and fixed variables if needed
#time = 'V3' 
timepoints = ['V2','V3','V4','V5','V6'] # 1 und 3 bzw in python 0 und 2 
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/sorted/accepted/'
target_direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/allTimes/'
direct_plots = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/allTimes/'
subjects =  [name for name in os.listdir(direct) if name.endswith('time.json')] #['001','003','004','005','006','008','010','011','013','015','018','019']
ipsi_first = ['011','007','005','015','002','008','012','018','003'] #condition 1
kontra_first = ['014','016','009','019','001','010','017','004','013','006'] # condition 2
acceptedSubjects = []
#define constant value to add to all values before log transformation to avoid log10(0) problem
c = 2.5


#%% load data and create dataframe
df_allTimes_MEP = {'subject' : [], 'V2': [], 'V3': [], 'V4':[], 'V5':[],'V6':[],'condition':[], 'intensity':[]}
df_allTimes_Occ = {'subject' : [], 'V2': [], 'V3': [], 'V4':[], 'V5':[],'V6':[],'condition':[], 'intensity':[]}


for subject in subjects:
    with open(direct + subject ) as json_file:
        data = json.load(json_file)

    with open(direct + subject[0:3] + '_MEP_occurrences.json') as jsonfile:
        occ_data = json.load(jsonfile)    

    ID = subject[0:3]
       

    for intensity in data.keys():
        df_allTimes_MEP['intensity'].append(int(intensity))
        df_allTimes_MEP['subject'].append(ID)
        df_allTimes_Occ['intensity'].append(int(intensity))
        df_allTimes_Occ['subject'].append(ID)

        if subject[0:3] in ipsi_first:
            condition = 1
        elif subject[0:3] in kontra_first:
            condition = 2

        df_allTimes_MEP['condition']. append(condition) 
        df_allTimes_Occ['condition']. append(condition)
    
        for timepoint in timepoints:  
            index = timepoints.index(timepoint)
            
            if data[intensity][index] == -1:
                MEP = np.nan
                Occ = np.nan
            elif data[intensity][index] == 0.0:
                MEP = 0  
                Occ = 0
            else: 
                MEP = data[intensity][index]
                Occ = occ_data[intensity][index]

                

            df_allTimes_MEP[timepoint].append(MEP)
            df_allTimes_Occ[timepoint].append(Occ)

           
            
df_allTimes_MEP = pd.DataFrame.from_dict(df_allTimes_MEP)      
df_allTimes_Occ = pd.DataFrame.from_dict(df_allTimes_Occ) 



#check subject column for completeness of data (at least 16 repetitions of subject ID in total)
'''
count = df_allTimes['subject'].value_counts()

acceptedSubjects = set(acceptedSubjects)
for subj in acceptedSubjects:
    if count[subj] < 16:
        indices = df_allTimes.index[df_allTimes['subject'] == subj].tolist()
        df_allTimes = df_allTimes.drop(indices)
    

df_allTimes_MEP_log = df_allTimes.copy()
df_allTimes_MEP_log['MEP size in µV'] = np.log10(df_allTimes_MEP_log['MEP size in µV'] + c)
df_allTimes_MEP_log = df_allTimes_MEP_log.rename(columns={'MEP size in µV':'log transformed MEP size'})
'''

#%% Save data frame
outfile = target_direct + 'allTimes_MEP.pkl'
df_allTimes_MEP.to_pickle(outfile)
outfile = target_direct + 'allTimes_Occ.pkl'
df_allTimes_Occ.to_pickle(outfile)
'''
outfile = target_direct + 'allTimes_MEP_log.pkl'
df_allTimes_MEP_log.to_pickle(outfile)
'''

