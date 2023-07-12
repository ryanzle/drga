import json
import decimal
from datetime import date
from datetime import timedelta
import os
import mysql.connector as database

connection = database.connect( 
    user = "root",
    password = "sean16",
    host = "localhost",
    database = 'sensor_data',
)

cursor = connection.cursor()

def recent_data():
    sql = '''SELECT *
                FROM sensor
                WHERE time = (SELECT max(time)
                                    FROM sensor) AND
                      date = (SELECT max(date)
                                    FROM sensor)'''

    cursor.execute(sql)

    data_result = cursor.fetchone()
    (id, hum, temp, moist, light, signal, date, time) = data_result

    hum = str(hum)
    temp = str(temp)
    moist = str(moist)
    time = str(time)
    date = str(date)
    light = str(light)
    x = {
        "data_id": id,
        "humidity": hum,
        "temperature": temp,
        "moisture": moist,
        "rssi": signal,
        "light_intensity": light, 
        "date": date,      
        "time": time,
    }
    f = open('data.js', 'w')
    f.write('export default\n')
    f.close()
    
    with open("data.js", "a") as outfile:     
        json.dump(x, outfile, indent=2)
    print("Json File Created Successfully")    


def hourly_hum():
    today = date.today()
    
    sql = '''SELECT hour(time), humidity
                FROM sensor
                WHERE date = %s
                GROUP BY hour(time)'''
    cursor.execute(sql, [today])

    hourly_result = cursor.fetchall()    
    f = open("hour_hum.js", "w")
    f.write('export const\n')
    f.write("hum = { \n")
    f.close
    i = 0
    for x in hourly_result:
        num = str(i)
        (hour, hum) = x
        time = str(hour)
        humidity = str(hum)
        y = {
            "x": time,
            "y": humidity
        }
        f = open("hour_hum.js", "a")
        f.write('t')
        f.write(num)
        f.write(': ')
        f.close()
        with open("hour_hum.js", "a") as outfile:
            json.dump(y, outfile, indent=2)
        
        f = open("hour_hum.js", "a")
        f.write(",\n")
        f.close()
        i+=1    
    f = open("hour_hum.js", "a")
    f.write('}')
    f.close

def hourly_temp():
    today = date.today()
    
    sql = '''SELECT hour(time), temperature
                FROM sensor
                WHERE date = %s
                GROUP BY hour(time)'''
    cursor.execute(sql, [today])

    hourly_result = cursor.fetchall()    
    f = open("hour_temp.js", "w")
    f.write('export const\n')
    f.write("temp = { \n")
    f.close
    i = 0
    for x in hourly_result:
        num = str(i)
        (hour, temp) = x
        time = str(hour)
        temperature = str(temp)
        y = {
            "x": time,
            "y": temperature
        }
        f = open("hour_temp.js", "a")
        f.write('t')
        f.write(num)
        f.write(': ')
        f.close()
        with open("hour_temp.js", "a") as outfile:
            json.dump(y, outfile, indent=2)
        
        f = open("hour_temp.js", "a")
        f.write(",\n")
        f.close()
        i+=1    
    f = open("hour_temp.js", "a")
    f.write('}')
    f.close
    
def hourly_moist():
    today = date.today()
    
    sql = '''SELECT hour(time), moisture
                FROM sensor
                WHERE date = %s
                GROUP BY hour(time)'''
    cursor.execute(sql, [today])

    hourly_result = cursor.fetchall()    
    f = open("hour_moist.js", "w")
    f.write('export const\n')
    f.write("moist = { \n")
    f.close
    i =0
    for x in hourly_result:
        num = str(i)
        (hour, moist) = x
        time = str(hour)
        moisture = str(moist)
        y = {
            "x": time,
            "y": moisture
        }
        f = open("hour_moist.js", "a")
        f.write('t')
        f.write(num)
        f.write(': ')
        f.close()
        with open("hour_moist.js", "a") as outfile:
            json.dump(y, outfile, indent=2)
        
        f = open("hour_moist.js", "a")
        f.write(",\n")
        f.close()
        i+=1    
    f = open("hour_moist.js", "a")
    f.write('}')
    f.close
    
    
