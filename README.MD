# DOMINICAN REPUBLIC GREENHOUSE AUTOMATION
## MARK CASTILLO, RYAN LE, ERIK MITCHELL

### GENERAL INFO
The Dominican Republic's Instituto Politécnico Loyola (IPL) needs a wirelessly connected network of sensors for their greenhouses. Our project uses long-range (LoRa) communication to receive data from sensors within the greenhouse on the recorded temperature, humidity, soil moisture, and light values; stores and organizes these measurements in a database and backup text file; and displays appropriate recordings on an interactive application. Aside from basic data senders used solely for testing purposes, our final design serves as a central hub remotely accessible from outside the greenhouse: a main device (in our case, a Raspberry Pi) serving as processing functionality receives information sent over LoRa, logs it to an internal database, and imports it into an HTML application displayed on an attached touchscreen tablet. While designed with specifically IPL’s greenhouses in mind, our system serves as a framework for expansion outside of IPL and eventually to remote farmlands in the global south. Our architecture was designed to use frugal materials for our project to be practically implemented.

### HARDWARE DISCUSSION
The software in this repository was designed as a part of a complete solution where it was tested using specific hardware. Although this solution can be used with other hardware, further testing and potential modification of the code may be needed if different components are used. Descriptions of the software outlined below will assume the architecture and hardware implemented in this specific project. More information on this and other parts of this system can be found in the thesis.

