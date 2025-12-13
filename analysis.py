import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


## SENSOR 1

ap_weights = np.array([0,54,107,161,282,403,525,645,765,886,1009,1131,1185,1239,1294])
s1p1times = np.array([0,25,50,81,105,121,150,170,189,207,230,245,265,285,301])
s1p2times = np.array([0,30,50,70,90,115,135,155,171,190,210,225,241,270,290])
s1p3times = np.array([0,20,39,59,79,95,115,160,245,265,285,300,320,340,360])


def matrix(fileName, sensorNum, ptimes, weights):

    sxpx = pd.read_csv(fileName)
    counter = np.trunc(np.array(sxpx['time'].values))
    pressures = np.array(sxpx[sensorNum].values)

    idx = np.ravel([np.where(counter == a) for a in ptimes]) #add something if number doesn't show up
    #print(idx)
    #REMEMBER TO CHECK IDX THAT IT ALL CORRELATES TO REAL VALUES
    #in case I accidentally rounded
    #in future have code detect where weight changes are made


    #averages and SDs
    averages = np.zeros_like(idx, float)
    stdevs = np.zeros_like(idx, float)

    full = np.zeros((len(idx),len(idx)))

    for b in np.arange(0,len(idx)):
        i = np.arange(idx[b],idx[b]+10)

        averages[b] = np.mean(pressures[i])
        stdevs[b] = np.std(pressures[i])

    fullmatrix = np.column_stack((weights,averages))
    return fullmatrix
#also have it plot w/o averages too


s1p1 = matrix('sensor1_position1.csv', 's1',s1p1times,ap_weights)
s1p2 = matrix('sensor1_position2.csv', 's1',s1p2times,ap_weights)
s1p3 = matrix('sensor1_position3.csv', 's1',s1p3times,ap_weights)

plottingplans = [s1p1,s1p2,s1p3]

plt.xlabel("Applied Weights (g)")
plt.ylabel("Recorded Pressure (kPa)")
opt = ['red','green','blue','orange']
names = ['position1', 'position2', 'position3']

for d in np.arange(0,len(plottingplans)):
    e = plottingplans[d]
    x=e[:,0]
    y=e[:,1]

    #line of best fit, use log scale for axes?

    plt.scatter(x,y, c=opt[d], label = names[d])
    plt.legend()

plt.show()





#print(counter[])
