#%%import tools and libraries
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb






#%% define paths and fixed variables if needed
phases = ['0','180']
#time = 'V3' 
timepoints = ['V2','V3','V4','V5','V6']
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/'


data0   = pd.read_json(direct + 'phase0_group_avgs.json').to_dict()
data180 = pd.read_json(direct + 'phase180_group_avgs.json').to_dict()
x = []
x1 = []
y = []
for time in timepoints:
    for intensity in data0.keys():
        #pd.DataFrame.insert(180)
        x.append(data0[intensity][time])
        x1.append(data180[intensity][time])
        y.append(intensity)

    plt.figure()    
    plt.boxplot(x, labels = y)
    #sb.boxplot(data = data0, x = 'intensity', y = 'MEP sizes in µV', hue= 'phase')
    plt.boxplot(x1, labels = y)
    plt.show()    
