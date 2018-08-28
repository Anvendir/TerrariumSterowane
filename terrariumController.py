#!/usr/bin/python3

import sys
sys.path.append("./subrepos/Adafruit_Python_DHT")
import Adafruit_DHT
import requests
from gpiozero import Energenie

def getHumidityAndTemperature():
    sensorModel = Adafruit_DHT.DHT22
    firstSensorGpio = 4
    secondSensorGpio = 26

    firstSensorHumidity, firstSensorTemperature = Adafruit_DHT.read_retry(sensorModel, firstSensorGpio)
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(firstSensorTemperature, firstSensorHumidity))

    secondSensorHumidity, secondSensorTemperature = Adafruit_DHT.read_retry(sensorModel, secondSensorGpio)
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(secondSensorTemperature, secondSensorHumidity))

    humidity = (firstSensorHumidity + secondSensorHumidity) / 2
    temperature = (firstSensorTemperature + secondSensorTemperature) / 2

    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    return {humidity, temperature}

hum, temp = getHumidityAndTemperature()
thingSpeakIoTKey = "8N9BL598BIFY4LV7"
requests.post('https://api.thingspeak.com/update.json', data = {'api_key':thingSpeakIoTKey, 'field1':temp, 'field2':hum})

Energenie(3, initial_value=False)

print ("Bla")
