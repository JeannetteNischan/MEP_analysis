#%%import tools and libraries
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
from math import log
import pickle






#%% define paths and fixed variables if needed
phases = ['0','180']
#time = 'V3' 
timepoints = ['V2','V3','V4','V5','V6']
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/'
direct_plots = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/phase_compare/'
outpath = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/phase_compare/'

#data0   = pd.read_json(direct + 'phase0_group_avgs.json').to_dict()
#data180 = pd.read_json(direct + 'phase180_group_avgs.json').to_dict()

df_phase_alltime = {'timepoint' : [], 'intensity':[], 'phase':[] , 'MEP size in µV' : []}
df_phase_alltime_log = {'timepoint' : [], 'intensity':[], 'phase':[] , 'MEP size in µV' : []}
for time in timepoints:
    df_phase = {'intensity':[], 'phase':[] , 'MEP size in µV' : []}
    df_phase_log = {'intensity':[], 'phase':[] , 'MEP size in µV' : []}
    for phase in phases:
        data = pd.read_json(direct + 'phase' + phase + '_group_avgs.json').to_dict()
        for intensity in data.keys():
            intens = [intensity] * len(data[intensity][time])
            phase_info = [phase] * len(data[intensity][time])
            times = [time] * len(data[intensity][time])
            log_data = [log(val+2) for val in data[intensity][time]]

            df_phase['intensity'].extend(intens)
            df_phase['phase'].extend(phase_info)
            df_phase['MEP size in µV'].extend(data[intensity][time])

            df_phase_log['intensity'].extend(intens)
            df_phase_log['phase'].extend(phase_info)
            df_phase_log['MEP size in µV'].extend(log_data)
            
            df_phase_alltime['timepoint'].extend(times)
            df_phase_alltime['intensity'].extend(intens)
            df_phase_alltime['phase'].extend(phase_info)
            df_phase_alltime['MEP size in µV'].extend(data[intensity][time])

            df_phase_alltime_log['timepoint'].extend(times)
            df_phase_alltime_log['intensity'].extend(intens)
            df_phase_alltime_log['phase'].extend(phase_info)
            df_phase_alltime_log['MEP size in µV'].extend(log_data)

            print('{} subjects at {} for {} %RMT'.format(len(intens), time, intensity))


    df_phase = pd.DataFrame.from_dict(df_phase)
    df_phase_log = pd.DataFrame.from_dict(df_phase_log)
    plt.figure()    
    sb.boxplot(data = df_phase, x = 'intensity', y = 'MEP size in µV', hue= 'phase')
    plt.title('Phase comparison for all intensities at ' + time)
    plt.ylabel('average MEP (peak to peak amplitude) in µV')
    plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
    plt.savefig(direct_plots + time + '.png', format = 'png')
    #plt.show()  

    plt.figure()    
    sb.boxplot(data = df_phase_log, x = 'intensity', y = 'MEP size in µV', hue= 'phase')
    plt.title('Phase comparison for all intensities at ' + time + '\n log transformed')
    plt.ylabel('log of MEP size (+2)')
    plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
    plt.savefig(direct_plots + time + '_LOG.png', format = 'png')
    #plt.show()

df_phase_alltime = pd.DataFrame.from_dict(df_phase_alltime)
df_phase_alltime_log = pd.DataFrame.from_dict(df_phase_alltime_log)

plt.figure()    
sb.boxplot(data = df_phase_alltime, x = 'intensity', y = 'MEP size in µV', hue= 'phase')
plt.title('Phase comparison for all intensities')
plt.ylabel('average MEP (peak to peak amplitude) in µV')
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
plt.savefig(direct_plots + 'all_times.png', format = 'png')
#plt.show()

plt.figure()    
sb.boxplot(data = df_phase_alltime_log, x = 'intensity', y = 'MEP size in µV', hue= 'phase')
plt.title('Phase comparison for all intensities with log transformed data')
plt.ylabel('log of MEP size (+2)')
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
plt.savefig(direct_plots + 'all_times_LOG.png', format = 'png')
#plt.show()

#%% Save data frame
outfile = outpath + 'allTimes.pkl'
df_phase_alltime.to_pickle(outfile)
outfile = outpath + 'allTimes_log.pkl'
df_phase_alltime_log.to_pickle(outfile)
