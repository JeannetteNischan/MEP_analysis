'''8.1. MEP analysis script
preceeded by 7a.stroke_data_plotIO_include

followed by 8.stroke_data_stats

Author: Jeannette Nischan
Date of 1st Version: 14th March 2023
-> different timepoint names <-
-> only two timepoints in comparison, with all available data (regardless of patient ID)
'''

#%%import tools and libraries
import matplotlib.pyplot as plt
import json

#%% define paths and fixed variables if needed
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/'
timepoints = ['pre','post']
shift = 0.4


#%% define functions
# 1.plot all average MEP sizes for all intensities over time
def plot_MEP(groupAVG, timepoints):
    plt.figure()
    colour = ['red','green','skyblue','orange','cyan','yellow','blueviolet','greenyellow','blue'] 
    i = 0
    for intensity in groupAVG[timepoints[i]].keys():
        y = []
        y_err = []
        x = [] 
        for time in timepoints:       
            y.append(groupAVG[time][intensity][0])
            y_err.append(groupAVG[time][intensity][1])
            x.append(time)
        plt.plot(x,y, marker='D', color = colour[i], linestyle='-', label = intensity + '%RMT')
        plt.errorbar(x,y, yerr = y_err, ecolor= colour[i], linestyle = '')
        i += 1
    plt.legend() 
    plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
    plt.title('average ipsilesional/contralateral MEP sizes over time')
    plt.ylabel('MEP size in µV')   
    plt.xlabel('timepoint')
    plt.show()
    #plt.savefig(direct + 'groupplot.png', format = 'png')  
    #plt.close()        


#2. plot log MEP sizes 
def plot_log(groupLOG, timepoints):
    plt.figure()
    colour = ['red','green','skyblue','orange','cyan','yellow','blueviolet','greenyellow','blue'] 
    i = 0
    for intensity in groupLOG[timepoints[i]].keys():  
        y_log = []
        y_log_sem = []
        x = [] 
        for time in timepoints:     
            y_log.append(groupLOG[time][intensity][0])
            y_log_sem.append(groupLOG[time][intensity][1])
            x.append(time)
        plt.plot(x,y_log, marker='D', color = colour[i], linestyle='-', label = intensity + '%RMT')
        plt.errorbar(x,y_log, yerr = y_log_sem, ecolor= colour[i], linestyle = '')
        i += 1
    plt.legend() 
    plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
    plt.title('average ipsilesional/contralateral logarithmic MEP sizes over time')
    plt.ylabel('log transformed MEP size')  
    plt.xlabel('Timepoint') 
    plt.show() 
    #plt.savefig(direct + 'groupplot_log.png', format = 'png')  
    #plt.close()


#3.plot MEP occurrences
def plot_Occ(groupAVG, timepoints):
    plt.figure()
    colour = ['red','green','skyblue','orange','cyan','yellow','blueviolet','greenyellow','blue'] 
    i = 0
    for intensity in groupAVG[timepoints[i]].keys():
        y_occ = []
        y_occ_sem = []
        x = [] 
        for time in timepoints:
            y_occ.append(groupAVG[time][intensity][2])
            y_occ_sem.append(groupAVG[time][intensity][3])   
            x.append(time)
        plt.plot(x,y_occ, marker='D', color = colour[i], linestyle='-', label = intensity + '%RMT')
        plt.errorbar(x,y_occ, yerr = y_occ_sem, ecolor= colour[i], linestyle = '')
        i += 1
    plt.legend() 
    plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
    plt.title('average ipsilesional/contralateral MEP occurrences \n in all accepted trials over time')
    plt.ylabel('relative amount of MEP occurrences')   
    plt.xlabel('Timepoint')
    plt.show()
    #plt.savefig(direct + 'groupplot_occurrence.png', format = 'png')  
    #plt.close()

#4. plot all I/O curves in one plot
def plot_IO(groupAVG, timepoints):
    plt.figure()
    colour = ['red','skyblue']
    i = 0
    for time in timepoints:
        y = []
        x = []
        y_sem = []
        for intensity in groupAVG[time].keys():
            if time == 'post':
                x.append(int(intensity) + shift)
            else:
                x.append(int(intensity) - shift)
            y.append(groupAVG[time][intensity][0])
            y_sem.append(groupAVG[time][intensity][1])
        plt.plot(x,y, marker = 'D', linestyle='-', color = colour[i], label = time) 
        plt.errorbar(x,y, yerr = y_sem, ecolor= colour[i], linestyle = '')   
        i += 1
        
    plt.legend()
    plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
    plt.title('Input/Output curves for ipsilesional/contralateral MEP sizes')
    plt.ylabel('average MEP sizes in µV')   
    plt.xlabel('% RMT')
    plt.show() 
    #plt.savefig(direct + 'groupplot_log.png', format = 'png')  
    #plt.close()    

#5. plot all logarithmic I/O curves in one plot
def plot_logIO(groupLOG, timepoints):
    plt.figure()
    colour = ['red','skyblue']
    i = 0
    for time in timepoints:
        y = []
        x = []
        y_sem = []
        for intensity in groupLOG[time].keys():
            if time == 'post':
                x.append(int(intensity) + shift)
            else:
                x.append(int(intensity) - shift)
            y.append(groupLOG[time][intensity][0])
            y_sem.append(groupLOG[time][intensity][1])
        plt.plot(x,y, marker = 'D', linestyle='-', color = colour[i], label = time) 
        plt.errorbar(x,y, yerr = y_sem, ecolor= colour[i], linestyle = '')  
        i += 1
    plt.legend()
    plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
    plt.title('Input/Output curves for ipsilesional/contralateral log transformed MEP sizes')
    plt.ylabel('average log(MEP sizes in µV)')  
    plt.xlabel('% RMT')
    plt.show() 
       
#5. plot I/O curve for occurrences
def plot_occIO(groupAVG, timepoints):
    plt.figure()
    colour = ['red','skyblue']
    i = 0
    for time in timepoints:
        y = []
        x = []
        y_sem = []
        for intensity in groupAVG[time].keys():
            if time == 'post':
                x.append(int(intensity) + shift)
            else:
                x.append(int(intensity) - shift)
            y.append(groupAVG[time][intensity][2])
            y_sem.append(groupAVG[time][intensity][3])
        plt.plot(x,y, marker = 'D', linestyle='-', color = colour[i], label = time) 
        plt.errorbar(x,y, yerr = y_sem, ecolor= colour[i], linestyle = '')   
        i += 1
    plt.legend()
    plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
    plt.title('Input/Output curves for ipsilesional/contralateral MEP occurences')
    plt.ylabel('relative amount of MEP occurrences')   
    plt.xlabel('% RMT')
    plt.ylim([0,1])
    plt.show()
    

#%% call functions
with open(direct + 'groupAVG.json') as json_file:
    group = json.load(json_file)

groupAVG = {}
groupAVG['pre'] = group['V2']
groupAVG['post'] = group['V4']

with open(direct + 'groupLOG.json') as json_file:
    groupL = json.load(json_file)

groupLOG = {}
groupLOG['pre'] = groupL['V2']
groupLOG['post'] = groupL['V4']    

#plot_MEP(groupAVG, timepoints)
#plot_log(groupLOG, timepoints)
#plot_Occ(groupAVG, timepoints)
#plot_IO(groupAVG, timepoints)
plot_logIO(groupLOG, timepoints)
plot_occIO(groupAVG, timepoints)

