#include <ESP8266WiFi.h>
#include <WebSocketClient.h>
#include <ArduinoJson.h>

// @@@@@@@@@@@@@@@ Modify wi-fi and domain info @@@@@@@@@@@@@@@@@@@@
const char* ssid     = "suddenlink.net-AD42"; //enter your ssid/ wi-fi(case sensitiv) router name - 2.4 Ghz only
const char* password = "G7MBSY89C601814";     // enter ssid password (case sensitiv)
char host[] = "espiot.herokuapp.com"; //enter your Heroku domain name like "espiot.herokuapp.com" 192.168.0.108 
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

char path[] = "/ws"; 
int port = 80;
WebSocketClient webSocketClient;

DynamicJsonBuffer jsonBuffer;
const int relayPin = 16;

// Use WiFiClient class to create TCP connections
WiFiClient client;

void setup() {
  Serial.begin(115200);
  delay(10);
  
  // Setup Relay
  pinMode(relayPin, OUTPUT);
  // We start by connecting to a WiFi network

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  delay(6000);
  
  Serial.println("Trying to reconnect to WebSock");
  winSockConnect();

}


void loop() {
//Serial.println("Loop started");
  String data;

  if (client.connected()) {
    //webSocketClient.sendData("{\"name\":\"OK\"}");
    webSocketClient.getData(data);
          if (data.length() > 0) {
            Serial.print("Received data: ");
            Serial.println(data);
      
            //load request into json
            JsonObject& root = jsonBuffer.parseObject(data);
            String device = root["device"];
            String location = root["location"];
            String state = root["state"];
            String query = root["query"];
            String message;
            if(query!="?"){
            
                    if(state=="on"){
                      digitalWrite(relayPin, HIGH);
                      message = "{\"state\":\"ON\"}";
                    }else{
                      digitalWrite(relayPin, LOW);
                      message = "{\"state\":\"OFF\"}";
                    
                    }
            }else{
              int state = digitalRead(relayPin);
                 if(state==1){
                      message = "{\"state\":\"ON\"}";
                    }else{
                      message = "{\"state\":\"OFF\"}";
                    }
            }
            Serial.println("Sending response back");
            webSocketClient.sendData(message);
            webSocketClient.sendData(message);
            Serial.println("Response send");
          }

  } else {
          Serial.println("Client disconnected.");
          Serial.println("Trying to reconnect to WebSock");
          winSockConnect();
  }
  
  // wait to fully let the client disconnect
  delay(2000);
  //Serial.println("Loop end");
}

void winSockConnect(){
  Serial.print(".");
    // Connect to the websocket server
  if (client.connect(host, port)) {
    Serial.println("Connected");
  } else {
    Serial.println("ws Connection failed.");
  }

  // Handshake with the server
  webSocketClient.path = path;
  webSocketClient.host = host;
  if (webSocketClient.handshake(client)) {
    Serial.println("Handshake successful");
  } else {
    Serial.println("Handshake failed.");
  }
}

