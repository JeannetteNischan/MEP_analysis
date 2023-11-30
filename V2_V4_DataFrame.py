#%%import tools and libraries
import pandas as pd
import json
from math import log10
import numpy as np
import os




#%% define paths and fixed variables if needed
#time = 'V3' 
timepoints = ['V2','V4'] # 1 und 3 bzw in python 0 und 2 
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/sorted/accepted/'
target_direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/V2_V4/'
direct_plots = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/V2_V4/'
subjects = [name for name in os.listdir(direct) if name.endswith('time.json')]
acceptedSubjects = []
#define constant value to add to all values before log transformation to avoid log10(0) problem
c = 2.5


#%% load data and create dataframe
df_V2V4 = {'subject' : [], 'timepoint' : [], 'intensity in %RMT':[], 'MEP size in µV' : [], 'occurrence':[]}

for subject in subjects:
    with open(direct + subject) as json_file:
        data = json.load(json_file)
    for intensity in data.keys():
        if data[intensity][0] != -1:
            ID = subject[0:3]
            timepoint = 'pre/V2'

            with open(direct + ID + '_MEP_occurrences.json') as occ_file:
                occData =json.load(occ_file)
            occ = occData[intensity][0]     
            

            if data[intensity][0] == 0.0:
                MEP = 0
            else: 
                    MEP = data[intensity][0]
            

            df_V2V4['subject'].append(ID) 
            df_V2V4['timepoint'].append(timepoint)
            df_V2V4['intensity in %RMT'].append(int(intensity))
            df_V2V4['MEP size in µV'].append(MEP)
            df_V2V4['occurrence'].append(occ)


            acceptedSubjects.append(ID)

            if data[intensity][2] != -1:
                ID = subject[0:3]
                timepoint = 'post/V4' 

                occ = occData[intensity][2]     
                
                if data[intensity][2] == 0.0:
                    MEP = 0
                else: 
                    MEP = data[intensity][2]
                

                df_V2V4['subject'].append(ID) 
                df_V2V4['timepoint'].append(timepoint)
                df_V2V4['intensity in %RMT'].append(int(intensity))
                df_V2V4['MEP size in µV'].append(MEP)
                df_V2V4['occurrence'].append(occ)

           
# transform dict to dataframe
df_V2V4 = pd.DataFrame.from_dict(df_V2V4)

#check subject column for completeness of data (at least 16 repetitions of subject ID in total)
count = df_V2V4['subject'].value_counts()

acceptedSubjects = set(acceptedSubjects)
for subj in acceptedSubjects:
    if count[subj] < 16:
        indices = df_V2V4.index[df_V2V4['subject'] == subj].tolist()
        df_V2V4 = df_V2V4.drop(indices)
    

df_V2V4_log = df_V2V4.copy()
df_V2V4_log['MEP size in µV'] = np.log10(df_V2V4_log['MEP size in µV'] + c)
df_V2V4_log = df_V2V4_log.rename(columns={'MEP size in µV':'log transformed MEP size'})
df_V2V4_log['occurrence'] = np.log10(df_V2V4_log['occurrence'] + c)
df_V2V4_log = df_V2V4_log.rename(columns={'occurrence':'log transformed occurrence'})

#%% Save data frame
outfile = target_direct + 'pre-post.pkl'
df_V2V4.to_pickle(outfile)
outfile = target_direct + 'pre-post_log.pkl'
df_V2V4_log.to_pickle(outfile)

