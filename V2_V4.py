#%%import tools and libraries
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import pingouin as pg
import json
from math import log
import os




#%% define paths and fixed variables if needed
#time = 'V3' 
timepoints = ['V2','V4'] # 1 und 3 bzw in python 0 und 2 
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/sorted/accepted/'
target_direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/V2_V4/'
direct_plots = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/V2_V4/'
subjects = [name for name in os.listdir(direct) if name.endswith('time.json')]
acceptedSubjects = []

#set colours for plotting to match previous plots
colourcode = ['red', 'skyblue']
sb.set_palette(colourcode)

#%% load data and create dataframe
df_V2V4 = {'subject' : [], 'timepoint' : [], 'intensity in %RMT':[], 'MEP size in µV' : [], 'occurrence':[]}
df_V2V4_log = {'subject' : [], 'timepoint' : [], 'intensity in %RMT':[], 'log transformed MEP size' : [], 'log transformed occurrence':[]}

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
            log_occ = log(occ +2)

            if data[intensity][0] == 0.0:
                MEP = 0
            else: 
                    MEP = data[intensity][0]
            log_data = log(MEP +2)

            df_V2V4['subject'].append(ID) 
            df_V2V4['timepoint'].append(timepoint)
            df_V2V4['intensity in %RMT'].append(int(intensity))
            df_V2V4['MEP size in µV'].append(MEP)
            df_V2V4['occurrence'].append(occ)

            df_V2V4_log['subject'].append(ID)
            df_V2V4_log['timepoint'].append(timepoint)
            df_V2V4_log['intensity in %RMT'].append(int(intensity))
            df_V2V4_log['log transformed MEP size'].append(log_data)
            df_V2V4_log['log transformed occurrence'].append(log_occ)

            acceptedSubjects.append(ID)

            if data[intensity][2] != -1:
                ID = subject[0:3]
                timepoint = 'post/V4' 

                occ = occData[intensity][2]     
                log_occ = log(occ +2)

                if data[intensity][2] == 0.0:
                    MEP = 0
                else: 
                    MEP = data[intensity][2]
                log_data = log(MEP +2)

                df_V2V4['subject'].append(ID) 
                df_V2V4['timepoint'].append(timepoint)
                df_V2V4['intensity in %RMT'].append(int(intensity))
                df_V2V4['MEP size in µV'].append(MEP)
                df_V2V4['occurrence'].append(occ)

                df_V2V4_log['subject'].append(ID)
                df_V2V4_log['timepoint'].append(timepoint)
                df_V2V4_log['intensity in %RMT'].append(int(intensity))
                df_V2V4_log['log transformed MEP size'].append(log_data)
                df_V2V4_log['log transformed occurrence'].append(log_occ) 
           
# transform dict to dataframe
df_V2V4 = pd.DataFrame.from_dict(df_V2V4)
df_V2V4_log = pd.DataFrame.from_dict(df_V2V4_log)

#check subject column for completeness of data (at least 16 repetitions of subject ID in total)
count = df_V2V4['subject'].value_counts()
count_log = df_V2V4_log['subject'].value_counts()

acceptedSubjects = set(acceptedSubjects)
for subj in acceptedSubjects:
    if count[subj] < 16:
        indices = df_V2V4.index[df_V2V4['subject'] == subj].tolist()
        df_V2V4 = df_V2V4.drop(indices)
    elif count_log[subj] < 16:
        indices = df_V2V4_log.index[df_V2V4_log['subject'] == subj].tolist()
        df_V2V4_log = df_V2V4_log.drop(indices)  


#%% Save data frame
outfile = target_direct + 'pre-post.pkl'
df_V2V4.to_pickle(outfile)
outfile = target_direct + 'pre-post_log.pkl'
df_V2V4_log.to_pickle(outfile)

