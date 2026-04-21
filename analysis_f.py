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
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import linecache

# %%
import sys
np.set_printoptions(threshold=sys.maxsize)

# %%
clawdata_file = 'high_rate_sample_f_20260410.txt'

# %%

notes = [] #times that each new sample starts
samples = [] #names of samples
tot_lines = sum(1 for _ in open(clawdata_file,'r',errors='ignore'))

with open(clawdata_file,'r',errors='ignore') as clawdata:
    p_matrix, v_matrix, c_matrix = [np.zeros([tot_lines+1,2]) for m in range(3)]
    t_matrix = np.zeros([tot_lines+1,8])
    CMD_matrix = np.zeros([tot_lines+1,4], dtype=object)

    for line_num, line in enumerate(clawdata,1):
        c = line.strip().split(',')
        final_time = float(c[0])
        if 'NOTE' in line:
            notes.append(c[0])
            samples.append(c[2])
        if c[1] == 'POS':
            p_matrix[line_num] = [c[0],c[3]]
        elif c[1] == 'VEL':
            v_matrix[line_num] = [c[0],c[3]]
        elif c[1] == 'CUR':
            c_matrix[line_num] = [c[0],c[3]]
        elif c[1] == 'TACTILE':
            try:
                t_matrix[line_num] = np.array([c[0]]+c[2:])
            except ValueError:
                pass
        elif c[1] == 'CMD':
            CMD_matrix[line_num]=c[:]
        else: 
            pass

ms = [p_matrix, v_matrix, c_matrix, t_matrix, CMD_matrix] #Full data, from start to finish
[p_matrix, v_matrix, c_matrix, t_matrix, CMD_matrix] = [m[~np.all(m == 0, axis=1)] for m in ms]

ms = [p_matrix, v_matrix, c_matrix, t_matrix, CMD_matrix] #Full data, from start to finish



# %%
def timesBetween(M, start, end):
    indices = np.zeros(2)
    times = M[:,0].astype(float)
    indices[0] = int(np.argmax(times > start))
    indices[1] = int(len(times)-1-np.argmax((times < end)[::-1]))
    return indices.astype(int)


# %%
#designate for each sample
n = 1 #<- # sample, index through each, starts at 0

def forEachSample(n): 
    if n+1 >= len(notes): #if sample is either the last or past the last, the last range is the end
        end_idx = final_time
    else:
        end_idx = [n+1]

    range = np.array([notes[n], end_idx],dtype=float)
   
    cmd_idx = timesBetween(CMD_matrix,range[0],range[1])
    #print(cmd_idx)

    Case1 = []
    Case2 = []
    Case3 = []

    for i in np.arange(int(cmd_idx[0]),int(cmd_idx[1])):
        if CMD_matrix[i,2] == 'POS' and CMD_matrix[i,3] == '30' and CMD_matrix[i+1,2] == 'POS' and CMD_matrix[i+1,3] == '0':
            #Case 1
            Case1.append(i+1)
        ''''
        elif CMD_matrix[i,2] == 'POS' and CMD_matrix[i,3] == '30' and CMD_matrix[i+1,2] == 'CUR' and CMD_matrix[i+1,3] == '500':
            #Case 2
            Case1.append(CMD_matrix[i+1,0])

        elif CMD_matrix[i,2] == 'POS' and CMD_matrix[i,3] == '30' and CMD_matrix[i+1,2] == 'CUR' and CMD_matrix[i+1,3] == '1000':
            #Case 3
            Case1.append(CMD_matrix[i+1,0])

        '''
    Case1 = np.array(Case1, dtype=int)

    return Case1, Case2, Case3

C1, C2, C3 = forEachSample(0)
#[A, B, C, D, E, F] = [forEachSample(t) for t in np.arrange(0,len(notes))]


# %%
##Functions of Time

def plot_one_case(Case, c, SampleName, endTOI=None):
    
    
    fig, axs = plt.subplots(4,1,figsize=(15,15))
    fig.suptitle(SampleName, y=0.93)
    if c==1: S = 'POS 30 -> POS 0'
    elif c==1: S = 'POS 30 -> CUR 500'
    elif c==2: S = 'POS 30 -> CUR 1000'

    fig.text(0.5, 0.90,f'Case{c}: {S}' , ha='center', fontsize=12)

    #Each figure should have 3 trials, maps each trial together
    for e in np.arange(0,len(Case)):
        start = float(CMD_matrix[Case[e],0])
        #print(start)
        if endTOI == None:
            if e+1 <=len(Case):
                end = float(CMD_matrix[Case[e]+1,0])
            else:
                end = float(final_time)
        else: 
            end = start + endTOI

    #tactile
    #ms[:5]

        [t1, t2] = timesBetween(t_matrix,start, end)
        colors = ['blue', 'blueviolet', 'mediumorchid', 'violet', 'magenta', 'deeppink', 'lightpink']
        for p in np.arange(1,8):
            initialtime = t_matrix[t1,0]
            x = t_matrix[t1:t2,0]-initialtime
            if e == 0:
                axs[0].scatter(x,t_matrix[t1:t2,p], c=colors[p-1],s=5, label = f"Sensor {p}")
            else:
                axs[0].scatter(x,t_matrix[t1:t2,p], c=colors[p-1],s=5)      


    #position, velocity, current
        odata = ['Position', 'Velocity', 'Current']
        colors = ['r','g','b']
        for i, otype in enumerate(odata):
            matrix = ms[i] #p, v, c
            [t1, t2] = timesBetween(matrix,start, end)
            initialtime = matrix[t1,0]
            x = matrix[t1:t2,0]-initialtime
            axs[i+1].scatter(x,matrix[t1:t2,1], c=colors[i],s=5)
            axs[i+1].set_title(otype)
            axs[i+1].set_xlabel('Time [s]')
            axs[i+1].set_ylabel(otype) #add units

    axs[0].set_title('Tactile')
    axs[0].legend()
    axs[0].set_xlabel('Time [s]')
    axs[0].set_ylabel('Pressure [kPa]')
    plt.subplots_adjust(hspace=0.5, wspace=0.3)
    plt.show()
    return None


# %%
plot_one_case(C1, 1, 'Sample F',2)
'''
for s in [A, B, C, D, E, F]
    plot_one_case(s[0], 1, f'Sample {s}')
    plot_one_case(s[1], 2, f'Sample {s}')
    plot_one_case(s[2], 3, f'Sample {s}')


'''
