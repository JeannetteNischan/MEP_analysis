#%% Import tools and libraries
import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd


#%% predefine paths and variables
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/V2_V4/'
direct_plots = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/V2_V4/'
shift = 0.3
labels = ['pre','post']

#set colours for plotting to match previous plots
colourcode = ['red', 'blue']
sb.set_palette(colourcode)


#%% load dataframes
file_name = direct + 'pre-post.pkl'
file_name_log = direct + 'pre-post_log.pkl'
df_V2V4 = pd.read_pickle(file_name)
df_V2V4_log = pd.read_pickle(file_name_log)


#%% prepare DataFrame for special lineplots with offset
df_V2V4_lineplot = df_V2V4.copy()
df_V2V4_log_lineplot = df_V2V4_log.copy()
V2_ind = df_V2V4_lineplot.index[df_V2V4_lineplot['timepoint'] == 'pre/V2'].tolist()
V4_ind = df_V2V4_lineplot.index[df_V2V4_lineplot['timepoint'] == 'post/V4'].tolist()
V2_log_ind = df_V2V4_log_lineplot.index[df_V2V4_log_lineplot['timepoint'] == 'pre/V2'].tolist()
V4_log_ind = df_V2V4_log_lineplot.index[df_V2V4_log_lineplot['timepoint'] == 'post/V4'].tolist()
df_V2V4_lineplot.loc[V2_ind,['intensity in %RMT']] = df_V2V4_lineplot.loc[V2_ind,['intensity in %RMT']] - shift
df_V2V4_lineplot.loc[V4_ind,['intensity in %RMT']] = df_V2V4_lineplot.loc[V4_ind,['intensity in %RMT']] + shift
df_V2V4_log_lineplot.loc[V2_log_ind,['intensity in %RMT']] = df_V2V4_log_lineplot.loc[V2_log_ind,['intensity in %RMT']] - shift
df_V2V4_log_lineplot.loc[V4_log_ind,['intensity in %RMT']] = df_V2V4_log_lineplot.loc[V4_log_ind,['intensity in %RMT']] + shift

#%%Plot
#%%1. Plot lineplots of MEP size and log MEP size with different errorbars
 #1.1 MEP size in µV
plt.figure(dpi=130)
plt.title('I/O curve for ipsilesional/contralateral MEP sizes \n (with 95% confidence interval)')
ax = sb.lineplot(data=df_V2V4_lineplot, x='intensity in %RMT', y='MEP size in µV', hue='timepoint', 
            style='timepoint', markers=True, errorbar='ci', err_style='bars', err_kws={'capsize':1.8})
ax.lines[0].set_linestyle("--")
plt.legend(labels=["pre","post"])
sb.move_legend(ax, "upper left")
plt.ylim(0.5,2)
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
plt.savefig(direct_plots + 'seaborn_lineplots/IO_MEP_ci.png', format='png')
#plt.show()
plt.close()
plt.figure(dpi=130)
plt.title('I/O curve for ipsilesional/contralateral MEP sizes \n (with standard error of the mean)')
ax = sb.lineplot(data=df_V2V4_lineplot, x='intensity in %RMT', y='MEP size in µV', hue='timepoint', 
                 style='timepoint', markers=True, errorbar='se', err_style='bars', err_kws={'capsize':1.8})
ax.lines[0].set_linestyle("--")
plt.legend(labels=["pre","post"])
sb.move_legend(ax, "upper left")
plt.ylim(0.5,2)
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
plt.savefig(direct_plots + 'seaborn_lineplots/IO_MEP_sem.png', format='png')
plt.close()

 #1.2 log(MEP size) 
 # log was computed with log() function of math library and by adding a constant of 2 to every value to avoid log(0)
plt.figure(dpi=130)
plt.title('I/O curve for ipsilesional/contralateral log transformed MEP sizes \n (with 95% confidence interval)')
ax = sb.lineplot(data=df_V2V4_log_lineplot, x='intensity in %RMT', y='log transformed MEP size', hue='timepoint', 
                 style='timepoint', markers=True, errorbar='ci', err_style='bars', err_kws={'capsize':1.8})
