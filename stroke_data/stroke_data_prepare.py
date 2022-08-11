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

#%% 2. Predefine variables and conditions
# key of interest (recorded physiological data)
direct = '/home/jeanettenischan/Data/data_INTENS_TMS/data/' #main folder with all subject subfolders


#%% . prepare data for processing

# 1.1 define function to list all relevant (ipsilesional) xdf files
def find_files(direct):
    ''' finds .xdf files in the given directory for a given subject (alias) that contain the string <ipsilesional>
    https://stacktuts.com/how-to-iterate-over-files-in-directory-using-python-with-example-code
    https://stackoverflow.com/questions/36294712/python-filename-contains-string-metachar'''
    xdf_files = []
    for root, dirs, files in os.walk(direct):
        for file in files:
            if file.endswith('.xdf') and fnmatch.fnmatch(file, "*"+"ipsilesional"+"*"): 
                xdf_files.append(os.path.join(root, file))             
    return xdf_files

def get_ids(file_array):
    subject_ids = []
    for i in range(len(file_array)):
        subject = str(file_array[i][48:51])
    if subject not in subject_ids:
        subject_ids.append(subject)
    return subject_ids    
       


# 1.2 define a function to load xdf files and save as a matfile
def xdf_to_mat(alias, file_array):
    patient_id = alias
    for i in range(len(file_array)):
        if alias in file_array[i] and '_180_' in file_array[i]:
            hemisphere = 'ipsilesional180'
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
            filename = direct + "/" + patient_id + "/pre1/" + "IO_" + hemisphere + ".mat"
            io.savemat(filename, data_IO)

        elif alias in file_array[i] and '_0_' in file_array[i]:
            hemisphere = 'ipsilesional0'
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
            filename = direct + "/" + patient_id + "/pre1/" + "IO_" + hemisphere + ".mat"
            io.savemat(filename, data_IO)

#%% Iterate over patient folders and check if preparation is neccessary
xdf_files = find_files(direct)
subject_ids = get_ids(xdf_files)

for alias in subject_ids:
    xdf_to_mat(alias, xdf_files)