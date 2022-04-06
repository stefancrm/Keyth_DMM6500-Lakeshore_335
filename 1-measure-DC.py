import sys
import time
import pyvisa as visa
import keyboard
import csv
from lakeshore.model_335 import *
from DMM6500 import DMM6500
from DMM6500_SCPI import Function

timestr = time.strftime("%m_%d_%H-%M")

filename = timestr+"-DCV.csv"

print (filename)
#-------Set filname save folder

exitProgram = False

# prepare to exit the program
def quit():
    global exitProgram
    exitProgram=True

# set hotkey    
keyboard.add_hotkey('q', lambda: quit())

#---------------------------------------------- DMM6500 Settings
try:
    rm = visa.ResourceManager()
    DMM = DMM6500(rm.open_resource('USB0::0x05E6::0x6500::04500037::INSTR'))
except ValueError:
    print('Could not connect to DMM6500 multimeter.')
    exit(1)

DMM.reset()
DMM.function = Function.DC_VOLTAGE
DMM.range = 'auto'
DMM.nplc = 4.0

#---------------------------------------------- Lakeshore 335 Settings
# Connect to the first available Model 335 temperature controller over USB using a baud rate of 57600
try:
    my_model_335 = Model335(57600)
except ValueError:
    print('Could not connect to Temperature Controller.')
    exit(1)    
# Create a new instance of the input sensor settings class
sensor_settings = Model335InputSensorSettings(Model335InputSensorType.DIODE, True, False,
                                              Model335InputSensorUnits.KELVIN,
                                              Model335DiodeRange.TWO_POINT_FIVE_VOLTS)
# Apply these settings to input A of the instrument
my_model_335.set_input_sensor("A", sensor_settings)
my_model_335._get_identity

# Collect instrument data
heater_output_1 = my_model_335.get_heater_output(1)
temperature_reading = my_model_335.get_all_kelvin_reading()

t1 = time.time()

def measure_and_save():
    t3 = time.time()
    seconds = "{0:.2f}".format(t3-t1)
    temperature = temperature_reading[0]
    voltage = DMM.measure()
    f.write(str(seconds) + " , " + str(temperature) + " , " + str(voltage) + " \n")
    print (str(seconds) + " , " + str(temperature) + " , " +  str(voltage) )
    
    #print("{0:.2f} s ".format(t3-t1)+ str(temperature_reading[0]) + " K ", DMM.measure()," V")
    time.sleep(2)


with open(filename , "w") as f:
    f.write("Seconds s," + "Temperature K," + "Voltage V")
    print("Seconds s," + "Temperature K," + "Voltage V")
    f.write("\n")
    while not exitProgram:
        measure_and_save()

if keyboard.is_pressed("q"):
    print(keyboard.is_pressed("q"))
    f.close() 
    sys.exit()

print("Data Aquisition finished")
sys.exit()
