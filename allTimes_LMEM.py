#%%import tools and libraries
import pandas as pd
#from pymer4.utils import get_resource_path
#from pymer4.models import Lmer


#%% define paths and fixed variables if needed
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/allTimes/'

#%% load dataframes
file_name = direct + 'allTimes_MEP.pkl'
file_name_occ = direct + 'allTimes_Occ.pkl'
df_allTimes_MEP = pd.read_pickle(file_name)
df_allTimes_Occ = pd.read_pickle(file_name_occ)


#%% divide by intervention (condition)
ipsi_first_MEP = df_allTimes_MEP.loc[df_allTimes_MEP['condition'] == 1]
contra_first_MEP = df_allTimes_MEP.loc[df_allTimes_MEP['condition'] == 2]
ipsi_first_Occ = df_allTimes_Occ.loc[df_allTimes_Occ['condition'] == 1]
contra_first_Occ = df_allTimes_Occ.loc[df_allTimes_Occ['condition'] == 2]

'''
ipsi_first_MEP = ipsi_first_MEP.drop(columns=['condition'])
contra_first_MEP = contra_first_MEP.drop(columns=['condition'])
ipsi_first_Occ = ipsi_first_Occ.drop(columns=['condition'])
contra_first_Occ = contra_first_Occ.drop(columns=['condition'])
'''

#%% rearrange dataframe
df_MEP_melt_ipsi = pd.melt(ipsi_first_MEP, id_vars=['subject', 'intensity'], 
                    value_vars=['V2','V3', 'V4','V5','V6'],
                    var_name='Timepoint', value_name='MEP')

df_MEP_melt_contra = pd.melt(contra_first_MEP, id_vars=['subject', 'intensity'], 
                    value_vars=['V2','V3', 'V4','V5','V6'],
                    var_name='Timepoint', value_name='MEP')

df_MEP_melt_all = pd.melt(df_allTimes_MEP, id_vars=['subject', 'intensity'], 
                    value_vars=['V2','V3', 'V4','V5','V6'],
                    var_name='Timepoint', value_name='MEP')


df_Occ_melt_ipsi = pd.melt(ipsi_first_Occ, id_vars=['subject', 'intensity'], 
                    value_vars=['V2','V3', 'V4','V5','V6'],
                    var_name='Timepoint', value_name='occurrence')

df_Occ_melt_contra = pd.melt(contra_first_Occ, id_vars=['subject', 'intensity'], 
                    value_vars=['V2','V3', 'V4','V5','V6'],
                    var_name='Timepoint', value_name='occurrence')

df_Occ_melt_all = pd.melt(df_allTimes_Occ, id_vars=['subject', 'intensity'], 
                    value_vars=['V2','V3', 'V4','V5','V6'],
                    var_name='Timepoint', value_name='occurrence')

#%%linear mixed model
""" model_all = Lmer("intensity ~ Timepoint ", data=df_MEP_melt_all)
print(model_all.anova())

model_ipsi = Lmer("intensity ~ Timepoint ", data=df_MEP_melt_ipsi)
print(model_ipsi.anova())

model_contra = Lmer("intensity ~ Timepoint ", data=df_MEP_melt_contra)
print(model_contra.anova())

model_Occ = Lmer("intensity ~ Timepoint ", data=df_Occ_melt_all)
print(model_Occ.anova())

model_iOcc = Lmer("intensity ~ Timepoint ", data=df_Occ_melt_ipsi)
print(model_iOcc.anova())

model_cOcc = Lmer("intensity ~ Timepoint ", data=df_Occ_melt_contra)
print(model_cOcc.anova()) """


#%% Save data frame
outfile = direct + 'ipsi_first_MEP.csv'
df_MEP_melt_ipsi.to_csv(outfile, index=False)

outfile = direct + 'contra_first_MEP.csv'
df_MEP_melt_contra.to_csv(outfile, index=False)

outfile = direct + 'allTimes_longF_MEP.csv'
df_MEP_melt_all.to_csv(outfile, index=False)


outfile = direct + 'ipsi_first_Occ.csv'
df_Occ_melt_ipsi.to_csv(outfile, index=False)

outfile = direct + 'contra_first_Occ.csv'
df_Occ_melt_contra.to_csv(outfile, index=False)

outfile = direct + 'allTimes_longF_Occ.csv'
df_Occ_melt_all.to_csv(outfile, index=False)


