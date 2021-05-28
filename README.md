# sensores
El archivo sensor_0.0.0.zip es para construir el servicio de ArangoDB

El archivo sensores.py corresponde a la api con Sanic

El archivo ultrasonico.ino es el codigo para la NodeMCU Esp8266 con el sensor ultrasonico

El archivo infrarrojo.py refiere al codigo para la Raspberry Pi 3 Modelo B con un módulo Ky-022 Sensor Receptor Infrarrojo

El archivo temperatura_humedad.py refiere al codigo para la Raspberry Pi 3 Modelo B+ con el sensor de humedad y temperatura DHT11

El archivo sensor_mov.ino es el codigo para la NodeMCU Esp8266 con el sensor de movimiento PIR

proyecto2.py es el archivo que se ejecuta en spark para enviar las estadisticas de todos los datos de la api

proyecto3.py se ejecuta en spark para seleccionar un rango de fechas de las cuales se sacan estadísticas 

La api se encuentra en http://165.227.125.50:8001/get
