#%%import tools and libraries
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt


#%% define paths and fixed variables if needed
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/allTimes/'
direct_plots = '/home/jeanettenischan/Desktop/MEP_Occ_plots/'

#%% load dataframes with MEP and occurrence info
filename = direct + 'complete_MEP.csv'
df_MEP = pd.read_csv(filename)

filename1 = direct + 'complete_Occ.csv'
df_Occ = pd.read_csv(filename1)

#%% introduce shift into data for better visibility of error bars
shift = [-0.6, -0.3, 0.3, 0.6]
#get different indices for timepoints
indV2 = df_MEP.index[df_MEP['Timepoint'] == 'V2'].to_list()
indV3 = df_MEP.index[df_MEP['Timepoint'] == 'V3'].to_list()
indV5 = df_MEP.index[df_MEP['Timepoint'] == 'V5'].to_list()
indV6 = df_MEP.index[df_MEP['Timepoint'] == 'V6'].to_list()

indV2 = df_Occ.index[df_Occ['Timepoint'] == 'V2'].to_list()
indV3 = df_Occ.index[df_Occ['Timepoint'] == 'V3'].to_list()
indV5 = df_Occ.index[df_Occ['Timepoint'] == 'V5'].to_list()
indV6 = df_Occ.index[df_Occ['Timepoint'] == 'V6'].to_list()

#replace intensity values by adding/substracing shift
df_MEP.loc[indV2,['intensity']] = df_MEP.loc[indV2,['intensity']] + shift[0]
df_MEP.loc[indV3,['intensity']] = df_MEP.loc[indV3,['intensity']] + shift[1]
df_MEP.loc[indV5,['intensity']] = df_MEP.loc[indV5,['intensity']] + shift[2]
df_MEP.loc[indV6,['intensity']] = df_MEP.loc[indV6,['intensity']] + shift[3]

#replace intensity values by adding/substracing shift
df_Occ.loc[indV2,['intensity']] = df_Occ.loc[indV2,['intensity']] + shift[0]
df_Occ.loc[indV3,['intensity']] = df_Occ.loc[indV3,['intensity']] + shift[1]
df_Occ.loc[indV5,['intensity']] = df_Occ.loc[indV5,['intensity']] + shift[2]
df_Occ.loc[indV6,['intensity']] = df_Occ.loc[indV6,['intensity']] + shift[3]

#%%plot
#1.1 MEP size in µV
plt.figure(dpi=130)
plt.title('I/O curve for ipsilesional/contralateral MEP sizes \n (with 95% confidence interval)')
sb.lineplot(data=df_MEP, x='intensity', y='MEP_ipsi', hue='Timepoint', 
            style='Timepoint', markers=True, errorbar='ci', err_style='bars', err_kws={'capsize':1.8})
plt.xlabel('Intensity in %RMT')
plt.ylabel('average MEP size in µV')
plt.legend(loc='upper left')
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
#plt.savefig(direct_plots + 'IO_MEP_ipsi.png', format='png')
plt.show()
#plt.close()

plt.figure(dpi=130)
plt.title('I/O curve for contralesional/ipsilateral MEP sizes \n (with 95% confidence interval)')
sb.lineplot(data=df_MEP, x='intensity', y='MEP_contra', hue='Timepoint', 
            style='Timepoint', markers=True, errorbar='ci', err_style='bars', err_kws={'capsize':1.8})
plt.xlabel('Intensity in %RMT')
plt.ylabel('average MEP size in µV')
plt.legend(loc='upper left')
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
#plt.savefig(direct_plots + 'IO_MEP_contra.png', format='png')
plt.show()
#plt.close()

#1.2 z-transformed MEP data
plt.figure(dpi=130)
plt.title('I/O curve for ipsilesional/contralateral z-transformed MEP sizes \n (with 95% confidence interval)')
sb.lineplot(data=df_MEP, x='intensity', y='zMEP_ipsi', hue='Timepoint', 
            style='Timepoint', markers=True, errorbar='ci', err_style='bars', err_kws={'capsize':1.8})
plt.xlabel('Intensity in %RMT')
plt.ylabel('z-transformed MEP size')
plt.legend(loc='upper left')
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
#plt.savefig(direct_plots + 'IO_zMEP_ipsi.png', format='png')
plt.show()
#plt.close()

plt.figure(dpi=130)
plt.title('I/O curve for contralesional/ipsilateral z-transformed MEP sizes \n (with 95% confidence interval)')
sb.lineplot(data=df_MEP, x='intensity', y='zMEP_contra', hue='Timepoint', 
            style='Timepoint', markers=True, errorbar='ci', err_style='bars', err_kws={'capsize':1.8})
plt.xlabel('Intensity in %RMT')
plt.ylabel('z-transformed MEP size')
plt.legend(loc='upper left')
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
#plt.savefig(direct_plots + 'IO_zMEP_contra.png', format='png')
plt.show()
#plt.close()

#2.1 Occurrence rates
plt.figure(dpi=130)
plt.title('I/O curve for ipsilesional/contralateral MEP sizes \n (with 95% confidence interval)')
sb.lineplot(data=df_Occ, x='intensity', y='occ_ipsi', hue='Timepoint', 
            style='Timepoint', markers=True, errorbar='ci', err_style='bars', err_kws={'capsize':1.8})
plt.xlabel('Intensity in %RMT')
plt.ylabel('average occurrence rate')
plt.legend(loc='upper left')
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
#plt.savefig(direct_plots + 'IO_Occ_ipsi.png', format='png')
plt.show()
#plt.close()

plt.figure(dpi=130)
plt.title('I/O curve for contralesional/ipsilateral MEP sizes \n (with 95% confidence interval)')
sb.lineplot(data=df_Occ, x='intensity', y='occ_contra', hue='Timepoint', 
            style='Timepoint', markers=True, errorbar='ci', err_style='bars', err_kws={'capsize':1.8})
plt.xlabel('Intensity in %RMT')
plt.ylabel('average occurrence rate')
plt.legend(loc='upper left')
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
#plt.savefig(direct_plots + 'IO_Occ_contra.png', format='png')
plt.show()
#plt.close()