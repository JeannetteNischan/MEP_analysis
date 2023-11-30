'''8. MEP analysis script
preceeded by 7a.stroke_data_plotIO_include

followed by 8.stroke_data_stats
Author: Jeannette Nischan
Date of 1st Version: 23rd Jan 2023
'''

#%%import tools and libraries
import pandas as pd
import os
from os.path import join
import matplotlib.pyplot as plt
import collections
import json
from math import log
import numpy as np

#%% define paths and fixed variables if needed
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/'
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/'
timepoints = ['pre1','post1','pre3','post3','post5']


#%% define functions
# 1.plot all average MEP sizes for all intensities over time
def plot_MEP(groupAVG, timepoints):
    plt.figure()
    colour = ['red','green','skyblue','orange','cyan','yellow','blueviolet','greenyellow','blue'] 
    i = 0
    for intensity in groupAVG.keys():
        y = []
        x = [] 
        for time in timepoints:       
            y.append(groupAVG[intensity][time][0])
            x.append(time)
        plt.plot(x,y, marker='D', color = colour[i], linestyle='-', label = intensity + '%RMT')
        i += 1
    plt.legend() 
    plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
    plt.title('average ipsilesional/contralateral MEP sizes over time')
    plt.ylabel('MEP size in µV')   
    #plt.show()
    plt.savefig(direct + 'groupplot.png', format = 'png')  
    plt.close()        


#2. plot log MEP sizes 
def plot_log(groupLOG, timepoints):
    plt.figure()
    colour = ['red','green','skyblue','orange','cyan','yellow','blueviolet','greenyellow','blue'] 
    i = 0
    for intensity in groupLOG.keys():
        y_log = []
        x = [] 
        for time in timepoints:       
            y_log.append(groupLOG[intensity][time])
            x.append(time)
        plt.plot(x,y_log, marker='D', color = colour[i], linestyle='-', label = intensity + '%RMT')
        i += 1
    plt.legend() 
    plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
    plt.title('average ipsilesional/contralateral logarithmic MEP sizes over time')
    plt.ylabel('log transformed MEP size')   
    #plt.show() 
    plt.savefig(direct + 'groupplot_log.png', format = 'png')  
    plt.close()


#3.plot MEP occurrences
def plot_Occ(groupAVG, timepoints):
    plt.figure()
    colour = ['red','green','skyblue','orange','cyan','yellow','blueviolet','greenyellow','blue'] 
    i = 0
    for intensity in groupAVG.keys():
        y_occ = []
        x = [] 
        for time in timepoints:
            y_occ.append(groupAVG[intensity][time][1])   
            x.append(time)
        plt.plot(x,y_occ, marker='D', color = colour[i], linestyle='-', label = intensity + '%RMT')
        i += 1
    plt.legend() 
    plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
    plt.title('average ipsilesional/contralateral MEP occurrences  in all accepted trials over time')
    plt.ylabel('relative amount of MEP occurrences')   
    #plt.show()
    plt.savefig(direct + 'groupplot_occurrence.png', format = 'png')  
    plt.close()

#4. plot all I/O curves in one plot
def plot_IO()
#5.statistical analysis
def stats(groupAVG, groupLOG):
    

#%% call functions
with open(direct + 'groupAVG.json') as json_file:
    groupAVG = json.load(json_file)

with open(direct + 'groupLOG.json') as json_file:
    groupLOG = json.load(json_file)

plot_MEP(groupAVG, timepoints)
plot_log(groupLOG, timepoints)
plot_Occ(groupAVG, timepoints)
stats(groupAVG, groupLOG)
