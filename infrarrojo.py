from gpiozero import LineSensor
from time import sleep
import json
import requests
import datetime

ir = LineSensor(18)

def encendido():
	print(ir.value)
	datet = datetime.datetime.now().replace(tzinfo=datetime.timezone(datetime.timedelta(seconds=-21600))).isoformat()
	archjso = '''"estado": "1", "sensor": "Infrarrojo", "fecha": '''+'"'+ datet +'"'
	print(archjso)
	archjson = "{"+archjso+"}"
	print(archjson)
	ar = json.loads(archjson)
	x=requests.post("http://165.227.125.50:8001/post", json=ar)
	print(x)

def apagado():
	print(ir.value)
	datet = datetime.datetime.now().replace(tzinfo=datetime.timezone(datetime.timedelta(seconds=-21600))).isoformat()
	archjso = '''"estado": "0", "sensor": "Infrarrojo", "fecha": '''+'"'+ str(datet) +'"'
	print(archjso)
	archjson = "{"+archjso+"}"
	print(archjson)
	ar = json.loads(archjson)
	x=requests.post("http://165.227.125.50:8001/post", json=ar)
	print(x)

# main program loop
while True:
	ir.when_line = lambda: encendido()
	sleep(5)
	ir.when_no_line = lambda: apagado()
	sleep(1)

