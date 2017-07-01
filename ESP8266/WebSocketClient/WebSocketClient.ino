#include <ESP8266WiFi.h>
#include <WebSocketClient.h>


const char* ssid     = "suddenlink.net-AD42";
const char* password = "G7MBSY89C601814";
char path[] = "/ws";
char host[] = "192.168.0.108";
  
WebSocketClient webSocketClient;

// Use WiFiClient class to create TCP connections
WiFiClient client;

void setup() {
  //while( (waitKey = getKey()) == NO_KEY ) yield();
  Serial.begin(115200);
  delay(10);

  // We start by connecting to a WiFi network

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  //ESP.wdtDisable();
//ESP.wdtEnable(WDTO_8S);
//WiFi.persistent(false);
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
  

  // Connect to the websocket server
  if (client.connect("192.168.0.108", 80)) {
    Serial.println("Connected");
  } else {
    Serial.println("ws Connection failed.");
    while(1) {
      // Hang on failure
    }
  }

  // Handshake with the server
  webSocketClient.path = path;
  webSocketClient.host = host;
  if (webSocketClient.handshake(client)) {
    Serial.println("Handshake successful");
  } else {
    Serial.println("Handshake failed.");
    while(1) {
      // Hang on failure
      delay(1);
    }  
  }

}


void loop() {

  String data;
  //ESP.wdtFeed();
  /*if(WiFi.status() != WL_CONNECTED){
    WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }}*/
  if (client.connected()) {
    //webSocketClient.sendData("{\"name\":\"OK\"}");
    webSocketClient.getData(data);
    if (data.length() > 0) {
      Serial.print("Received data: ");
      Serial.println(data);
      webSocketClient.sendData("{\"name\":\"OK\"}");
      webSocketClient.sendData("{\"name\":\"OK\"}");
    }
    
    // capture the value of analog 1, send it along
   // pinMode(1, INPUT);
    //data = String(analogRead(1));
    
    //webSocketClient.sendData("1");
    
  } else {
    Serial.println("Client disconnected.");
    while (1) {
      delay(1);
      // Hang on disconnect.
    }
  }
  
  // wait to fully let the client disconnect
  delay(2000);
  //Serial.println("Loop end");
}
