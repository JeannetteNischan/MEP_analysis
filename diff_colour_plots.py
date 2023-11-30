import matplotlib.pyplot as plt 
direct = directory('...')

#%% define functions

# 1.plot all average MEP sizes for all intensities over time
def plot_MEP(groupAVG, timepoints):
    plt.figure() #open new figure
    colour = ['red','green','skyblue','orange','cyan','yellow','blueviolet','greenyellow','blue'] #define colours of choice
    i = 0 #set counter for colour
    for intensity in groupAVG.keys(): #iterate over intensities (from 80-160, keys in dictionary in my case)
        y = [] #y values as empty list for every new intensity
        x = [] #x also
        for time in timepoints:       #iterate over timepoints 
            y.append(groupAVG[intensity][time][0]) # 'fill' y with data
            x.append(time)
        plt.plot(x,y, marker='D', color = colour[i], linestyle='-', label = intensity + '%RMT') #plot each pair of x and y values
        i += 1 #update colour counter
    plt.legend() #when all lines are plottet, add legend, title, lables, ...
    plt.grid(which='both', axis='y', c = 'gray', linestyle=':')
    plt.title('average ipsilesional/contralateral MEP sizes over time')
    plt.ylabel('MEP size in µV')   
    plt.show() #either show figure or save with next two lines. Both doesn't work somehow
    #plt.savefig(direct + 'groupplot.png', format = 'png')  
    #plt.close() 
