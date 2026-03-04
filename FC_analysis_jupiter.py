# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: base
#     language: python
#     name: python3
# ---

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd

# %%
weights = np.array([106,160,214,267,389,510,631,751,871,991,1115,1236,1291,1345,1399])

sAp1times = np.array([15,38,60,79,100,119,140,166,186,206,230,252,270,295,312])
sAp2times = np.array([0,24,49,72,93,113,131,157,182,203,220,240,260,280,298])
sAp3times = np.array([1,24,46,66,88,105,125,145,166,183,205,225,244,262,279])
sAp4times = np.array([0,20,39,60,91,112,130,147,165,185,203,220,240,263,281])
sAp5times = np.array([1,19,50,70,99,119,137,156,178,200,219,239,255,275,292])
sAp6times = np.array([0,23,41,60,81,101,119,138,158,176,195,213,231,250,269])
sAp7times = np.array([0,19,39,57,77,96,117,137,159,179,199,219,240,259,279])

sBp1times = np.array([0,22,40,57,77,97,115,136,155,175,193,211,228,245,262])
sBp2times = np.array([0,18,38,57,77,95,118,137,156,179,197,216,234,253,270])
sBp3times = np.array([0,19,40,58,76,95,114,134,158,175,193,212,231,249,268])
sBp4times = np.array([0,26,44,62,82,101,119,136,155,175,195,214,230,246,264])
sBp5times = np.array([0,19,39,68,86,104,122,141,159,175,192,208,226,243,259])
sBp6times = np.array([0,22,40,59,77,94,112,129,146,165,183,199,216,234,252])
sBp7times = np.array([1,17,35,52,70,88,106,124,141,157,174,192,210,229,249])


# %%
def matrix(fileName, sensorNum, ptimes, weights):

    sxpx = pd.read_csv(fileName)
    counter = np.trunc(np.array(sxpx['time'].values))
    pressures = np.array(sxpx[sensorNum].values)

    idx = np.ravel([np.where(counter == a) for a in ptimes]) #add something if number doesn't show up
    #print(idx)
    #REMEMBER TO CHECK IDX THAT IT ALL CORRELATES TO REAL VALUES
    #in case I accidentally rounded


    #averages and SDs
    averages = np.zeros_like(idx, float)
    stdevs = np.zeros_like(idx, float)

    full = np.zeros([len(idx),10])

    for b in np.arange(0,len(idx)):
        i = np.arange(idx[b],idx[b]+10) #taking the values for each set of 10 times after the initial time
        
        full[b,:] = pressures[i]

        averages[b] = np.mean(pressures[i])
        stdevs[b] = np.std(pressures[i])
        
    stdmatrix = np.hstack(stdevs)
    avgmatrix = np.column_stack((weights,averages))
    return avgmatrix, stdmatrix


# %%
sAp1, stdsAp1 = matrix('sensorA_p1_FC.csv', 's1',sAp1times,weights)
sAp2, stdsAp2 = matrix('sensorA_p2_FC.csv', 's2',sAp2times,weights)
sAp3, stdsAp3 = matrix('sensorA_p3_FC.csv', 's3',sAp3times,weights)
sAp4, stdsAp4 = matrix('sensorA_p4_FC.csv', 's4',sAp4times,weights)
sAp5, stdsAp5 = matrix('sensorA_p5_FC.csv', 's5',sAp5times,weights)
sAp6, stdsAp6 = matrix('sensorA_p6_FC.csv', 's6',sAp6times,weights)
sAp7, stdsAp7 = matrix('sensorA_p7_FC.csv', 's7',sAp7times,weights)

sBp1, stdsBp1 = matrix('sensorB_p1_FC.csv', 's1',sBp1times,weights)
sBp2, stdsBp2 = matrix('sensorB_p2_FC.csv', 's2',sBp2times,weights)
sBp3, stdsBp3 = matrix('sensorB_p3_FC.csv', 's3',sBp3times,weights)
sBp4, stdsBp4 = matrix('sensorB_p4_FC.csv', 's4',sBp4times,weights)
sBp5, stdsBp5 = matrix('sensorB_p5_FC.csv', 's5',sBp5times,weights)
sBp6, stdsBp6 = matrix('sensorB_p6_FC.csv', 's6',sBp6times,weights)
sBp7, stdsBp7 = matrix('sensorB_p7_FC.csv', 's7',sBp7times,weights)


# %%
def makePlots(data, std, sensorNum):
    #Data must be in order from 1=>5
    #SensorNum must be an Int
    
    opt = ['red','green','blue','darkorange','violet','skyblue','pink']
    names = ['Position1', 'Position2', 'Position3','Position4','Position5','Position6','Position7']

    m = np.zeros(7)
    b = np.zeros(7)

    

    for d in np.arange(0,len(data)):
        e = data[d]
        x=e[:,0]
        y=e[:,1]

        #line of best fit
        m[d], b[d] = np.polyfit(x,y,deg=1)

        plt.scatter(x,y, c=opt[d])
        plt.plot(x,m[d]*x+b[d],c=opt[d], label = names[d]+ f" {m[d]:.2f}*x={b[d]:.2f}")
        plt.errorbar(x,y,std[d],fmt='o', color=opt[d])
        
    plt.xlabel("Applied Weights (g)")
    plt.ylabel("Recorded Pressure (kPa)")
    plt.legend(bbox_to_anchor=(1.05, 1),
                         loc='upper left', borderaxespad=0.)
    plt.title("Sensor " + sensorNum)
        


    plt.show()
    return m,b

# %%
sAdata = [sAp1,sAp2,sAp3,sAp4,sAp5,sAp6,sAp7]
print(len(sAdata))
sAdev = [stdsAp1, stdsAp2, stdsAp3, stdsAp4, stdsAp5, stdsAp6, stdsAp7]
mA, bA = makePlots(sAdata,sAdev,"A")

# %%
sBdata = [sBp1,sBp2,sBp3,sBp4,sBp5,sBp6,sBp7]
sBdev = [stdsBp1, stdsBp2, stdsBp3, stdsBp4, stdsBp5, stdsBp6, stdsBp7]
mB, bB = makePlots(sBdata,sBdev,"B")
