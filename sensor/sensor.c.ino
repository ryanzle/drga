//#include <SPI.h>
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
