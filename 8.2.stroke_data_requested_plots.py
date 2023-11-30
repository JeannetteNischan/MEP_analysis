'''8.2. MEP analysis script
preceeded by 7a.stroke_data_plotIO_include

followed by 8.stroke_data_stats

Author: Jeannette Nischan
Date of 1st Version: 14th March 2023
-> different timepoint names <-
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
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO_include/namingV/'
timepoints = ['V4','V6'] 
tps = ['V2','V3','V4','V5','V6']

#%% define functions
#1. plot MEP occurrences for each timepoint seperately
def plotMEPocc_IO(tps, groupAVG):
    for time in tps:
        y = []
        y_err = []
        x = []
        for intensity in groupAVG[time].keys():
            y.append(groupAVG[time][intensity][2])
            y_err.append(groupAVG[time][intensity][3])
            x.append(intensity)
        plt.plot(x,y, 'gd-')  
        plt.errorbar(x,y, yerr = y_err) 
        plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
        plt.title('average ipsilesional/contralateral MEP occurrence per intensity at ' + time)
        plt.ylabel('relative amount of MEP occurrence')  
        plt.xlabel('% RMT') 
        plt.show()  

#1.1 log transformed MEP occurrences
def plotMEPocc_logIO(tps, groupLOG):
    for time in tps:
        y = []
        y_err = []
        x = []
        for intensity in groupLOG[time].keys():
            y.append(groupLOG[time][intensity][2])
            y_err.append(groupLOG[time][intensity][3])
            x.append(intensity)
        plt.plot(x,y, 'gd-')  
        plt.errorbar(x,y, yerr = y_err) 
        plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
        plt.title('average log transformed ipsilesional/contralateral MEP occurrence per intensity at ' + time)
        plt.ylabel('log10 of relative amount of MEP occurrence')  
        plt.xlabel('% RMT') 
        plt.show()

#2. MEP occurrences at V4 and V6 with errorbars
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

#3. MEP occurrences log transformed
""" def plot_Occ_log(groupLOG, timepoints):
    plt.figure()
    colour = ['red','green','skyblue','orange','cyan','yellow','blueviolet','greenyellow','blue'] 
    i = 0
    for intensity in groupLOG[timepoints[i]].keys():
        y_occ = []
        y_occ_sem = []
        x = [] 
        for time in timepoints:
            y_occ.append(groupLOG[time][intensity][2])
            y_occ_sem.append(groupLOG[time][intensity][3])   
            x.append(time)
        plt.plot(x,y_occ, marker='D', color = colour[i], linestyle='-', label = intensity + '%RMT')
        plt.errorbar(x,y_occ, yerr = y_occ_sem, ecolor= colour[i], linestyle = '')
        i += 1
    plt.legend() 
    plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
    plt.title('average ipsilesional/contralateral log transformed MEP occurrences \n in all accepted trials over time')
    plt.ylabel('log10 of relative amount of MEP occurrences')   
    plt.xlabel('Timepoint')
    plt.show() 
 """

#%% call functions
with open(direct + 'groupAVG.json') as json_file:
    groupAVG = json.load(json_file)

with open(direct + 'groupLOG.json') as json_file:
    groupLOG = json.load(json_file)

plotMEPocc_IO(tps, groupAVG)
#plot_Occ(groupAVG, timepoints)
#plot_Occ_log(groupLOG, timepoints)    #log of occurrences does not exist right now in the dict