#%%import tools and libraries
import pandas as pd



#%% define paths and fixed variables if needed
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/allTimes/'

#%% load needed dataframes
file_name = direct + 'allTimes_MEP_zMEP.csv'
df_completeMEP = pd.read_csv(file_name)

file_name1 = direct + 'allTimes_longF_Occ.csv'
df_completeOcc = pd.read_csv(file_name1)

file_name2 = direct + 'contralesional_allTimes_MEP_zMEP.csv'
df_contralesional = pd.read_csv(file_name2)

file_name3 = direct + 'karolina_df_occ.csv'
df_contra_occ = pd.read_csv(file_name3)


#%% prepare my dataframes, reversing anonymisation with number code
code_list = pd.read_csv('/home/jeanettenischan/Data/data_INTENS_TMS/SubjectCodeList.csv')
code_list = code_list.transpose()
code_list = code_list[0].to_dict()
# turn subject numbers into string for replacement
df_completeMEP['subject'] = df_completeMEP['subject'].apply(str)
df_completeOcc['subject'] = df_completeOcc['subject'].apply(str)

#replace values with names
df_completeMEP = df_completeMEP.replace({'subject':code_list})
df_completeOcc = df_completeOcc.replace(code_list)


#%% prepare carolinas dataframes for conversion
time_code = {'Pre1':'V2', 'Post1':'V3', 'Pre3':'V4', 'Post3':'V5', 'Post5':'V6'}

#replace timepoint names
df_contralesional = df_contralesional.replace({'Timepoint':time_code})
df_contra_occ = df_contra_occ.replace({'Timepoint':time_code})

#%% combine dataframes
# sort both dataframes by subject name, intensity and timepoint, adapting the index (by ignore_index=False)
df_completeMEP = df_completeMEP.sort_values(by=['subject','intensity','Timepoint'], ignore_index=True)
df_completeOcc = df_completeOcc.sort_values(by=['subject','intensity','Timepoint'], ignore_index=True)

df_contralesional = df_contralesional.sort_values(by=['Patient', 'Intensity', 'Timepoint'], ignore_index=True)
df_contra_occ = df_contra_occ.sort_values(by=['Patient', 'Intensity', 'Timepoint'], ignore_index=True)

#rename columns for clera understanding
df_completeMEP = df_completeMEP.rename(columns={"zMEP": "zMEP_ipsi"})
df_completeMEP = df_completeMEP.rename(columns={"MEP": "MEP_ipsi"})
df_completeMEP['MEP_contra'] = df_contralesional['MEP']
df_completeMEP['zMEP_contra'] = df_contralesional['zMEP']

df_completeOcc = df_completeOcc.rename(columns={"occurrence": "occ_ipsi"})
df_completeOcc['occ_contra'] = df_contra_occ['OCC']


#%% save generated dataframes with complete information
outfile = direct + 'complete_MEP.csv'
df_completeMEP.to_csv(outfile, index=False)

outfile1 = direct + 'complete_Occ.csv'
df_completeOcc.to_csv(outfile1, index=False)