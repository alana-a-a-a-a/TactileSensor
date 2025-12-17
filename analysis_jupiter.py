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

# %%
ap_weights = np.array([82,136,190,243,364,485,606,725,905,1026,1150,1270,1324,1379,1433])

## SENSOR 1
s1p1times = np.array([0,30,65,90,130,205,259,285,320,355,369,400,425,450,475])
s1p2times = np.array([0,30,69,90,110,140,170,220,245,495,275,361,385,410,430])
s1p3times = np.array([0,30,55,80,105,125,160,185,215,250,290,320,345,365,390])
s1p4times = np.array([0,55,80,105,130,155,180,210,255,290,325,350,370,390,410])
s1p5times = np.array([0,35,65,90,125,145,180,235,265,290,319,345,380,410,435])

s2p1times = np.array([0,29,54,85,115,135,160,190,220,249,274,300,325,350,375])
s2p2times = np.array([0,25,50,75,95,115,140,180,211,240,274,299,325,340,355])
s2p3times = np.array([0,20,130,60,160,200,290,240,340,360,385,405,425,445,470])
s2p4times = np.array([0,25,50,75,95,115,135,165,200,220,245,265,284,300,320])
s2p5times = np.array([0,30,51,75,100,120,150,175,200,314,345,370,390,410,430])

s3p1times = np.array([0,25,41,61,80,100,125,145,176,200,225,250,275,300,320])
s3p2times = np.array([0,75,95,120,140,161,185,200,230,255,275,300,320,345,361])
s3p3times = np.array([0,20,60,80,100,125,150,175,200,230,251,280,300,316,335])
s3p4times = np.array([0,20,40,60,80,100,120,139,170,195,215,235,260,280,300])
s3p5times = np.array([1,25,45,60,80,100,129,160,190,210,235,260,284,304,325])

#Senso4 4 not testing p1 and p5
s4p2times = np.array([0,25,50,70,95,115,135,155,190,220,245,265,290,310,325])
s4p3times = np.array([0,25,50,70,95,115,135,160,200,230,261,285,304,330,351])
s4p4times = np.array([1,30,50,75,95,120,140,160,210,230,255,275,295,320,340])

s5p1times = np.array([0,20,40,60,85,105,125,150,210,235,260,280,295,315,330])
s5p2times = np.array([1,30,50,70,91,111,130,150,185,210,230,250,270,290,309])
s5p3times = np.array([0,25,50,75,95,120,140,160,194,220,240,265,285,305,324])
s5p4times = np.array([0,25,45,105,125,145,165,185,220,245,275,300,320,340,359])
s5p5times = np.array([0,25,45,65,85,110,130,150,180,205,231,251,270,285,300])

s6p1times = np.array([0,30,60,85,105,130,150,170,201,280,311,380,401,435,450])
s6p2times = np.array([0,20,65,119,140,160,186,215,256,276,299,375,395,435,451])
s6p3times = np.array([0,25,45,65,100,121,145,165,204,235,255,280,300,316,335])
s6p4times = np.array([0,25,45,65,90,110,130,151,196,220,245,270,285,300,320])
s6p5times = np.array([0,20,50,70,90,110,155,175,210,231,251,274,296,316,339])

s7p1times = np.array([0,20,40,60,145,165,186,215,244,264,285,305,325,345,365])
s7p2times = np.array([1,30,70,90,111,131,155,180,225,250,275,295,315,335,355])
s7p3times = np.array([0,20,40,60,81,105,126,150,185,211,236,260,280,299,319])
s7p4times = np.array([1,30,50,86,125,145,170,190,210,235,259,280,300,320,340])
s7p5times = np.array([1,30,50,69,95,114,134,154,175,195,230,250,270,295,315])