### SENIOR THESIS
Our published thesis can be found for free on the [SCU scholar commons site](https://scholarcommons.scu.edu/cseng_senior/253/).

### DATABASE SETUP
The database was constructed locally on the pi through the use of MariaDB. Instructions for how to install and set up the server can be found [here](https://mariadb.org/download/?t=mariadb&p=mariadb&r=11.3.0).

Create the database: 
```
	CREATE DATABASE name
```
Navigate to database:
```
	USE name
```
Then create the table in the following format:
```
	CREATE TABLE sensor (
		data_id 	INTEGER NOT NULL AUTO_INCREMENT,
		humidity	DECIMAL(3,1),
		temperature	DECIMAL(3,1),
		moisture	DECIMAL(3,1),
		light_intensity	DECIMAL(3,1),
		rssi 		INTEGER,
		date 		DATE,
		time		TIME,
		PRIMARY KEY(data_id));
```
Here, Sensor is made up of 8 columns, 5 of which hold the data that is collected from the sensors. The remaining 3 columns were made for tracking and monitoring purposes. Data and Time are unambiguous, and are recorded at the time the entry is being inserted into the database, and is assigned a data ID in order to uniquely identify the entry. 


### DIRECTORIES
This repository is split into three directories. The `app` directory includes all the files for the HTML application, including the Python scripts that retrieve information from the database for external display. The `python` directory includes the Python scripts for LoRa communication (`lora_gateway.py`) and entering data into the MySQL database (`parser.py`). Finally, the `sensor` directory includes Arduino code for a simple node to send example test data.

#### APP
This directory contains the HTML and CSS that make up the application’s visuals, using the logo and colors provided by the client. The text is hard-coded in Spanish and thus does not yet have a multi-language features; however, there are enough cognates and graphics for people who cannot speak Spanish to understand.

##### SCRIPTS
Most of the code in this folder is JavaScript, with only one written in Python (`get_data.py`). The Python code is located here so that the application has easy access to its outputs: the data to be displayed on the webpage.

`get_data.py` - This program is our main method of extracting the data from the database. All of the functions follow the same procedure but they are modified to extract data over different areas of time (more down below). The main function is recent_data(), which grabs the most recent entry in the database. 

```
    sql = '''SELECT *
                FROM sensor
                WHERE time = (SELECT max(time)
                                    FROM sensor) AND
                      date = (SELECT max(date)
                                    FROM sensor)'''

    cursor.execute(sql)

    data_result = cursor.fetchone()
```
We make use of SQL functions such as the SELECT statement. The order here matters because we are ensuring that we are grabbing the latest entry through the max time on the max day. In our hour_[variable]() functions we use the following: 
```
   ​​today = date.today()
    
    sql = '''SELECT hour(time), AVG(humidity)
                FROM sensor
                WHERE date = %s
                GROUP BY hour(time)'''
    cursor.execute(sql, [today])

    hourly_result = cursor.fetchall()    
```
In the same way, we use date, we then further this in our ``` week_[variable]()``` functions by using this to subtract 7 days prior to the date as such: 
```
today = date.today()
    week_ago = (today - timedelta(days=7))
    
    sql = '''SELECT day(date), AVG(humidity)
                FROM sensor
                WHERE date >= %s
                GROUP BY day(date)'''
    cursor.execute(sql, [week_ago])
    weekly_result = cursor.fetchall()  

```

Here we take advantage of built in libraries to be able to determine the date. We then use the SQL statement to calculate the AVG of whatever stat we are looking at. And then execute the statement based on the date recorded.

```
    f = open("data.js", "w")
    f.write("export const\n")
    f.write("data = { \n")
```
These procedures are consistent throughout all functions in the file. Through these statements, we are able to create a file on the first execution of the program, and later continuously update the file with the new desired data for a specific time frame. In the last two lines, we are beginning to format the file appropriately.

```
    (id, hum, temp, moist, light, signal, time, date) = data_result
```
This statement unpackages the results from the SQL query formatted as a tuple into individual variables that contain their respective data. They are then converted to strings in the following way: 
```
    hum = str(hum)
    temp = str(temp)
    moist = str(moist)
    time = str(time)
    date = str(date)
    light = str(light)
```
They are then packaged into a dictionary format

```
    y = {
        "data_id": id,
        "humidity": hum,
        "temperature": temp,
        "moisture": moist,
        "light_intensity": light, 
        "rssi": signal,
        "date": date,      
        "time": time,
    }
```

The Week/Hour functions differentiate from get data because we are grabbing data over the course of time. We want to make sure all the data is being formatted, so a for statement is being used to make sure that as long as we still have data in the queue, that we continue to record it and label it with the correct way so that the files can be read.

hour_[variable]()
```
    for x in hourly_result:
        num = str(i)
        (hour, light) = x
        time = str(hour)
        light_intensity = str(light)
        y = {
            "x": time,
            "y": light_intensity
        }
        f = open("hour_light.js", "a")
        f.write('t')
        f.write(num)
        f.write(': ')
        f.close()
        with open("hour_light.js", "a") as outfile:
            json.dump(y, outfile, indent=2)
        
        f = open("hour_light.js", "a")
        f.write(",\n")
        f.close()
        i+=1  
```
In the hour functions, we are recording the hour we are assigning the avg to and are doing a similar procedure in the ```week_[variable]()```
```
for x in weekly_result:
        num = str(i)
        (day, hum) = x
        day = str(day)
        humidity = str(hum)
        y = {
            "x": day,
            "y": humidity
        }
        f = open("week_hum.js", "a")
        f.write('d')
        f.write(num)
        f.write(': ')
        f.close()
        with open("week_hum.js", "a") as outfile:
            json.dump(y, outfile, indent=2)
        f = open("week_hum.js", "a")
        f.write(",\n")
        f.close()
        i+=1    

```

`data.js` - One of the outputs of the `get_data.py` file. It is formatted as a JSON but is a .js file rather than a .json file in order to integrate more effectively with the rest of the application. The file currently contains a single set of example values hypothetically measured at a single moment. This is the data propagating the home page of the application.

`hour_hum.js`, `hour_light.js`, hour_moist.js`, `hour_temp.js` - One of the outputs of the `get_data.py` file. They are formatted as JSON but are .js files rather than .json files in order to integrate more effectively with the rest of the application. These files currently contain 24 points of example data for each measurement hypothetically taken over the past 24 hours. This is the data propagating the hourly graph viewable by clicking on each of the sensors’ measured values on the home page.

`weekly_hum.js`, `weekly_light.js`, `weekly_moist.js`, `weekly_temp.js` - One of the outputs of the `get_data.py` file. They are formatted as JSON but are .js files rather than .json files in order to integrate more effectively with the rest of the application. These files currently contain 7 points of example data for each measurement as hypothetical average temperatures over the past 7 days. This is the data propagating the weekly graph viewable by clicking on each of the sensors’ measured values on the home page.

`data_display.js` - A JavaScript file that displays the contents of `data.js` on the homescreen. It uses the module function `import` to use the `data.js` file, creates an array out of the JSON, and changes the HTML’s inner text to its respective value.

`graph.js` - A JavaScript file that displays the contents of each `hour.js` file in a graph on their respective subpages. It utilizes the module function `import` to use the JSON data, then uses ChartJS to create a scatterplot.

`graph_week.js` - A JavaScript file that displays the contents of each `weekly.js` file in a graph on their respective subpages. It utilizes the module function `import` to use the JSON data, then uses ChartJS to create a scatterplot.


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
