#!/usr/bin/python3

import sys
sys.path.append("./subrepos/Adafruit_Python_DHT")
import Adafruit_DHT
import requests
from gpiozero import Energenie
from time import sleep

def getHumidityAndTemperature():
    sensorModel = Adafruit_DHT.DHT22
    firstSensorGpio = 4
    secondSensorGpio = 26

    firstSensorHumidity, firstSensorTemperature = Adafruit_DHT.read_retry(sensorModel, firstSensorGpio)
    print('Read out #1: Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(firstSensorTemperature, firstSensorHumidity))

    secondSensorHumidity, secondSensorTemperature = Adafruit_DHT.read_retry(sensorModel, secondSensorGpio)
    print('Read out #2: Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(secondSensorTemperature, secondSensorHumidity))

    humidityAvg = (firstSensorHumidity + secondSensorHumidity) / 2
    temperatureAvg = (firstSensorTemperature + secondSensorTemperature) / 2

    print('Read out #AVG Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperatureAvg, humidityAvg))
    return (humidityAvg, temperatureAvg)

enableHeaterTemperature_Celsius = 25
disableHeaterTemperature_Celsius = 26

enableHumidifierMoistness_Procent = 89
disableHumidifierMoistness_Procent = 95

heater = Energenie(2, initial_value=False) 
humidifier = Energenie(3, initial_value=False)

while True:
    lastReadOn = getHumidityAndTemperature() 
    humidity = lastReadOn[0]
    temperature = lastReadOn[1]

    thingSpeakIoTKey = "8N9BL598BIFY4LV7"
    requests.post('https://api.thingspeak.com/update.json', data = {'api_key':thingSpeakIoTKey, 'field1':temperature, 'field2':humidity})

    if int(humidity) < enableHumidifierMoistness_Procent and not humidifier.is_active:
        humidifier.on()
        print('Humidifier enabled!')

    if int(humidity) > disableHumidifierMoistness_Procent and humidifier.is_active:
        humidifier.off()
        print('Humidifier disabled!')
        

    if temperature < enableHeaterTemperature_Celsius and not heater.is_active:
        heater.on()
        print('Heater enabled!')

    if temperature > disableHeaterTemperature_Celsius and heater.is_active:
        heater.off()
        print('Heater disabled!')

    sleep(10.0)

print ("Execution terminated!")
