/* Adapted for face2pi from:
 * ESP8266 (Adafruit HUZZAH) Mosquitto MQTT Publish Example
 * Thomas Varnish (https://github.com/tvarnish), (https://www.instructables.com/member/Tango172)
 * Made as part of my MQTT Instructable - "How to use MQTT with the Raspberry Pi and ESP8266"
 */
#include <ESP8266WiFi.h> // Enables the ESP8266 to connect to the local network (via WiFi)
#include <PubSubClient.h> // Allows us to connect to, and publish to the MQTT broker

//const int ledPin = 0; // This code uses the built-in led for visual feedback that the button has been pressed
//const int buttonPin = 13; // Connect your button to pin #13

// WiFi
// Make sure to update this for your own WiFi network!
const char* ssid = "INCONSPICUOUS SURVEILLANCE VAN";
const char* wifi_password = "guestGUEST!";

// MQTT
// Make sure to update this for your own MQTT Broker!
const char* mqtt_server = "192.168.0.99";
const char* mqtt_topic = "outTopic";
// The client id identifies the ESP8266 device. Think of it a bit like a hostname (Or just a name, like Greg).
const char* clientID = "esp";

// Initialise the WiFi and MQTT Client objects
WiFiClient wifiClient;
PubSubClient client(mqtt_server, 1883, wifiClient); // 1883 is the listener port for the Broker

void setup() {
  Serial.begin(9600);
  pinMode(D2,INPUT);
  digitalWrite(D2,LOW);

  Serial.print("Connecting to ");
  Serial.println(ssid);

  // Connect to the WiFi
  WiFi.begin(ssid, wifi_password);

  // Wait until the connection has been confirmed before continuing
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  // Debugging - Output the IP Address of the ESP8266
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Connect to MQTT Broker
  // client.connect returns a boolean value to let us know if the connection was successful.
  if (client.connect(clientID)) {
    Serial.println("Connected to MQTT Broker!");
  }
  else {
    Serial.println("Connection to MQTT Broker failed...");
  }
  
}

int quadruplecheck(){
    delay(250);
     if(digitalRead(D2)==HIGH)  
    {
      Serial.println("SHIT"); //movement - sel=0
      return 0;
    }
    else  
    {
      Serial.println("FUCK"); //no movement - sel=1
      return 1;
    }
}

void loop() {
    //delay(1000); //check every 1 seconds
    
    char SHIT[5] = {'S','H','I','T'};
    char FUCK[5] = {'F','U','C','K'};
    char *msg;
    bool sel;
    int check[4];
    for (int i = 0; i < 4; i++){
      check[i] = quadruplecheck();
    }
    if (check[0] + check[1] + check[2] + check[3] == 0 || check[0] + check[1] + check[2] + check[3] == 4){
      sel = check[0];
      if (!sel)
        msg = SHIT;
      else
        msg = FUCK;
    }
    else
        msg = FUCK; //default no movement if quadcheck fails
    
    // PUBLISH to the MQTT Broker (topic = mqtt_topic, defined at the beginning)
    // Here, "Button pressed!" is the Payload, but this could be changed to a sensor reading, for example.
    if (client.publish(mqtt_topic, msg)) {
      Serial.println("message sent!");
    }
    // Again, client.publish will return a boolean value depending on whether it succeded or not.
    // If the message failed to send, we will try again, as the connection may have broken.
    else {
      Serial.println("Message failed to send. Reconnecting to MQTT Broker and trying again");
      client.connect(clientID);
      delay(10); // This delay ensures that client.publish doesn't clash with the client.connect call
      //client.publish(mqtt_topic, "Button pressed!");
    }  
}