# %%
def matrix(fileName, sensorNum, ptimes, weights):

    sxpx = pd.read_csv(fileName)
    counter = np.trunc(np.array(sxpx['time'].values))
    pressures = np.array(sxpx[sensorNum].values)*10 ##THIS IS JUST FOR THIS SET OF DATA BC I CONVERTED WRONG

    idx = np.ravel([np.where(counter == a) for a in ptimes]) #add something if number doesn't show up
    #print(idx)
    #REMEMBER TO CHECK IDX THAT IT ALL CORRELATES TO REAL VALUES
    #in case I accidentally rounded
    #in future have code detect where weight changes are made


    #averages and SDs
    averages = np.zeros_like(idx, float)
    stdevs = np.zeros_like(idx, float)

    full = np.zeros((10,len(idx)))

    for b in np.arange(0,len(idx)):
        i = np.arange(idx[b],idx[b]+10)
        
        full[:,b] = pressures[i]

        averages[b] = np.mean(pressures[i])
        stdevs[b] = np.std(pressures[i])
    stdmatrix = np.hstack(stdevs)
    avgmatrix = np.column_stack((weights,averages))
    return avgmatrix, stdmatrix


# %%
def makePlots(data, std, sensorNum):
    #Data must be in order from 1=>5
    #SensorNum must be an Int

    fig, ax = plt.subplots(3,2,figsize=(15,15))
    axs = [ax[0,0],ax[0,1],ax[1,0],ax[1,1],ax[2,0],ax[2,1]]

    axs[0].set_title("Sensor " +str(sensorNum))
    
    opt = ['red','green','blue','darkorange','violet','skyblue','pink']
    names = ['Position1', 'Position2', 'Position3','Position4','Position5']


    for d in np.arange(0,len(data)):
        e = data[d]
        x=e[:,0]
        y=e[:,1]

        #line of best fit
        m, b = np.polyfit(x,y,deg=1)
        for i in [0,d+1]:
            axs[i].set_xlabel("Applied Weights (g)")
            axs[i].set_ylabel("Recorded Pressure (kPa)")
            axs[i].scatter(x,y, c=opt[d], label = names[d])
            axs[i].plot(x,m*x+b,c=opt[d],label=f"{m:.2f}*x={b:.2f}")
            axs[i].errorbar(x,y,std[d],fmt='o', color=opt[d])

        axs[d+1].legend()


    plt.show()
    return None


# %%
def makeJust4Plots(data, std, sensorNum):
    #Data must be in order from 1=>5
    #SensorNum must be an Int

    fig, ax = plt.subplots(2,2,figsize=(15,15))
    axs = [ax[0,0],ax[0,1],ax[1,0],ax[1,1]]

    axs[0].set_title("Sensor " +str(sensorNum))
    
    opt = ['green','blue','darkorange','violet','skyblue','pink']
    names = ['Position2', 'Position3','Position4','Position5']


    for d in np.arange(0,len(data)):
        e = data[d]
        x=e[:,0]
        y=e[:,1]

        #line of best fit
        m, b = np.polyfit(x,y,deg=1)
        for i in [0,d+1]:
            axs[i].set_xlabel("Applied Weights (g)")
            axs[i].set_ylabel("Recorded Pressure (kPa)")
            axs[i].scatter(x,y, c=opt[d], label = names[d])
            axs[i].plot(x,m*x+b,c=opt[d],label=f"{m:.2f}*x={b:.2f}")
            axs[i].errorbar(x,y,std[d],fmt='o', color=opt[d])

        axs[d+1].legend()


    plt.show()
    return None

# %%
s1p1, stds1p1 = matrix('sensor1_position1.csv', 's1',s1p1times,ap_weights)
s1p2, stds1p2 = matrix('sensor1_position2.csv', 's1',s1p2times,ap_weights)
s1p3, stds1p3 = matrix('sensor1_position3.csv', 's1',s1p3times,ap_weights)
s1p4, stds1p4 = matrix('sensor1_position4.csv', 's1',s1p4times,ap_weights)
s1p5, stds1p5 = matrix('sensor1_position5.csv', 's1',s1p5times,ap_weights)

s2p1, stds2p1 = matrix('sensor2_position1.csv', 's2',s2p1times,ap_weights)
s2p2, stds2p2 = matrix('sensor2_position2.csv', 's2',s2p2times,ap_weights)
s2p3, stds2p3 = matrix('sensor2_position3.csv', 's2',s2p3times,ap_weights)
s2p4, stds2p4 = matrix('sensor2_position4.csv', 's2',s2p4times,ap_weights)
s2p5, stds2p5 = matrix('sensor2_position5.csv', 's2',s2p5times,ap_weights)

