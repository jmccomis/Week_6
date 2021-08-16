from flask import Flask,jsonify
from threading import Thread, Event
from time import sleep
import random

import Adafruit_DHT as dht

from gpiozero import Button,LED
DHT = 4
led= LED(18)


temperatureSetpoint = 78
workerEvent = Event()

# Call setLED(True) to turn LED on, setLED(False) to turn LED off
def setLED(state):
    ### TODO:  Replace this with code to actually use the LED ###
    if state == True:
        led.on()
    else:
        led.off()

# Get a reading from the temperature sensor
def readTemperature():
    ### TODO:  Replace this with code to actually read the sensor and return the temperature ###
    h,t = dht.read_retry(dht.DHT22, DHT)
    x=(t*9/5)+32
    
    return x #(W.temperature('fahrenheit').get('temp'))

# Set the temperature setpoint
def configureSetpoint(value):
    global temperatureSetpoint
    print ('Changing setpoint to ' + str(value))
    temperatureSetpoint = value


# Function to run in the worker thread
def workerThreadFunction():
    global workerEvent
    global temperatureSetpoint
    while True:
        if workerEvent.is_set():
            print ('Ending worker thread function')
            break

        else:
            temperature = readTemperature()
            print ('Temperature: ' + str(temperature))

            if temperature > temperatureSetpoint:
                setLED(True)
            else:
                setLED(False)

            sleep(5)


# Web server application
webApplication = Flask(__name__)

# Route to read temperature with a GET request
@webApplication.route('/Temperature', methods=['GET'])
def getTemperature():
    global temperatureSetpoint
    return jsonify({'temperature': readTemperature(), 'setpoint': temperatureSetpoint})

# Route to set setpoint with PUT request
@webApplication.route('/Temperature/Setpoint/<int:value>', methods=['PUT'])
def putSetpoint(value):
    global temperatureSetpoint
    configureSetpoint(value)
    return jsonify({'temperature': readTemperature(), 'setpoint': temperatureSetpoint})


# Launch worker thread
print ('Starting worker thread...')
workerThread = Thread(target = workerThreadFunction)
workerThread.start()


# Run web server (program blocks on this call until server is stopped)
print ('Starting web server...')
try:
    webApplication.run(host = '0.0.0.0', port = 5000)
except:
    print ('Failed to start web server')


# Web server stopped, shut down worker thread
print ('Shutting down...')
workerEvent.set()
workerThread.join()
