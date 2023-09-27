
"""
from datetime import datetime
import os
import mysql.connector as database
#import pymysql

connection = database.connect(
    #user = username,
    #password = password,
    #host = hostname,
    #database = 'sensor_data',
    
    #user = "root",
    #password = "sean16",
    #host = "localhost",
    #database = 'sensor_data',
    
    user = "ipl",
    password = "ipl2023",
    host = "localhost",
    database = 'sensor_data',
)

cursor = connection.cursor()


def parser(string, rssi):
    #cursor = connection.cursor()
    
    values = string.split(" ")
    #print(values)
    
    print(values[0])
    print(values[1])
    print(values[2])
    print(values[3])
    
    #floats = [float(x) for x in string.split(" ")]
    #print(floats)
    
    #temperature = floats[0]
    #humidity = floats[1]
    #moisture = floats[2]
    #light_intensity = floats[3]
    
    temperature = values[0]
    humidity = values[1]
    moisture = values[2]
    light_intensity = values[3]
    
    print(temperature)
    print(humidity)
    print(moisture)
    print(light_intensity)
    
    print(rssi)
    
    time_stamp = datetime.now()
    time_stamp = str(time_stamp)
    
    print(time_stamp)
    
    time_stamp = time_stamp.split(" ")
    date = time_stamp[0]
    time = time_stamp[1]
    
    print(date)
    time = time.split(".")
    time = time[0]
    
    print(time)
    
    statement = ("INSERT INTO sensor "
                "(humidity, temperature, moisture, light_intensity, rssi, date, time) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    data = (humidity, temperature, moisture, light_intensity, rssi, date, time)
    cursor.execute(statement, data)
    connection.commit()
    print("Successfully added entry to database")
    cursor.close()
    connection.close()
    

#parser("43.00 61.00 6.00 2.0", 98)
"""

from datetime import date
import os
import mysql.connector as database
import time

def parser(string, rssi):
    con = database.connect( 
    user = "ipl",
    password = "ipl2023",
    host = "localhost",
    database = 'sensor_data',
    )
    cur = con.cursor()
#def parser(string, rssi, cur, connection):
    #splits incoming 
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
    
    today = date.today()
    
    print(today)
    
    t = time.localtime() 
    current_time = time.strftime("%H:%M:%S", t)
    
    print(current_time)
    
    
    statement = ("INSERT INTO sensor "
               "(humidity, temperature, moisture, rssi, light_intensity, time, date) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    data = (humidity, temperature, moisture, rssi, light_intensity, current_time, today)
    cur.execute(statement, data)
    #cur.execute(statement, data)
    con.commit()
    print("Successfully added entry to database")
    cur.close()
    #cur.close()
    con.close()
        
