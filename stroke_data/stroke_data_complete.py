'''2.1 stroke_data_complete
Script to fill in the missing data for stimulation intensity
for some patients via user input'''

import json
from time import time
import pandas as pd

#load json file with the dictionary where info about which subject is missing is stored
with open('/home/jeanettenischan/Data/data_INTENS_TMS/stim_intens_miss.json') as json_file:
    stim_intens_miss = json.load(json_file)
    print(stim_intens_miss)


for ID in stim_intens_miss.keys():
    subject_dict = pd.read_json('/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/' 
                               + ID + '.json').to_dict()
    for timepoint in stim_intens_miss[ID]:
        stim_intens = input('Please enter the stilumation intensities for subject '
                           + ID + ' at timepoint ' + timepoint + ' :')
        if timepoint in ['pre1_0' , 'pre1_180']:                   
            subject_dict['pre1'][timepoint]['stim_intens'] = stim_intens
        else:
            subject_dict[timepoint]['stim_intens']   

        df = pd.DataFrame.from_dict(subject_dict) 
        df.to_json ('/home/jeanettenischan/Data/data_INTENS_TMS/ProcessedData/' + ID + '.json')
