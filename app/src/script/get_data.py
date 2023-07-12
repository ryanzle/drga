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

def optimize():
    today = date.today()
    week_ago = (today - timedelta(days=7))
    sql = '''SELECT day(date)
                FROM sensor
                GROUP BY day(date)'''
    cursor.execute(sql)
    result = cursor.fetchall()
    if(len(result) > 7):
        sql = '''DELETE FROM sensor WHERE date < %s'''
        cursor.execute(sql, [week_ago])
        connection.commit();
    print("Done")
    
optimize()

def recent_data():
    sql = '''SELECT *
                FROM sensor
                WHERE time = (SELECT max(time)
                                    FROM sensor) AND
                      date = (SELECT max(date)
                                    FROM sensor)'''

    cursor.execute(sql)

    data_result = cursor.fetchone()
    backup_data()
    f = open("data.js", "w")
    f.write("export const\n")
    f.write("data = { \n")
    f.close
    (id, hum, temp, moist, light, signal, time, date) = data_result
    hum = str(hum)
    temp = str(temp)
    moist = str(moist)
    time = str(time)
    date = str(date)
    light = str(light)
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
    f = open("data.js", "a")
    f.write('recent:')
    f.close()
    with open("data.js", "a") as outfile:
        json.dump(y, outfile, indent=2)
        
    f = open("data.js" , 'a')
    f.write("\n}")
    f.close()   


def hour_hum():
    today = date.today()
    
    sql = '''SELECT hour(time), AVG(humidity)
                FROM sensor
                WHERE date = %s
                GROUP BY hour(time)'''
    cursor.execute(sql, [today])

    hourly_result = cursor.fetchall()    
    f = open("hour_hum.js", "w")
    f.write("export const\n")
    f.write("humidity = { \n")
    f.close
    i =0
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

def hour_temp():
    today = date.today()
    
    sql = '''SELECT hour(time), AVG(temperature)
                FROM sensor
                WHERE date = %s
                GROUP BY hour(time)'''
    cursor.execute(sql, [today])

    hourly_result = cursor.fetchall()    
    f = open("hour_temp.js", "w")
    f.write("export const\n")
    f.write("temperature = { \n")
    f.close
    i =0
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
    
def hour_moist():
    today = date.today()
    
    sql = '''SELECT hour(time), AVG(moisture)
                FROM sensor
                WHERE date = %s
                GROUP BY hour(time)'''
    cursor.execute(sql, [today])

    hourly_result = cursor.fetchall()    
    f = open("hour_moist.js", "w")
    f.write("export const\n")
    f.write("moisture = { \n")
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
    
    
def hour_light():
    today = date.today()
    
    sql = '''SELECT hour(time), AVG(light_intensity)
                FROM sensor
                WHERE date = %s
                GROUP BY hour(time)'''
    cursor.execute(sql, [today])

    hourly_result = cursor.fetchall()    
    f = open("hour_light.js", "w")
    f.write("export const\n")
    f.write("light = { \n")
    f.close
    i =0
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
    
def week_hum():
    today = date.today()
    week_ago = (today - timedelta(days=7))
    
    sql = '''SELECT day(date), AVG(humidity)
                FROM sensor
                WHERE date >= %s
                GROUP BY day(date)'''
    cursor.execute(sql, [week_ago])
    weekly_result = cursor.fetchall()  
    f = open("week_hum.js", "w")
    f.write("export const\n")
    f.write("humidity = { \n")
    f.close
    i =0
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

def week_temp():
    today = date.today()
    week_ago = (today - timedelta(days=7))
    
    sql = '''SELECT day(date), AVG(temperature)
                FROM sensor
                WHERE date >= %s
                GROUP BY day(date)'''
    cursor.execute(sql, [week_ago])
    weekly_result = cursor.fetchall()  
    f = open("week_temp.js", "w")
    f.write("export const\n")
    f.write("temperature = { \n")
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

def week_moist():
    today = date.today()
    week_ago = (today - timedelta(days=7))
    
    sql = '''SELECT day(date), AVG(moisture)
                FROM sensor
                WHERE date >= %s
                GROUP BY day(date)'''
    cursor.execute(sql, [week_ago])
    weekly_result = cursor.fetchall()  
    f = open("week_moist.js", "w")
    f.write("export const\n")
    f.write("moisture = { \n")
    f.close
    i =0
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

    
def week_light():
    today = date.today()
    week_ago = (today - timedelta(days=7))
    
    sql = '''SELECT day(date), AVG(light_intensity)
                FROM sensor
                WHERE date >= %s
                GROUP BY day(date)'''
    cursor.execute(sql, [week_ago])
    weekly_result = cursor.fetchall()  
    f = open("week_light.js", "w")
    f.write("export const\n")
    f.write("light = { \n")
    f.close
    i =0
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
  
def backup_data():
    sql = '''SELECT *
                FROM sensor
                WHERE time = (SELECT max(time)
                                    FROM sensor) AND
                      date = (SELECT max(date)
                                    FROM sensor)'''
    cursor.execute(sql)
    result = cursor.fetchone()
    (id, hum, temp, moist, signal, light, time, day) = result
    i = str(id)
    h = str(hum)
    t = str(temp)
    m = str(moist)
    s = str(signal)
    l = str(light)
    ti = str(time)
    d = str(day)
    f = open("backup.txt", "a")
    f.write("id:" + i + " date:" + d + " time:" + ti + " humidity:" + h + " temperature:" + t + " moisture:" + m + " rssi:" + s + " light intensity:" + l)
    f.write('\n')
    f.close()
    
#recent_data()
#hour_temp()
#hour_hum()
#hour_moist()
#hour_light()
#week_temp()
#week_hum()
#week_moist()
#week_light()