#%%import tools and libraries
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt


#%% define paths and fixed variables if needed
direct = '/home/jeanettenischan/Desktop/'

file_name = direct + 'LMM_Estimates_longFormat.csv'  #'LMM_Estimates_for_plot.csv'
df_estimates = pd.read_csv(file_name)
labels = ['zMEP','Occ']
shift = [-0.4, -0.2, 0.2]

#prepare Intensity values with shift for netter visualisation of error bars
#get different indices for timepoints
indV3 = df_estimates.index[df_estimates['Timepoint'] == 'V3'].to_list()
indV4 = df_estimates.index[df_estimates['Timepoint'] == 'V4'].to_list()
indV6 = df_estimates.index[df_estimates['Timepoint'] == 'V6'].to_list()
#replace intensity values by adding/substracing shift
df_estimates.loc[indV3,['Intensity']] = df_estimates.loc[indV3,['Intensity']] + shift[0]
df_estimates.loc[indV4,['Intensity']] = df_estimates.loc[indV4,['Intensity']] + shift[1]
df_estimates.loc[indV6,['Intensity']] = df_estimates.loc[indV6,['Intensity']] + shift[2]

plt.figure(dpi=130)
lp = sb.lineplot(data= df_estimates, x='Intensity', y = 'zMEP', hue='Timepoint', 
            style='Timepoint', markers=True)
# n_intens = 8
# for n_times in range(4):
#     plt.errorbar(list(df_estimates['Intensity'])[n_times * n_intens:(n_times + 1) * n_intens - 1], 
#                  list(df_estimates['zMEP'])[n_times * n_intens:(n_times + 1) * n_intens - 1], 
#                  yerr=list(df_estimates['SEM'])[n_times * n_intens:(n_times + 1) * n_intens - 1], 
#                  fmt='none')

plt.show()

plt.figure(dpi=130)
plt.title('Fixed effect estimates with standard error \n of MEP data (z-transformed) and occurrences')
ax = sb.barplot(data=df_estimates, x='Intensity', y='log transformed MEP size', 
           hue='Type', errorbar='se', errwidth = 1, capsize=0.06)
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
h, l = ax.get_legend_handles_labels()
ax.legend(h, labels, title='Timepoint')
sb.move_legend(ax, "upper left")
plt.ylim(0,2)