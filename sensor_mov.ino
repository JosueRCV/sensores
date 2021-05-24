


//------------------------LIBRERIAS--------------------------------------------------------------------
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ESP8266HTTPClient.h>
#include <ezTime.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

//------------------------DATOS--------------------------------------------------------------------
#define PIR_Sensor D0 // PIR sensor 
int Waiting_Time = 5000;                  
const int LED = 2; //GPIO 2 corresponde al LED integrado de las placas NodeMCU - Wemos D1  
String post = "http://165.227.125.50:8001/post";// Enlace a la API



//----------------------CONEXION WIFI-------------------------------------------------

const char* ssid = "INFINITUM5422_2.4";
const char* password = "JnAT0RKGBu";

//-------GLOBALES-------------------

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
String fecha="";

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");
unsigned long epochTime;

unsigned long getTime() {
  timeClient.update();
  unsigned long now = timeClient.getEpochTime();
  return now;
}

//-------------------------------------------FUNCIONES---------------------------------------------------------------------------------------------------------

void setup() {
  pinMode(PIR_Sensor, INPUT); // SENSOR
  pinMode(LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  digitalWrite(LED, HIGH); 
  Serial.begin(115200);
  setup_wifi();
  timeClient.begin();

}
void ezt::setTime(time_t);


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



void loop() {
  time_t is8 = getTime();
  setTime(is8);
  Timezone myTZ;
  myTZ.setLocation(F("America/Mexico_City"));
  String iso8 = myTZ.dateTime(ISO8601);
  int state = digitalRead(PIR_Sensor);    // Continuously check the state of PIR sensor
  delay(10000);                             // Check state of PIR after every half second
    if(state == HIGH){                
      digitalWrite (LED, LOW);    // Enciende  el led
      delay(150);
      Serial.print("DETECTO MOVIMIENTO...");
      Serial.println();
      String estado = "1";
      String sensor = "Movimiento";
      estado.toCharArray(msg,50);
      postmov(estado, sensor, iso8);
      delay(1000);                
                  
    }
    else {
      digitalWrite (LED, HIGH);      // Apaga el led
      Serial.print("NO DETECTO MOVIMIENTO...");
      Serial.println();
      String estado = "0";
      String sensor = "Movimiento";
      estado.toCharArray(msg,50);
      postmov(estado, sensor, iso8);
      delay(1000);  
      
   }
  
 

 
}






//---------------------------------------------POST----------------------------------------------------------------------


void postmov(String estado, String sensor, String tiempo) {
  HTTPClient http;

  String json;
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& root = jsonBuffer.createObject();
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
