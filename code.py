import board
import busio
from ms5837 import MS5837
import adafruit_tca9548a
from adafruit_bus_device.i2c_device import I2CDevice
import time

i2c = board.STEMMA_I2C()
tca = adafruit_tca9548a.TCA9548A(i2c)

SENSOR_I2C_ADDRESS = 0x76
num_sens = 7

sensors = []
for i in range(num_sens):
    device = I2CDevice(tca[i], SENSOR_I2C_ADDRESS)
    sensor = MS5837(device)
    sensor.init()      # Initializes calibration for each sensor
    sensors.append(sensor)

pressures = [0]*num_sens
tare = [0]*num_sens

def sensorpressures(s):
    for idx, s in enumerate(s):
        s.read()  # Triggers sensor measurement, updates compensation
        pressures[idx] = s.pressure() # units: kPa
    return pressures
tare = sensorpressures(sensors)

while True:
    orig_pressures = sensorpressures(sensors)
    pressures = [a-b for a,b in zip(orig_pressures, tare)]
    print(",".join("{:.4f}".format(p) for p in pressures))
    #print((pressures[0],pressures[1],pressures[2],pressures[3],pressures[4],pressures[5],pressures[6])) #formatted like this for plotter
    #do i want a time.sleep()?