def hourly_light():
    today = date.today()
    
    sql = '''SELECT hour(time), light_intensity
                FROM sensor
                WHERE date = %s
                GROUP BY hour(time)'''
    cursor.execute(sql, [today])

    hourly_result = cursor.fetchall()    
    f = open("hour_light.js", "w")
    f.write('export const\n')
    f.write("light = { \n")
    f.close
    i = 0
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
    f = open("hour_light.js", "a")
    f.write('}')
    f.close
    
def weekly_hum():
    today = date.today()
    week_ago = (today - timedelta(days=7))
    
    sql = '''SELECT day(date), AVG(humidity)
                FROM sensor
                WHERE date >= %s
                GROUP BY day(date)'''
    cursor.execute(sql, [week_ago])
    weekly_result = cursor.fetchall()  
    f = open("week_hum.js", "w")
    f.write('export const\n')
    f.write("hum = { \n")
    f.close
    i = 0
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
    f = open("week_hum.js", "a")
    f.write('}')
    f.close  

def weekly_temp():
    today = date.today()
    week_ago = (today - timedelta(days=7))
    
    sql = '''SELECT day(date), AVG(temperature)
                FROM sensor
                WHERE date >= %s
                GROUP BY day(date)'''
    cursor.execute(sql, [week_ago])
    weekly_result = cursor.fetchall()  
    f = open("week_temp.js", "w")
    f.write('export const\n')
    f.write("temp = { \n")
    f.close
    i =0
    for x in weekly_result:
        num = str(i)
        (day, temp) = x
        day = str(day)
        temperature = str(temp)
        y = {
            "x": day,
            "y": temperature
        }
        f = open("week_temp.js", "a")
        f.write('d')
        f.write(num)
        f.write(': ')
        f.close()
        with open("week_temp.js", "a") as outfile:
            json.dump(y, outfile, indent=2)
        
        f = open("week_temp.js", "a")
        f.write(",\n")
        f.close()
        i+=1    
    f = open("week_temp.js", "a")
    f.write('}')
    f.close  

def weekly_moist():
    today = date.today()
    week_ago = (today - timedelta(days=7))
    
    sql = '''SELECT day(date), AVG(moisture)
                FROM sensor
                WHERE date >= %s
                GROUP BY day(date)'''
    cursor.execute(sql, [week_ago])
    weekly_result = cursor.fetchall()  
    f = open("week_moist.js", "w")
    f.write('export const\n')
    f.write("moist = { \n")
    f.close
    i = 0
    for x in weekly_result:
        num = str(i)
        (day, moist) = x
        day = str(day)
        moisture = str(moist)
        y = {
            "x": day,
            "y": moisture
        }
        f = open("week_moist.js", "a")
        f.write('d')
        f.write(num)
        f.write(': ')
        f.close()
        with open("week_moist.js", "a") as outfile:
            json.dump(y, outfile, indent=2)
        
        f = open("week_moist.js", "a")
        f.write(",\n")
        f.close()
        i+=1    
    f = open("week_moist.js", "a")
    f.write('}')
    f.close  

    
def weekly_light():
    today = date.today()
    week_ago = (today - timedelta(days=7))
    
    sql = '''SELECT day(date), AVG(light_intensity)
                FROM sensor
                WHERE date >= %s
                GROUP BY day(date)'''
    cursor.execute(sql, [week_ago])
    weekly_result = cursor.fetchall()  
    f = open("week_light.js", "w")
    f.write('export const\n')
    f.write("light = { \n")
    f.close
    i = 0
    for x in weekly_result:
        num = str(i)
        (day, light) = x
        day = str(day)
        light_intensity = str(light)
        y = {
            "x": day,
            "y": light_intensity
        }
        f = open("week_light.js", "a")
        f.write('d')
        f.write(num)
        f.write(': ')
        f.close()
        with open("week_light.js", "a") as outfile:
            json.dump(y, outfile, indent=2)
        f = open("week_light.js", "a")
        f.write(",\n")
        f.close()
        i+=1    
    f = open("week_light.js", "a")
    f.write('}')
    f.close  
  
    
recent_data()
#hourly_temp()
#hourly_hum()
#hourly_moist()
#hourly_light()
#weekly_temp()
#weekly_hum()
#weekly_moist()
#weekly_light()