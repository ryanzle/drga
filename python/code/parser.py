from datetime import datetime
import os
import mysql.connector as database
#import pymysql

username = os.environ.get("ipl")
password = os.environ.get("ipl2023")
hostname = os.environ.get("localhost")

connection = database.connect(
    #user = username,
    #password = password,
    #host = hostname,
    #database = 'sensor_data',
    
    user = "ipl",
    password = "ipl2023",
    host = "localhost",
    database = 'sensor_data',
)

cursor = connection.cursor()


def parser(string, rssi):
    #values = string.split(" ")
    #print(values)
    
    #print(values[0])
    #print(values[1])
    #print(values[2])
    #print(values[3])
    
    #floats = [float(x) for x in string.split(" ")]
    floats = [(float(x)/10) for x in string]
    print(floats)
    
    temperature = floats[0]
    humidity = floats[1]
    moisture = floats[2]
    light_intensity = floats[3]
    
    print(temperature)
    print(humidity)
    print(moisture)
    print(light_intensity)
    
    print(rssi)
    
    time_stamp = datetime.now()
    
    print(time_stamp)
    
    statement = ("INSERT INTO sensor "
                "(humidity, temperature, moisture, time_stamp, rssi, light_intensity) "
                "VALUES (%s, %s, %s, %s, %s, %s)")
    data = (humidity, temperature, moisture, time_stamp, rssi, light_intensity)
    cursor.execute(statement, data)
    connection.commit()
    print("Successfully added entry to database")
    cursor.close()
    connection.close()
    
    
    
    
