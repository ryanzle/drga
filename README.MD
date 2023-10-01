Dominican Republic Greenhouse Automation
SCU Senior Design Project
Mark Castillo, Ryan Le, Erik Mitchell

#### PYTHON

##### CODE

###### lora_gateway.py

```
from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD

from parser import *

BOARD.setup()
```

We used 2 libraries to code the receiver LoRa protocol in Python. The time library allows the use of the sleep method. The SX127x library allows for the use of the LoRaRcvCont class which configures the LoRa chip to receive LoRa connections. We also import methods from the file parser.py and set the board GPIO (of the Raspberry Pi). More information about the time and SX127x libraries can be found here: 
https://docs.python.org/3/library/time.html
https://github.com/mayeranalytics/pySX127x

```
class LoRaRcvCont(LoRa):
    def __init__(self, verbose = False):
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        #self.set_dio_mapping([1,0,0,0,0,0])
```

The LoRa class is subclassed and the three functions __init__, start, and on_rx_done are overridden for the behavior of the specific implementation. __init__ sets up the proper registers, puts the chip into sleep mode, and maps the proper board pins (of the LoRa chip).

```
    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            sleep(.5)
            rssi_value = self.get_rssi_value()
            status = self.get_modem_status()
            sys.stdout.write("\r%d %d %d" % (rssi_value, status['rx_ongoing'], status['modem_clear']))
            #sys.stdout.write("\n")
            sys.stdout.write("Waiting for inputs...")
            sys.stdout.flush()
```

The start() method sets the board to receive signals and waits to receive a value from the sender device.

```
def on_rx_done(self):
        print("\nReceived: ")
        self.clear_irq_flags(RxDone = 1)
        payload = self.read_payload(nocheck = True)
        #data = ''.join([chr(c) for c in payload])
        #print(data)
        #string = bytes(payload).decode("utf-8",'ignore')
        #print(string)
        print(payload)
        string = payload
        #print(bytes(payload).decode("utf-8",'ignore'))
        
        print("\nSending Payload to Parser:")
        rssi_value = self.get_rssi_value()
        parser(string, rssi_value);
        
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
```

The on_rx_done() method specifies the protocol behavior when data is received on the chip. The data is read into the payload which is then sent into the parser function. The parser function is written in the parser.py file. After the payload contents are sent to parser(), the LoRa chip is then set to receive again.

```
lora = LoRaRcvCont(verbose = False)
lora.set_mode(MODE.STDBY)
#initializing lora to 434.0 MHz, Bw = 125kHz
lora.set_pa_config(pa_select = 1)
```

Outside of the subclass definition, the LoRa chip is set to receive data and initialized to the proper frequency.

```
try:
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("")
    sys.stderr.write("Keyboard Interrupt\n")
finally:
    sys.stdout.flush()
    print("")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
```

The overall LoRa protocol attempts to start() in order to begin waiting for inputs. If there is a manual interrupt, a message is written. After the start() method is finished, the resources on the board are then freed.

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
