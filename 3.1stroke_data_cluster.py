'''3.1 script for MEP analysis
loads epoched data from script 3 'stroke_data_epoch'
and extracts the intensity value to perform a cluster analysis. 
Followed by script 4. 'stroke_data_visual'
Author: Jeannette Nischan
Date of first version: Nov 18th 2022'''

#%%import tools and libraries
import os
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
import random
import statistics
#from scipy.cluster.hierarchy import linkage
#from pathlib import Path


#%% define paths and variables
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/Epochs/'
target_direct = '/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/IO/'
figures_direct = '/home/jeanettenischan/Data/data_INTENS_TMS/Clustering_anomalies/'
timepoints = os.listdir(direct)
# load file with info of subjects and timepoints where stim intensity is missing
with open('/home/jeanettenischan/Data/data_INTENS_TMS/stim_intens_miss_corrected.json') as json_file:
    missing_intens = json.load(json_file)



#%% define functions

#1. load intensity values and plot
def load_intensities (data):
    '''iterates over epochs in given data (nested dict) and extracts the intensity values
    into a list. Loads two other functions
    Input: nested dict with epoched data
    Output: nested dict with epoched data with decoded/replaced intensity values
    
    Author: Jeannette Nischan
    Date of first version: Nov 16th 2022'''
    #predefine empty list
    intensities = []
    #iterate over epochs, extract intensity and store in list
    for epoch in data.keys():
        trial = data[epoch]
        intensities.append(trial['intensity'])
    l = len(intensities)  
    # call function to cluster values
    labels, save = cluster_data(intensities, l)
    #call function to decode values with real intensities (in percent of resting motor threshold (RMT))
    if save == 'yes':
        intens_new = replace_values(labels, intensities)
        #iterate over epochs again to replace values
        i = 0
        for epoch in data.keys():
            trial = data[epoch]
            trial['intensity'] = intens_new[i]
            i +=1

    return data, save

#2. cluster intensities
def cluster_data(intensities, l):
    '''Uses hierachical clustering from sklearn module to combine values into 9 different clusters
    uses random y-value assignment for plotting, shows result as scatterplot for visual inspection
    option to repeat analysis
    https://www.w3schools.com/python/python_ml_hierarchial_clustering.asp
    
    Input: list with intensity values and lenght of that list
    Output: list with cluster labels
    Author: Jeannette Nischan
    First working version: Nov 18th 2022'''
    #linkage(data, method= 'ward', metric='euclidean')
    hierarchical_cluster = AgglomerativeClustering(n_clusters=9, affinity='euclidean', linkage='ward')
    inspect = 'r'
    while inspect != 'c':
        y = []
        for ind in range(0,l):
            n = random.uniform(0,1)
            y.append(n)   
        data_intens = list (zip(intensities,y))
        labels = hierarchical_cluster.fit_predict(data_intens)
        plt.figure()
        plt.rcParams['image.cmap'] = 'nipy_spectral' #choose a colormap with 9 distinct colours
        scatter = plt.scatter(intensities, y, c=labels)
        plt.legend(handles = scatter.legend_elements()[0], labels = range(0,9))
        plt.title('subject ' + alias[0:3] + ' at timepoint ' + timepoint)
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        plt.show(block=False)
        inspect = input('Visual inspection ok? \n enter -r- to repeat, -n- to not save data or -c- to continue: ')
        if inspect == 'n':
            save = 'no'
            plt.savefig(figures_direct + alias[0:3] + timepoint + '.png', format = 'png')
            inspect = 'c'
        else:
            save = 'yes' 
        plt.close()      
    return labels, save

#3. replace values
def replace_values(labels, intensities):
    '''Function to decode intensity values from dataset 
    and replace with real value (80 to 160% resting motor threshold (RMT) in steps of 10)
    
    Input: list with labels
    Output: list with real intensities in percent RMT
    Author: Jeannette Nischan
    first working version: Nov 21st 2022'''
    #predefine lists
    intens_new = []
    intens_mean = []
    cl_nr = []

    #convert list to numpy array to use where()
    intensities = np.array(intensities)

    #iterate over cluster numbers to find corresponding values
    for i in range(0,9):
        #find indices of labels with same cluster number
        cl_ind = np.where(labels == i)
        #convert array to list
        cl_ind = cl_ind[0].tolist()
        #compute average of all values with same cluster number and append mean value to list
        intens_mean.append(statistics.mean(list(intensities[cl_ind])))
        #append corresponding cluster number to list 
        cl_nr.append(i)

    #combine average value and clusternumber and sort list
    data_intens = list (zip(intens_mean,cl_nr))
    data_intens.sort()

    #define minimum value of resting motor threshold in percent
    RMT = 80
    intens_new = labels.copy() 

    #iterate over list with labels and replace them with %RMT value
    for i in range(0, len(data_intens)): #from 0 to max number of clusters
        #replace cluster number with intensity
        intens_new[intens_new == data_intens[i][1]] = RMT
        #increase intensity by 10
        RMT += 10
  
    return intens_new          




#%%iterate over timepoints and subjects
for timepoint in timepoints:
    subjects = os.listdir(direct + timepoint)
    subjects_list = subjects.copy()
    for alias in subjects:
        #check in list if intensity value for this subject at this timepoint is missing
        if alias[0:3] in missing_intens.keys() and timepoint in missing_intens[alias[0:3]]:
            print('Intensity for '+ alias + ' at ' + timepoint + ' is missing!')
        #if not, load data
        else:   
            print('Begin subject ' + alias[0:3] + ' at ' + timepoint) 
            data = pd.read_json( direct + timepoint + '/' + alias).to_dict()
            #pass data to funcion(s)
            data, save = load_intensities(data)
            #create pandas dataframe from data dict
            df = pd.DataFrame.from_dict(data) 
            if save == 'yes':
                #save as json file (alias in this case is already a string with .json at the end)
                if os.path.exists(target_direct + timepoint): # check if folder already exists
                    df.to_json (target_direct + timepoint + '/' + alias)
                else:
                    os.makedirs(target_direct + timepoint) # otherwise create folder
                    df.to_json (target_direct + timepoint + '/' + alias)
        #copy subjects in order not to remove alias from there        
        #remove alias when done
        subjects_list.remove(alias)
        #save upcated subject list for possible reloading after crash
        with open(target_direct + timepoint + '/subjects.json', 'w') as file:
            json.dump(subjects_list, file)
        print('Finished subject ' + alias[0:3] + ' at ' + timepoint)     
