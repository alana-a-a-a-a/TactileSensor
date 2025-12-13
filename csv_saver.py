import serial
import csv
import time
#import matplotlib.pyplot as plt
#import numpy as np

PORT = "COM4"      # change to your QT Py port
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)
start = time.monotonic()

## try to make continuosly updating plot

with open("sensor1_position5.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["time", "s1", "s2", "s3", "s4", "s5", "s6", "s7"])
    #time[s] pressure [kPa]


    while True:
        line = ser.readline().decode().strip()
        if not line:
            continue
        pressures = line.split(",")
        if len(pressures) != 7:
            continue
        
        t =time.monotonic()-start
        writer.writerow([t] + pressures)
        f.flush()  # makes the CSV continuously update on disk
        print(t, pressures)
    
                     