'''
#%%Plot
#1. Plot lineplots of MEP size and log MEP size with different errorbars
 #1.1 MEP size in µV
plt.figure()
plt.title('I/O curve for ipsilesional/contralateral MEP sizes \n (with 95% confidence interval)')
sb.lineplot(data=df_V2V4, x='intensity in %RMT', y='MEP size in µV', hue='timepoint', style='timepoint', markers=True, errorbar='ci')
plt.savefig(direct_plots + 'seaborn_lineplots/IO_MEP_ci.png', format='png')
plt.figure()
plt.title('I/O curve for ipsilesional/contralateral MEP sizes \n (with standard error of the mean)')
sb.lineplot(data=df_V2V4, x='intensity in %RMT', y='MEP size in µV', hue='timepoint', style='timepoint', markers=True, errorbar='se')
plt.savefig(direct_plots + 'seaborn_lineplots/IO_MEP_sem.png', format='png')

 #1.2 log(MEP size) 
 # log was computed with log() function of math library and by adding a constant of 2 to every value to avoid log(0)
plt.figure()
plt.title('I/O curve for ipsilesional/contralateral log transformed MEP sizes \n (with 95% confidence interval)')
sb.lineplot(data=df_V2V4_log, x='intensity in %RMT', y='log transformed MEP size', hue='timepoint', style='timepoint', markers=True, errorbar='ci')
plt.savefig(direct_plots + 'seaborn_lineplots/logIO_MEP_ci.png', format='png')
plt.figure()
plt.title('I/O curve for ipsilesional/contralateral log(MEP sizes) \n (with standard error of the mean)')
sb.lineplot(data=df_V2V4_log, x='intensity in %RMT', y='log transformed MEP size', hue='timepoint', style='timepoint', markers=True, errorbar='se')
plt.savefig(direct_plots + 'seaborn_lineplots/logIO_MEP_sem.png', format='png')


#2. Plot lineplots of MEP occurrences and log MEP occurrences with different errorbars
 #2.1 MEP occurrence rates (relative MEP occurrence in all accepted trials, amount of accepted trial varies and is not known)
 # value of 1 means: in all accepted trials an MEP occurred
plt.figure()
plt.title('I/O of ipsilesional/contralateral relative MEP occurrence rate \n (with 95% confidence interval)')
sb.lineplot(data=df_V2V4, x='intensity in %RMT', y='occurrence', hue='timepoint', style='timepoint', markers=True, errorbar='ci')
plt.savefig(direct_plots + 'seaborn_lineplots/occIO_MEP_ci.png', format='png')
plt.figure()
plt.title('I/O of ipsilesional/contralateral relative MEP occurrence rate \n (with standard error of the mean)')
sb.lineplot(data=df_V2V4, x='intensity in %RMT', y='occurrence', hue='timepoint', style='timepoint', markers=True, errorbar='se')
plt.savefig(direct_plots + 'seaborn_lineplots/occIO_MEP_sem.png', format='png')

 #2.2 log transformed MEP occurrences
plt.figure()
plt.title('I/O of ipsilesional/contralateral logarithmic MEP occurrence rate \n (with 95% confidence interval)')
sb.lineplot(data=df_V2V4_log, x='intensity in %RMT', y='log transformed occurrence', hue='timepoint', style='timepoint', markers=True, errorbar='ci')
plt.savefig(direct_plots + 'seaborn_lineplots/log-occ_IO_MEP_ci.png', format='png')
plt.figure()
plt.title('I/O of ipsilesional/contralateral logarithmic MEP occurrence rate \n (with standard error of the mean)')
sb.lineplot(data=df_V2V4_log, x='intensity in %RMT', y='log transformed occurrence', hue='timepoint', style='timepoint', markers=True, errorbar='se')
plt.savefig(direct_plots + 'seaborn_lineplots/log-occ_IO_MEP_sem.png', format='png')


#3. Boxplots for MEP size and log MEP size (with and without outliers)
 #3.1 MEP sizes in µV with outliers
plt.figure()
plt.title('Ipsilesional/contralateral MEP sizes \n including outlier values')
sb.boxplot(data=df_V2V4, x="intensity in %RMT", y="MEP size in µV", hue="timepoint")
plt.savefig(direct_plots + 'seaborn_boxplots/IO_MEP_outliers.png', format='png')

 #3.2 largest outlier values excluded
plt.figure()
plt.title('Ipsilesional/contralateral MEP sizes \n outlier values excluded')
sb.boxplot(data=df_V2V4, x="intensity in %RMT", y="MEP size in µV", hue="timepoint", showfliers=False)
plt.savefig(direct_plots + 'seaborn_boxplots/IO_MEP_no-outliers.png', format='png')

 #3.3 log(MEP size)
plt.figure()
plt.title('Ipsilesional/contralateral log transformed MEP sizes \n (log(MEP size + 2) constant added to avoid log(0))') 
sb.boxplot(data=df_V2V4_log, x='intensity in %RMT', y='log transformed MEP size', hue='timepoint' )
plt.savefig(direct_plots + 'seaborn_boxplots/logIO_MEP_outliers.png', format='png')

 #3.4 outliers excluded
plt.figure()
plt.title('Ipsilesional/contralateral log transformed MEP sizes \n (log(MEP size + 2) constant added to avoid log(0))') 
sb.boxplot(data=df_V2V4_log, x='intensity in %RMT', y='log transformed MEP size', hue='timepoint', showfliers=False )
plt.savefig(direct_plots + 'seaborn_boxplots/logIO_MEP_no-outliers.png', format='png')


#4. Boxplots for MEP occurence rates
 #4.1 relative occurrences
plt.figure()
plt.title('Ipsilesional/contralateral MEP occurrence rates')
sb.boxplot(data=df_V2V4, x="intensity in %RMT", y="occurrence", hue="timepoint")
plt.savefig(direct_plots + 'seaborn_boxplots/occIO_MEP_outliers.png', format='png')
 #4.2 log transformed MEP occurrences
plt.figure()
plt.title('Ipsilesional/contralateral log transformed MEP occurrence rates')
sb.boxplot(data=df_V2V4_log, x="intensity in %RMT", y="log transformed occurrence", hue="timepoint")
plt.savefig(direct_plots + 'seaborn_boxplots/log-occ_IO_MEP_outliers.png', format='png')

#5. Barplots for MEP sizes
 #5.1 MEP size in µV
plt.figure()
plt.title('Ipsilesional/contralateral MEP sizes in µV \n with 95% confidence interval')
sb.barplot(data=df_V2V4, x='intensity in %RMT', y='MEP size in µV', hue='timepoint', errorbar='ci', errwidth = 1, capsize=0.07)
plt.savefig(direct_plots + 'seaborn_barplots/IO_MEP_outliers.png', format='png')
plt.figure()
plt.title('Ipsilesional/contralateral MEP sizes in µV \n with standard error of the mean')
sb.barplot(data=df_V2V4, x='intensity in %RMT', y='MEP size in µV', hue='timepoint', errorbar='se', errwidth = 1, capsize=0.05)
plt.show()

 #5.2 log MEP size
plt.figure()
plt.title('Ipsilesional/contralateral log transformed MEP sizes \n with 95% confidence interval')
sb.barplot(data=df_V2V4_log, x='intensity in %RMT', y='log transformed MEP size', hue='timepoint', errorbar='ci', errwidth = 1, capsize=0.06)
plt.show()
plt.figure()
plt.title('Ipsilesional/contralateral log transformed MEP sizes \n with standard error of the mean')
sb.barplot(data=df_V2V4_log, x='intensity in %RMT', y='log transformed MEP size', hue='timepoint', errorbar='se', errwidth = 1, capsize=0.05)
plt.show()

#6. Barplots for MEP occurrences
 #6.1 realtive MEP occurrences
plt.figure()
plt.title('Ipsilesional/contralateral MEP occurrences \n with 95% confidence interval')
sb.barplot(data=df_V2V4, x='intensity in %RMT', y='occurrence', hue='timepoint', errorbar='ci', errwidth = 1, capsize=0.05)
plt.show()
plt.figure()
plt.title('Ipsilesional/contralateral MEP occurrences \n with standard error of the mean')
sb.barplot(data=df_V2V4, x='intensity in %RMT', y='occurrence', hue='timepoint', errorbar='se', errwidth = 1, capsize=0.05)
plt.show()
 #6.2 log transformed occurrences
plt.figure()
plt.title('Ipsilesional/contralateral log transformed MEP occurrence rates \n with 95% confidence interval')
sb.barplot(data=df_V2V4_log, x='intensity in %RMT', y='log transformed occurrence', hue='timepoint', errorbar='ci', errwidth = 1, capsize=0.05)
plt.show()
plt.figure()
plt.title('Ipsilesional/contralateral log transformed MEP occurrence rates \n with standard error of the mean')
sb.barplot(data=df_V2V4_log, x='intensity in %RMT', y='log transformed occurrence', hue='timepoint', errorbar='se', errwidth = 1, capsize=0.05)
plt.show()


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
print(anova_occ_log)'''