s3p1, stds3p1 = matrix('sensor3_position1.csv', 's3',s3p1times,ap_weights)
s3p2, stds3p2 = matrix('sensor3_position2.csv', 's3',s3p2times,ap_weights)
s3p3, stds3p3 = matrix('sensor3_position3.csv', 's3',s3p3times,ap_weights)
s3p4, stds3p4 = matrix('sensor3_position4.csv', 's3',s3p4times,ap_weights)
s3p5, stds3p5 = matrix('sensor3_position5.csv', 's3',s3p5times,ap_weights)

s4p2, stds4p2 = matrix('sensor4_position2.csv', 's4',s4p2times,ap_weights)
s4p3, stds4p3 = matrix('sensor4_position3.csv', 's4',s4p3times,ap_weights)
s4p4, stds4p4 = matrix('sensor4_position4.csv', 's4',s4p4times,ap_weights)

s5p1, stds5p1 = matrix('sensor5_position1.csv', 's5',s5p1times,ap_weights)
s5p2, stds5p2 = matrix('sensor5_position2.csv', 's5',s5p2times,ap_weights)
s5p3, stds5p3 = matrix('sensor5_position3.csv', 's5',s5p3times,ap_weights)
s5p4, stds5p4 = matrix('sensor5_position4.csv', 's5',s5p4times,ap_weights)
s5p5, stds5p5 = matrix('sensor5_position5.csv', 's5',s5p5times,ap_weights)

s6p1, stds6p1 = matrix('sensor6_position1.csv', 's6',s6p1times,ap_weights)
s6p2, stds6p2 = matrix('sensor6_position2.csv', 's6',s6p2times,ap_weights)
s6p3, stds6p3 = matrix('sensor6_position3.csv', 's6',s6p3times,ap_weights)
s6p4, stds6p4 = matrix('sensor6_position4.csv', 's6',s6p4times,ap_weights)
s6p5, stds6p5 = matrix('sensor6_position5.csv', 's6',s6p5times,ap_weights)

s7p1, stds7p1 = matrix('sensor7_position1.csv', 's7',s7p1times,ap_weights)
s7p2, stds7p2 = matrix('sensor7_position2.csv', 's7',s7p2times,ap_weights)
s7p3, stds7p3 = matrix('sensor7_position3.csv', 's7',s7p3times,ap_weights)
s7p4, stds7p4 = matrix('sensor7_position4.csv', 's7',s7p4times,ap_weights)
s7p5, stds7p5 = matrix('sensor7_position5.csv', 's7',s7p5times,ap_weights)

# %%
plottingplans1 = [s1p1,s1p2,s1p3,s1p4,s1p5]
stdev1 = [stds1p1,stds1p2,stds1p3,stds1p4,stds1p5]
makePlots(plottingplans1,stdev1,1)

# %%
plottingplans2 = [s2p1,s2p2,s2p3,s2p4,s2p5]
stdev2 = [stds2p1,stds2p2,stds2p3,stds2p4,stds2p5]
makePlots(plottingplans2,stdev2,2)

# %%
plottingplans3 = [s3p1,s3p2,s3p3,s3p4,s3p5]
stdev3 = [stds3p1,stds3p2,stds3p3,stds3p4,stds3p5]
makePlots(plottingplans3,stdev3,3)

# %%
plottingplans4 = [s4p2,s4p3,s4p4]
stdev4 = [stds4p2,stds4p3,stds4p4]
makeJust4Plots(plottingplans4,stdev4,4)

# %%
plottingplans5 = [s5p1,s5p2,s5p3,s5p4,s5p5]
stdev5 = [stds5p1,stds5p2,stds5p3,stds5p4,stds5p5]
makePlots(plottingplans5,stdev5,5)

# %%
plottingplans6 = [s6p1,s6p2,s6p3,s6p4,s6p5]
stdev6 = [stds6p1,stds6p2,stds6p3,stds6p4,stds6p5]
makePlots(plottingplans6,stdev6,6)

# %%
plottingplans7 = [s7p1,s7p2,s7p3,s7p4,s7p5]
stdev7 = [stds7p1,stds7p2,stds7p3,stds7p4,stds7p5]
makePlots(plottingplans7,stdev7,7)
