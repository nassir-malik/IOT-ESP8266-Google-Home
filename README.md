# IOT-ESP8266-Google-Home

YouTube tutorial -->https://www.youtube.com/watch?v=Uvg0ruRkKgY

In This project you will beable to control ESP8266 with Google Home without opening a firewall port or setuping a revers proxy.

1. Download this project and unzip.
  
2. Deploy this project to Heroku by clicking this button
    [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
    
3. Copy following folders to "C:\Program Files (x86)\Arduino\libraries", or install the libraries via the Arduino Library manager.

    arduinoWebSockets (WebSockets by Markus Sattler)
  
    ArduinoJson (ArduinoJson by Benolt Blanchon)
    
4. Update and flash your ESP8266 with "ESP8266/WebSocketClient/ESP8266_WebSocketClient/ESP8266_WebSocketClient.ino"

5. Create an API.ai agent and import "matrix-ai.zip"  and setup Google integration and webhook

6. Test and enjoy.


## Troubleshooting

1. Make sure Google Home device is logged in to same account as your API.ai account.

2. If unable to trigger relay power cycle the ESP8266.

3. If you are still unable to trigger the relay then restart Heroku app by selecting option "Restat all dynos" and then power cycle the ESP8266.

3. If you see crash errors in Arduino IDE serial monitor the use a better power supply.

4. Use a saprate power source for relay or use 5volts power source and use 3.3 voltage regulator to power ESP8266 from same power supply.

5. Make sure you enter the correct URL for webhook in API.ai

6. Make sure Google action option is enabled.

7. If it still does not work then go to church and pray to God -:)
