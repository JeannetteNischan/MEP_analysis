#%% Import tools and libraries
import pandas as pd
import pingouin as pg

#%% predefine paths and variables
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/V2_V4/'

#%% load dataframes
file_name = direct + 'pre-post.pkl'
file_name_log = direct + 'pre-post_log.pkl'
df_V2V4 = pd.read_pickle(file_name)
df_V2V4_log = pd.read_pickle(file_name_log)

#%%create new group averages
for intens in range(80,160,10):
    df_intens = df_intens = df_V2V4[df_V2V4['intensity in %RMT'] == intens]
    df_V2 = df_intens[df_intens['timepoint'] == 'pre/V2']
    df_V4 = df_intens[df_intens['timepoint'] == 'post/V4']