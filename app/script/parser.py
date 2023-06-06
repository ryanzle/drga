from datetime import datetime
import os
import mysql.connector as database
#import pymysql

connection = database.connect(
    #user = username,
    #password = password,
    #host = hostname,
    #database = 'sensor_data',
    
    user = "root",
    password = "sean16",
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
    
    floats = [float(x) for x in string.split(" ")]
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
                "(humidity, temperature, moisture, light_intensity, rssi, time_stamp) "
                "VALUES (%s, %s, %s, %s, %s, %s)")
    data = (humidity, temperature, moisture, light_intensity, rssi, time_stamp)
    cursor.execute(statement, data)
    connection.commit()
    print("Successfully added entry to database")
    cursor.close()
    connection.close()

parser("43.00 61.00 6.00 2.0", 98)