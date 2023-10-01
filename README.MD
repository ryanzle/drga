Dominican Republic Greenhouse Automation
SCU Senior Design Project
Mark Castillo, Ryan Le, Erik Mitchell


###### parser.py

##### pySX127x
This folder is a fork of the Python LoRa library that we used to enable LoRa communication on the Raspberry Pi. Since our group was more comfortable coding with Python, and to keep consistency with the other Python code on the Raspberry Pi, we used this library to write the file lora_gateway.py (see the 2nd and 3rd lines). The fork also contains other examples of ways to use the library which could be informative to following projects.

#### SENSOR

##### sensor.c.ino

```
#include <LoRa.h>
int counter = 0;
void setup() {
 Serial.begin(9600);
 while (!Serial);
 Serial.println("LoRa Sender");
 if (!LoRa.begin(434E6)) {
   Serial.println("Starting LoRa failed!");
   while (1);
 }
 LoRa.setSyncWord(0xF3);
 LoRa.setTxPower(20);
}
```



The library that we used to program the sender LoRa protocol in C was the LoRa library supported by Arduino: https://www.arduino.cc/reference/en/libraries/lora/. The library supports SX1276/77/78/79-based boards. In the setup() method, the library is initialized to the frequency 434 MHz, the radio frequency permitted for communications in the Dominican Republic. The sync word and power of the board are set to start communication.


```
void loop()
{
 Serial.print("Sending packet: ");
 Serial.print(counter);
 Serial.println();
 randomSeed(analogRead(0));
 float temperature = random(40, 80);
 float humidity = random(0, 100);
 float moisture = random(0, 100);
 int light = random(0, 7);
 Serial.print(temperature);
 Serial.print(" ");
 Serial.print(humidity);
 Serial.print(" ");
 Serial.print(moisture);
 Serial.print(" ");
 Serial.print(light);
 // send packet
 LoRa.beginPacket();
 LoRa.print(temperature);
 LoRa.print(" ");
 LoRa.print(humidity);
 LoRa.print(" ");
 LoRa.print(moisture);
 LoRa.print(" ");
 LoRa.print(light);
 LoRa.endPacket();
 counter++;
 Serial.println();
 delay(5000);
}
```

After the setup is done, the sensor repeatedly sends packets of data to the gateway. For testing purposes, the data is randomized and labeled. It is then packed and sent in a packet by the methods beginPacket() and endPacket().
