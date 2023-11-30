## Get phases for IO curves
# %% Import modules
from scipy import io
import numpy as np
import os
import matplotlib.pyplot as plt

# %% Load example file
direct  = '/home/jeanettenischan/Data/data_INTENS_TMS/data/' #main folder with all subject subfolder
# Create a list of folder names as subject id
subject_ids = os.listdir(direct)



for ID in subject_ids:
    timepoints= os.listdir(direct + ID)
    for timepoint in timepoints:
        datapath = direct + ID + '/' + timepoint + '/IO_ipsilesional.mat'
        if os.path.isfile(datapath):
            # Load data
            data = io.loadmat(datapath)

        # get phase information from spongebob marker
            sp_marker = data["spongebob_timeseries"] # has 13 channels; 12 = target phase, 11 = trigger (yes, no)

        # Plot channel 12 and 11 
        #fig = plt.figure(dpi=300)
            plt.plot(sp_marker[:,12]) # Here you can see that first: 0° until approx. half of the measurement; then: 180°
#phase= np.where(sp_marker[:,12] == 180)
#print(phase)
#phase_change = phase[0][0]
#print(phase_change)

#fig = plt.figure(dpi=300)
            plt.plot(sp_marker[:,11]) # here you can see 1 if pulse has been triggered and 0 if  not. The gap at around 400000 (for this example dataset) is a short break inbetween the two IO curves and for each curve, you can nicely see 5 blocks (4x20 stim; 1x10 stim --> inbetween were a couple of seconds break)


# %% The timestamps of these two markers is identical
""" I would suggest to find the time of the jump from 0° to 180° in chan 12 and then cound the trig (=1) in chan 11. 
Then you know how many pulses of your data were applied at which phase.
As sometimes, the borders are not as clear as for this example set, see for example AmWo at post1, I would furthermore integrate a criterium to take the jump but only if phase has been 0 for at least 100000 ms beforehand (or something like that)"""

# might be useful:
test = np.where(sp_marker[:,11] == 1) # gives you the index of trigger points
triggercount = np.size(test) # amount of triggers; shoul dbe indentical with number of tms_artifact
#print(test)
#print(triggercount)