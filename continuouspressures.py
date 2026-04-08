import serial
import csv
import time
import threading

#import matplotlib.pyplot as plt
#import numpy as np

PORT = "COM4"      # change to your QT Py port
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=0.1)

class continuouspressures:
        def __init__(self):
            self.data = None
            self.running = True

            self._thread = threading.Thread(target=self._background_loop, daemon=True)
            self._thread.start()

        def _backgroundloop(self):
              while self.running:
                    self.data = ser.readline().decode().strip()
        def value(self):
              return self.data