ax.lines[0].set_linestyle("--")
plt.legend(labels=["pre","post"])
sb.move_legend(ax, "upper left")
plt.ylim(0.5,2)
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
plt.savefig(direct_plots + 'seaborn_lineplots/logIO_MEP_ci.png', format='png')
plt.close()
plt.figure(dpi=130)
plt.title('I/O curve for ipsilesional/contralateral log(MEP sizes) \n (with standard error of the mean)')
ax = sb.lineplot(data=df_V2V4_log_lineplot, x='intensity in %RMT', y='log transformed MEP size', hue='timepoint', 
                 style='timepoint', markers=True, errorbar='se', err_style='bars', err_kws={'capsize':1.8})
ax.lines[0].set_linestyle("--")
plt.legend(labels=["pre","post"])
sb.move_legend(ax, "upper left")
plt.ylim(0.5,2)
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
plt.savefig(direct_plots + 'seaborn_lineplots/logIO_MEP_sem.png', format='png')
plt.close()


#2. Plot lineplots of MEP occurrences and log MEP occurrences with different errorbars
 #2.1 MEP occurrence rates (relative MEP occurrence in all accepted trials, amount of accepted trial varies and is not known)
 # value of 1 means: in all accepted trials an MEP occurred
plt.figure(dpi=130)
plt.title('I/O of ipsilesional/contralateral relative MEP occurrence rate \n (with 95% confidence interval)')
ax = sb.lineplot(data=df_V2V4_lineplot, x='intensity in %RMT', y='occurrence', hue='timepoint', 
                 style='timepoint', markers=True, errorbar='ci', err_style='bars', err_kws={'capsize':1.8})
ax.lines[0].set_linestyle("--")
plt.legend(labels=["pre","post"])
sb.move_legend(ax, "upper left")
plt.ylim(0,0.55)
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
plt.savefig(direct_plots + 'seaborn_lineplots/occIO_MEP_ci.png', format='png')
plt.close()
plt.figure(dpi=130)
plt.title('I/O of ipsilesional/contralateral relative MEP occurrence rate \n (with standard error of the mean)')
ax = sb.lineplot(data=df_V2V4_lineplot, x='intensity in %RMT', y='occurrence', hue='timepoint', 
                 style='timepoint', markers=True, errorbar='se', err_style='bars', err_kws={'capsize':1.8})
ax.lines[0].set_linestyle("--")
plt.legend(labels=["pre","post"])
sb.move_legend(ax, "upper left")
plt.ylim(0,0.55)
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
plt.savefig(direct_plots + 'seaborn_lineplots/occIO_MEP_sem.png', format='png')
plt.close()

 #2.2 log transformed MEP occurrences
plt.figure(dpi=130)
plt.title('I/O of ipsilesional/contralateral logarithmic MEP occurrence rate \n (with 95% confidence interval)')
ax = sb.lineplot(data=df_V2V4_log_lineplot, x='intensity in %RMT', y='log transformed occurrence', hue='timepoint', 
                 style='timepoint', markers=True, errorbar='ci', err_style='bars', err_kws={'capsize':1.8})
ax.lines[0].set_linestyle("--")
plt.legend(labels=["pre","post"])
sb.move_legend(ax, "upper left")
plt.ylim(0,0.55)
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
plt.savefig(direct_plots + 'seaborn_lineplots/log-occ_IO_MEP_ci.png', format='png')
plt.close()
plt.figure(dpi=130)
plt.title('I/O of ipsilesional/contralateral logarithmic MEP occurrence rate \n (with standard error of the mean)')
ax = sb.lineplot(data=df_V2V4_log_lineplot, x='intensity in %RMT', y='log transformed occurrence', hue='timepoint', 
                 style='timepoint', markers=True, errorbar='se', err_style='bars', err_kws={'capsize':1.8})
