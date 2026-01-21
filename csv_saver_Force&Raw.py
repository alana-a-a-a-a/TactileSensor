import serial
import csv
import time
import pressuretoforce as ptf
#import matplotlib.pyplot as plt
#import numpy as np

PORT = "COM4"      # change to your QT Py port
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)
start = time.monotonic()

## try to make continuosly updating plot

with open("Run1_RawPressures") as r, open("Run1_Force") as f:
    writer_r = csv.writer(r)
    writer_r.writerow(["time", "s1", "s2", "s3", "s4", "s5", "s6", "s7"])

    writer_f = csv.writer(f)
    writer_f.writerow(["time", "s1", "s2", "s3", "s4", "s5", "s6", "s7"])
    #time[s] pressure [kPa]


    while True:
        line = ser.readline().decode().strip()
        if not line:
            continue
        pressures = line.split(",")
        if len(pressures) != 7:
            continue
        
        t =time.monotonic()-start
        writer_r.writerow([t] + pressures)

        r.flush()  # makes the CSV continuously update on disk
        print(t, pressures)

         #assuming everything happens at the center
        pressures = [float(x) for x in pressures]
        forces = ptf.ptoforces(pressures,3)
        writer_f.writerow([t] + forces)
        f.flush()
        print(t,forces)


                     
