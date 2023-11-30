'''1. script for MEP analysis of stroke patient data
prepares the data so all is in the same format. Imports xdf files and creates .mat files
followed by script 2 'stroke_data_loadandepoch' 
Author: Jeannette Nischan
Date of first version: 31. May 2022'''

#%% 1. import all tools and libraries
from liesl.api import XDFFile
import pyxdf
import numpy as np
import os
import fnmatch
from scipy import io
from scipy.io import loadmat

#%% 2. Predefine variables and conditions
# key of interest (recorded physiological data)
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/data/' #main folder with all subject subfolders
subjects = ['015','011','014']
filename = 'IO_ipsilesional'

#%% . prepare data for processing

# 1.1 define function to list all relevant (ipsilesional) xdf files
def find_files(direct):
    ''' finds .xdf files in the given directory for a given subject (alias) that contain the string <ipsilesional>
    https://stacktuts.com/how-to-iterate-over-files-in-directory-using-python-with-example-code
    https://stackoverflow.com/questions/36294712/python-filename-contains-string-metachar'''
    xdf_files = []
    for root, dirs, files in os.walk(direct):
        for file in files:
            if file.endswith('.xdf') and fnmatch.fnmatch(file, "*"+"ipsilesional"+"*"): # and fnmatch.fnmatch(file, '*'+ 'ioc'+ '*'): 
                xdf_files.append(os.path.join(root, file))  

    return xdf_files

def get_ids(file_array):
    subject_ids = []
    for i in range(len(file_array)):
        subject = str(file_array[i][48:51])
        if subject not in subject_ids and subject != '016':
            subject_ids.append(subject)
    return subject_ids    
       
# 1.2 define a function to load xdf files and save as a matfile
def xdf_to_mat(alias, file_array):
    patient_id = alias
    for i in range(len(file_array)):
        file_name = file_array[i]
        xdf_file = XDFFile(file_array[i])
        chan = xdf_file["BrainVision RDA"].channel_labels
        sp_phase = xdf_file["Spongebob-Data"].time_series[:, 12]# 9
        sp_trigger = xdf_file["Spongebob-Data"].time_series[:,11]
        trigger = np.where(sp_trigger==1)[0]
        sp_pd = []
        for ts in trigger:
            phase = sp_phase[trigger]
            sp_pd.append(phase) 

        first_pdRMT = trigger[0]
        last_pdRMT = trigger[-1]
        sp_tstamp = xdf_file["Spongebob-Data"].time_stamps                     
        bv_tstamp = xdf_file["BrainVision RDA"].time_stamps
        bv_tseries = xdf_file["BrainVision RDA"].time_series
        sp_tseries = xdf_file["Spongebob-Data"].time_series
        # Trigger for first hemipshere according to spongebob:
        bv_trigidx_0 = []

        for ts in trigger: # find closest tstamps in EMG (BrainVision RDA)
        # sp_trigger = xdf["Spongebob-Data"].time_series[ts, 11]
            sp_trig = xdf_file["Spongebob-Data"].time_stamps[ts]
            bv_trig = np.argmin(np.abs(bv_tstamp - sp_trig))
        # bv_tstamps = bv_tstamp[trigger_according_to_sp]
            bv_trigidx_0.append(bv_trig)

        # Get  phase 
        emg_data = xdf_file["BrainVision RDA"].time_series

        gmfp = np.std(emg_data[:, 0:64], 1)
        aptp = []
        arttrig = []

        # find artifact via gmfp for first hem
        for onset in bv_trigidx_0:
            artifact = gmfp[onset-150 : onset+150]
            aptp.append(np.ptp(artifact))
            arttrig.append(int(np.argmax(artifact) - 150 + onset)) # find artifact via gmfp

        tms_artifact = np.array(arttrig)    

        data_IO = {
            "channel_label": chan, "BrainVisionRDA_stamps": bv_tstamp, 
            "BrainVisionRDA_series": bv_tseries, "tms_artifact": tms_artifact,
            "spongebob_timeseries": sp_tseries, "spongebob_timestamps": sp_tstamp
                  }

        if '_0_ipsilesional' in str(file_name): 
            hemisphere = 'ipsilesional_0'
        elif '_180_' in str(file_name):
            hemisphere = 'ipsilesional_180'   


        filename = direct + "/" + patient_id + "/pre1/" + "IO_" + hemisphere + ".mat"
        io.savemat(filename, data_IO)

# 1.3 define function to concatenate 180 and 0 from same patient
#def merge_files(direct, subjects, filename):
    #for i in subjects:
        #hem_0   = loadmat(direct  + i + '/pre1/' + filename + '_0.mat')
        #hem_180 = loadmat(direct  + i + '/pre1/' + filename + '_180.mat')
        
        #np.concatenate((hem_0['BrainVisionRDA_stamps'],hem_180['BrainVisionRDA_stamps']),axis=None)
        #np.concatenate((hem_0['BrainVisionRDA_series'], hem_180['BrainVisionRDA_series']),axis=None)
        #np.concatenate((hem_0['tms_artifact'][0],hem_180['tms_artifact'][0]),axis=None)
        #print(hem_0['tms_artifact'])
        #np.concatenate((hem_0['spongebob_timeseries'],hem_180['spongebob_timeseries']),axis=None)
        #np.concatenate((hem_0['spongebob_timestamps'],hem_180['spongebob_timestamps']),axis=None)
        #ds = [hem_0, hem_180]
        #d = {}
        #for k in hem_0.keys():
        #    d[k] = tuple(d[k] for d in ds)

        #file_name = direct + "/" + i + "/pre1/" + "IO_ipsilesional.mat"
        #io.savemat(file_name, hem_0)    
       

#%% Iterate over patient folders and check if preparation is neccessary
xdf_files = find_files(direct)
#print(xdf_files)
subject_ids = get_ids(xdf_files)
print(subject_ids)

for alias in subject_ids:
    xdf_to_mat(alias, xdf_files)
    #merge_files(direct,subjects,filename)