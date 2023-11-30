#%% Import tools and libraries
import pandas as pd
import pingouin as pg
from scipy import stats


#%% predefine paths and variables
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/V2_V4/'

#%% load dataframes
file_name = direct + 'pre-post.pkl'
file_name_log = direct + 'pre-post_log.pkl'
df_V2V4 = pd.read_pickle(file_name)
df_V2V4_log = pd.read_pickle(file_name_log)


#%%Statistical analysis
#%%Test for data distribution
#stats.kstest()
#%%1.pairwise tests
 #1a.1 exactly like Karolina, first fo MEP size:
'''MEPTests_lK = pg.pairwise_tests(data=df_V2V4, 
                                    dv='MEP size in µV', 
                                    within=['intensity in %RMT','timepoint'], 
                                    subject='subject', 
                                    parametric=True, 
                                    padjust='fdr_bh', 
                                    alternative='greater',
                                    effsize='cohen')
pg.print_table(MEPTests_lK, floatfmt='.3f')

 #1a.2 for log MEP size
logMEPTests_lK = pg.pairwise_tests(data=df_V2V4_log, 
                                    dv='log transformed MEP size', 
                                    within=['intensity in %RMT','timepoint'], 
                                    subject='subject', 
                                    parametric=True, 
                                    padjust='fdr_bh', 
                                    alternative='greater',
                                    effsize='cohen')
pg.print_table(logMEPTests_lK, floatfmt='.3f')

 #1a.3 for MEP occurrence rates
occTests_lK = pg.pairwise_tests(data=df_V2V4, 
                                    dv='occurrence', 
                                    within=['intensity in %RMT','timepoint'], 
                                    subject='subject', 
                                    parametric=True, 
                                    padjust='fdr_bh', 
                                    alternative='greater',
                                    effsize='cohen')
pg.print_table(occTests_lK, floatfmt='.3f')

#1b. Paired tests with individual parameters:
 #1b.1 MEP size
pairTests = pg.pairwise_tests(data=df_V2V4, 
                                    dv='MEP size in µV', 
                                    within=['intensity in %RMT','timepoint'], 
                                    subject='subject', 
                                    alpha= 0.05, 
                                    alternative='greater',
                                    padjust = 'bonf', 
                                    effsize = 'cohen')
pg.print_table(pairTests, floatfmt='.3f')


#%%T-Tests in loop
 # for MEP size
for intens in range (80,160,10):
    df_intens = df_V2V4[df_V2V4['intensity in %RMT'] == intens]
    df_V2 = df_intens[df_intens['timepoint'] == 'pre/V2']
    df_V4 = df_intens[df_intens['timepoint'] == 'post/V4']
    Ttest = pg.ttest(df_V2['MEP size in µV'],df_V4['MEP size in µV'], 
                                        paired = True, 
                                        alternative='greater',
                                        confidence = 0.95)
    pg.print_table(Ttest, floatfmt='.3f')

 #for log MEP 
for intens in range (80,160,10):
    df_intens = df_V2V4_log[df_V2V4_log['intensity in %RMT'] == intens]
    df_V2 = df_intens[df_intens['timepoint'] == 'pre/V2']
    df_V4 = df_intens[df_intens['timepoint'] == 'post/V4']
    logT = pg.ttest(df_V2['log transformed MEP size'],df_V4['log transformed MEP size'], 
                                        paired = True, 
                                        alternative='greater',
                                        confidence = 0.95)
    pg.print_table(logT, floatfmt='.3f')

 # for occurrence
for intens in range (80,160,10):
    df_intens = df_V2V4[df_V2V4['intensity in %RMT'] == intens]
    df_V2 = df_intens[df_intens['timepoint'] == 'pre/V2']
    df_V4 = df_intens[df_intens['timepoint'] == 'post/V4']
    occ_T = pg.ttest(df_V2['occurrence'],df_V4['occurrence'], 
                                        paired = True, 
                                        alternative='greater',
                                        confidence = 0.95)
    pg.print_table(occ_T, floatfmt='.3f')
'''    
#%% rmANOVA 
rm_anova = pg.rm_anova(data=df_V2V4_log, dv='log transformed MEP size', within=['intensity in %RMT','timepoint'],
                       subject='subject', correction='auto', detailed=True, effsize='n2') 
  
pg.print_table(rm_anova, floatfmt='.3f')

rm_anova_occ = pg.rm_anova(data=df_V2V4_log, dv='log transformed occurrence', within=['intensity in %RMT','timepoint'],
                       subject='subject', correction='auto', detailed=True, effsize='n2') 
  
pg.print_table(rm_anova_occ, floatfmt='.3f')


anova = pg.rm_anova(data=df_V2V4_log, dv='log transformed MEP size', within=['intensity in %RMT','timepoint'],
                       subject='subject', correction='auto', detailed=True, effsize='n2') 
  
pg.print_table(anova, floatfmt='.3f')


anova_occ = pg.rm_anova(data=df_V2V4_log, dv='log transformed occurrence', within=['intensity in %RMT','timepoint'],
                       subject='subject', correction='auto', detailed=True, effsize='n2') 
  
pg.print_table(anova_occ, floatfmt='.3f')