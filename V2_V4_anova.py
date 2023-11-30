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

#%% statistical analysis
#Anova for MEP sizes 
anova = pg.anova(data=df_V2V4, dv='MEP size in µV', between=['timepoint', 'intensity in %RMT'], detailed=True)
pg.print_table(anova, floatfmt='.3f')
print(anova)

anova_log = pg.anova(data=df_V2V4_log, dv='log transformed MEP size', between=['timepoint', 'intensity in %RMT'], detailed=True)
pg.print_table(anova_log, floatfmt='.3f')
print(anova_log)


#for MEP occurrence rates
anova_occ = pg.anova(data=df_V2V4, dv='occurrence', between=['timepoint', 'intensity in %RMT'], detailed=True)
pg.print_table(anova_occ, floatfmt='.3f')
print(anova_occ)

anova_occ_log = pg.anova(data=df_V2V4_log, dv='log transformed occurrence', between=['timepoint', 'intensity in %RMT'], detailed=True)
pg.print_table(anova_occ_log, floatfmt='.3f')
print(anova_occ_log)
