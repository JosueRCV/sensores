//------------------------LIBRERIAS--------------------------------------------------------------------
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <HCSR04.h>
#include <ezTime.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
//------------------------DATOS--------------------------------------------------------------------
int Waiting_Time = 500;                  
int b1;
int b2;
String post = "http://165.227.125.50:8001/post";// Enlace a la API
HCSR04 hc(5,4);//initialisation class HCSR04 (trig pin , echo pin)

//----------------------CONEXION WIFI-------------------------------------------------

const char* ssid = "ARRIS-F782";
const char* password = "C85D6D6196489379";

//-------GLOBALES-------------------

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");
unsigned long epochTime;

unsigned long getTime() {
  timeClient.update();
  unsigned long now = timeClient.getEpochTime();
  return now;
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  timeClient.begin();
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void ezt::setTime(time_t);

void loop() {
  Serial.print("Lectura de datos");
  Serial.println();
  String estado = String(hc.dist(),2);
  Serial.println(estado);
  String sensor = "Ultrasonico";
  time_t is8 = getTime();
  setTime(is8);
  Timezone myTZ;
  myTZ.setLocation(F("America/Mexico_City"));
  String iso8 = myTZ.dateTime(ISO8601);
  postinterruptor(estado, sensor, iso8);
  delay(10000);
}


void postinterruptor(String estado, String sensor, String tiempo) {
  HTTPClient http;
  String json;
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& root = jsonBuffer.createObject();
  Serial.println(estado);
  Serial.println(sensor);
  Serial.println(tiempo);
  root["estado"] = estado;
  root["sensor"] = sensor;
  root["fecha"] = tiempo;
  /* Ejemplo si quieres más atributos
  root["sensor"] = "gps";
  root["time"] = 1351824120;*/
  root.printTo(json);
  
  Serial.println(""); // salto de linea para http.writeToStream(&Serial);
  
  http.begin(post); //URL del microservicio
  http.addHeader("Content-Type", "application/json");
  http.POST(json); 
  http.writeToStream(&Serial);
  http.end();

  //delay(1000);
}
