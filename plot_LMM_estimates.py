#%%import tools and libraries
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np


#%% define paths and fixed variables if needed
direct = '/home/jeanettenischan/Desktop/'

#load all needed csv files with fixed effect estimates
file_name = direct + 'LMM_Estimates_ipsi_time.csv'
ipsi_time = pd.read_csv(file_name)

file_name = direct + 'LMM_Estimates_contra_time.csv'
contra_time = pd.read_csv(file_name)

file_name = direct + 'LMM_Estimates_ipsi_intens.csv'
ipsi_intens = pd.read_csv(file_name)

file_name = direct + 'LMM_Estimates_contra_intens.csv'
contra_intens = pd.read_csv(file_name)


#%%plot
c=0
errors = ipsi_time['Error'].tolist()
plt.figure(dpi=130)
ax = sb.barplot(data=ipsi_time, x='Timepoint', y='Estimate', hue='cat')
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
for i in [-0.2,0.2,0.8,1.2,1.8,2.2,2.8,3.2]:
    plt.errorbar(i, ipsi_time['Estimate'][c], yerr=errors[c], color='black')
    c += 1

plt.legend(loc='upper left')
plt.show()


# Set the width of the bars
bar_width = 0.85

# Set the positions of the bars on the x-axis (respective Timepoints and Intensities)
x1 = ipsi_time.query("cat == 'Timepoint'")['Timepoint'].tolist()  #['V3','V4','V5','V6']
# Convert column with intensity labels from integer to string
ipsi_intens['Intensity'] = ipsi_intens['Intensity'].astype("string")
x2 = ipsi_intens.query("cat == 'Intensity'")['Intensity'].tolist()

#get y values
y1  = ipsi_time.query("cat == 'Timepoint'")['Estimate'].tolist() #get estimate values where category is Timepoint
y2 = ipsi_time.query("cat == 'Intercept'")['Estimate'].tolist()
y3 = ipsi_time.query("cat == 'Intercept'")['Error'].tolist()
errors = ipsi_time.query("cat == 'Timepoint'")['Error'].tolist()

#1.1 plot timepoints
plt.figure(dpi=130)
plt.bar(x1, y1, color='skyblue', width=bar_width, label='Timepoint')
#add intercept as solid line and +/- error as dashed lines
plt.hlines(y2[0],-0.4, 3.4 , colors='orange', linestyles='solid', label='Intercept')
plt.hlines(y2[0]+y3[0],-0.4, 3.4 , colors='orange', linestyles='dashed')
plt.hlines(y2[0]-y3[0],-0.4, 3.4 , colors='orange', linestyles='dashed')
# add predefined error bars
for i in range(len(x1)):
    plt.errorbar(i, y1[i], yerr=errors[i], color='black', elinewidth=1, capsize=2)

# adapt to x axis
plt.xticks(range(len(x1)), x1)
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
plt.legend()
plt.title('Fixed effect estimates for each timepoint with std. error \n and intercept with std. error (ipsilesional)')
plt.show()

#1.2 plot for contralesional side
y1  = contra_time.query("cat == 'Timepoint'")['Estimate'].tolist() #get estimate values where category is Timepoint
y2 = contra_time.query("cat == 'Intercept'")['Estimate'].tolist()
y3 = contra_time.query("cat == 'Intercept'")['Error'].tolist()
errors = contra_time.query("cat == 'Timepoint'")['Error'].tolist()

plt.figure(dpi=130)
plt.bar(x1, y1, color='skyblue', width=bar_width, label='Timepoint')
#add intercept as solid line and +/- error as dashed lines
plt.hlines(y2[0],-0.4, 3.4 , colors='orange', linestyles='solid', label='Intercept')
plt.hlines(y2[0]+y3[0],-0.4, 3.4 , colors='orange', linestyles='dashed')
plt.hlines(y2[0]-y3[0],-0.4, 3.4 , colors='orange', linestyles='dashed')
# add predefined error bars
for i in range(len(x1)):
    plt.errorbar(i, y1[i], yerr=errors[i], color='black', elinewidth=1, capsize=2)

# adapt to x axis
plt.xticks(range(len(x1)), x1)
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
plt.legend()
plt.title('Fixed effect estimates for each timepoint with std. error \n and intercept with std. error (contralesional)')
plt.show()


#2. plot intensities
#2.1 ipsilesional
y1  = ipsi_intens.query("cat == 'Intensity'")['Estimate'].tolist() #get estimate values where category is Timepoint
y2 = ipsi_intens.query("cat == 'Intercept'")['Estimate'].tolist()
y3 = ipsi_intens.query("cat == 'Intercept'")['Error'].tolist()
errors = ipsi_intens.query("cat == 'Intensity'")['Error'].tolist()

plt.figure(dpi=130)
plt.bar(x2, y1, color='skyblue', width=bar_width, label='Intensity')
#add intercept as solid line and +/- error as dashed lines
plt.hlines(y2[0],-0.4, 7.4 , colors='orange', linestyles='solid', label='Intercept')
plt.hlines(y2[0]+y3[0],-0.4, 7.4  , colors='orange', linestyles='dashed')
plt.hlines(y2[0]-y3[0],-0.4, 7.4 , colors='orange', linestyles='dashed')
# add predefined error bars
for i in range(len(x2)):
    plt.errorbar(i, y1[i], yerr=errors[i], color='black', elinewidth=1, capsize=2)

# adapt to x axis
plt.xticks(range(len(x2)), x2)
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
plt.legend()
plt.title('Fixed effect estimates for each Intensity with std. error \n and intercept with std. error (ipsilesional)')
plt.show()

#2.2 contralesional
y1  = contra_intens.query("cat == 'Intensity'")['Estimate'].tolist() #get estimate values where category is Timepoint
y2 = contra_intens.query("cat == 'Intercept'")['Estimate'].tolist()
y3 = contra_intens.query("cat == 'Intercept'")['Error'].tolist()
errors = contra_intens.query("cat == 'Intensity'")['Error'].tolist()

plt.figure(dpi=130)
plt.bar(x2, y1, color='skyblue', width=bar_width, label='Intensity')
#add intercept as solid line and +/- error as dashed lines
plt.hlines(y2[0],-0.4, 7.4  , colors='orange', linestyles='solid', label='Intercept')
plt.hlines(y2[0]+y3[0],-0.4, 7.4 , colors='orange', linestyles='dashed')
plt.hlines(y2[0]-y3[0],-0.4, 7.4  , colors='orange', linestyles='dashed')
# add predefined error bars
for i in range(len(x2)):
    plt.errorbar(i, y1[i], yerr=errors[i], color='black', elinewidth=1, capsize=2)

# adapt to x axis
plt.xticks(range(len(x2)), x2)
plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
plt.legend()
plt.title('Fixed effect estimates for each Intensity with std. error \n and intercept with std. error (contralesional)')
plt.show()