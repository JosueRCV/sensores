import Adafruit_DHT
import time
import requests
import json
from datetime import date
from datetime import datetime

sensor = Adafruit_DHT.DHT11
pin = 23

DEVICE_LABEL = "raspberry"  # Put your device label here 
VARIABLE_LABEL_1 = "temperatura"  # Put your first variable label here
VARIABLE_LABEL_2 = "humedad"  # Put your second variable label here

def build_payload(variable_1, variable_2):
    # Creates two random values for sending data
    sensor = Adafruit_DHT.DHT11
    pin = 23
    humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin)
    if humedad is not None and temperatura is not None:
         print(f'Temperatura={temperatura:.2f}*C  Humedad={humedad:.2f}%')
         print ("Temperatura = {}".format(temperatura))
         print ("Humedad =  {}".format(humedad))

    else:
        print('Fallo la lectura del sensor.Intentar de nuevo')
        
    now = datetime.now()
    print(now)
    now=str(now)
    value_1 = temperatura
    value_2 = humedad
    value_1=str(value_1)
    value_2=str(value_2)
    print(value_1)
    payload = {"estado": value_1,"sensor": "Temperatura", "fecha": now}
    r = requests.post('http://165.227.125.50:8001/post', data =json.dumps(payload))
    print(r.text)
    payload2 = {"estado": value_2,"sensor": "Humedad", "fecha": now}
    r = requests.post('http://165.227.125.50:8001/post', data =json.dumps(payload2))
    print(r.text)
    
    
    
   


    time.sleep(5)
   
while True:
    build_payload(VARIABLE_LABEL_1, VARIABLE_LABEL_2)
