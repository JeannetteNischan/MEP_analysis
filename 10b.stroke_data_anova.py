#%%import tools and libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pingouin as pg
from math import log
import pickle

#%%define paths and variables
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/phase_compare/'


#%% load dataframes
file_name = direct + 'allTimes.pkl'
file_name_log = direct + 'allTimes_log.pkl'
df_phase_allTime = pd.read_pickle(file_name)
df_phase_allTime_log = pd.read_pickle(file_name_log)

#%% statistical analysis
# https://pingouin-stats.org/build/html/generated/pingouin.anova.html
anova = pg.anova(data=df_phase_allTime, dv='MEP size in µV', between=['phase', 'intensity'], detailed=True)
pg.print_table(anova, floatfmt='.3f')
print(anova)

anova_log = pg.anova(data=df_phase_allTime_log, dv='MEP size in µV', between=['phase', 'intensity'], detailed=True)
pg.print_table(anova_log, floatfmt='.3f')
print(anova_log)

posthoc = pg.pairwise_tests(data=df_phase_allTime, dv='MEP size in µV', between=['phase', 'intensity'], parametric=True, padjust='fdr_bh', effsize='hedges')
# Pretty printing of posthoc table
print(posthoc)
pg.print_table(posthoc, floatfmt='.3f')