ax.lines[0].set_linestyle("--")
plt.legend(labels=["pre","post"])
sb.move_legend(ax, "upper left")
plt.ylim(0,0.55)
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
plt.savefig(direct_plots + 'seaborn_lineplots/log-occ_IO_MEP_sem.png', format='png')
plt.close()
'''

#%%3. Boxplots for MEP size and log MEP size (with and without outliers)

 #3.1 MEP sizes in µV with outliers
plt.figure(dpi=130)
plt.title('Ipsilesional/contralateral MEP sizes \n including outlier values')
sb.boxplot(data=df_V2V4, x="intensity in %RMT", y="MEP size in µV", hue="timepoint")
plt.savefig(direct_plots + 'seaborn_boxplots/IO_MEP_outliers.png', format='png')
plt.close()

 #3.2 largest outlier values excluded
plt.figure(dpi=130)
plt.title('Ipsilesional/contralateral MEP sizes \n outlier values excluded')
sb.boxplot(data=df_V2V4, x="intensity in %RMT", y="MEP size in µV", hue="timepoint", showfliers=False)
plt.savefig(direct_plots + 'seaborn_boxplots/IO_MEP_no-outliers.png', format='png')
plt.close()

 #3.3 log(MEP size)
plt.figure(dpi=130)
plt.title('Ipsilesional/contralateral log transformed MEP sizes \n (log(MEP size + 2) constant added to avoid log(0))') 
sb.boxplot(data=df_V2V4_log, x='intensity in %RMT', y='log transformed MEP size', hue='timepoint' )
plt.savefig(direct_plots + 'seaborn_boxplots/logIO_MEP_outliers.png', format='png')
plt.close()

 #3.4 outliers excluded
plt.figure(dpi=130)
plt.title('Ipsilesional/contralateral log transformed MEP sizes \n (log(MEP size + 2) constant added to avoid log(0))') 
sb.boxplot(data=df_V2V4_log, x='intensity in %RMT', y='log transformed MEP size', hue='timepoint', showfliers=False )
plt.savefig(direct_plots + 'seaborn_boxplots/logIO_MEP_no-outliers.png', format='png')
plt.close()


#4. Boxplots for MEP occurence rates
 #4.1 relative occurrences
plt.figure(dpi=130)
plt.title('Ipsilesional/contralateral MEP occurrence rates')
sb.boxplot(data=df_V2V4, x="intensity in %RMT", y="occurrence", hue="timepoint")
plt.savefig(direct_plots + 'seaborn_boxplots/occIO_MEP_outliers.png', format='png')
plt.close()
 #4.2 log transformed MEP occurrences
plt.figure(dpi=130)
plt.title('Ipsilesional/contralateral log transformed MEP occurrence rates')
sb.boxplot(data=df_V2V4_log, x="intensity in %RMT", y="log transformed occurrence", hue="timepoint")
plt.savefig(direct_plots + 'seaborn_boxplots/log-occ_IO_MEP_outliers.png', format='png')
plt.close()

#%%5. Barplots for MEP sizes
 #5.1 MEP size in µV
plt.figure(dpi=130)
plt.title('Ipsilesional/contralateral MEP sizes in µV \n with 95% confidence interval')
ax = sb.barplot(data=df_V2V4, x='intensity in %RMT', y='MEP size in µV', hue='timepoint', 
           errorbar='ci', errwidth = 1, capsize=0.06)
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
h, l = ax.get_legend_handles_labels()
ax.legend(h, labels, title='Timepoint')
sb.move_legend(ax, "upper left")
plt.ylim(0,2)
plt.savefig(direct_plots + 'seaborn_barplots/IO_MEP_ci.png', format='png')
plt.close()
plt.figure(dpi=130)
plt.title('Ipsilesional/contralateral MEP sizes in µV \n with standard error of the mean')
ax = sb.barplot(data=df_V2V4, x='intensity in %RMT', y='MEP size in µV', hue='timepoint',
            errorbar='se', errwidth = 1, capsize=0.06)
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
h, l = ax.get_legend_handles_labels()
ax.legend(h, labels, title='Timepoint')
sb.move_legend(ax, "upper left")
plt.ylim(0,2)
plt.savefig(direct_plots + 'seaborn_barplots/IO_MEP_sem.png', format='png')
plt.close()

 #5.2 log MEP size
plt.figure(dpi=130)
plt.title('Ipsilesional/contralateral log transformed MEP sizes \n with 95% confidence interval')
ax = sb.barplot(data=df_V2V4_log, x='intensity in %RMT', y='log transformed MEP size', 
           hue='timepoint', errorbar='ci', errwidth = 1, capsize=0.06)
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
h, l = ax.get_legend_handles_labels()
ax.legend(h, labels, title='Timepoint')
sb.move_legend(ax, "upper left")
plt.ylim(0,2)
plt.savefig(direct_plots + 'seaborn_barplots/logIO_MEP_ci.png', format='png')
plt.close()
plt.figure(dpi=130)
plt.title('Ipsilesional/contralateral log transformed MEP sizes \n with standard error of the mean')
ax = sb.barplot(data=df_V2V4_log, x='intensity in %RMT', y='log transformed MEP size',
            hue='timepoint', errorbar='se', errwidth = 1, capsize=0.05)
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
h, l = ax.get_legend_handles_labels()
ax.legend(h, labels, title='Timepoint')
plt.ylim(0,2)
plt.savefig(direct_plots + 'seaborn_barplots/logIO_MEP_sem.png', format='png')
plt.close()

#6. Barplots for MEP occurrences
 #6.1 realtive MEP occurrences
plt.figure(dpi=130)
plt.title('Ipsilesional/contralateral MEP occurrences \n with 95% confidence interval')
ax = sb.barplot(data=df_V2V4, x='intensity in %RMT', y='occurrence',
            hue='timepoint', errorbar='ci', errwidth = 1, capsize=0.05)
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
h, l = ax.get_legend_handles_labels()
ax.legend(h, labels, title='Timepoint')
sb.move_legend(ax, "upper left")
plt.ylim(0,0.6)
plt.savefig(direct_plots + 'seaborn_barplots/occIO_MEP_ci.png', format='png')
plt.close()
plt.figure(dpi=130)
plt.title('Ipsilesional/contralateral MEP occurrences \n with standard error of the mean')
ax = sb.barplot(data=df_V2V4, x='intensity in %RMT', y='occurrence', hue='timepoint', 
           errorbar='se', errwidth = 1, capsize=0.05)
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
h, l = ax.get_legend_handles_labels()
ax.legend(h, labels, title='Timepoint')
sb.move_legend(ax, "upper left")
plt.ylim(0,0.6)
plt.savefig(direct_plots + 'seaborn_barplots/occIO_MEP_sem.png', format='png')
plt.close()

 #6.2 log transformed occurrences
plt.figure(dpi=130)
plt.title('Ipsilesional/contralateral log transformed MEP occurrence rates \n with 95% confidence interval')
ax = sb.barplot(data=df_V2V4_log, x='intensity in %RMT', y='log transformed occurrence', 
           hue='timepoint', errorbar='ci', errwidth = 1, capsize=0.05)
plt.savefig(direct_plots + 'seaborn_barplots/log-occIO_MEP_ci.png', format='png')
plt.close()
plt.figure(dpi=130)
plt.title('Ipsilesional/contralateral log transformed MEP occurrence rates \n with standard error of the mean')
ax = sb.barplot(data=df_V2V4_log, x='intensity in %RMT', y='log transformed occurrence',
            hue='timepoint', errorbar='se', errwidth = 1, capsize=0.05)
plt.savefig(direct_plots + 'seaborn_barplots/log-occIO_MEP_sem.png', format='png')
plt.close()'''