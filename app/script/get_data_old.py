import json
import decimal
import datetime
import os
import mysql.connector as database

#class in order to convert decimal to string since JSON does not have 
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


connection = database.connect( 
    user = "root",
    password = "sean16",
    host = "localhost",
    database = 'sensor_data',
)

cursor = connection.cursor()

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def makefile():
    f = open("data.js", "w")
    f.write("export default\n")
    f.close()

def data():
    
    sql = '''SELECT *
                FROM sensor
                WHERE time_stamp = (SELECT max(time_stamp)
                                    FROM sensor)'''

    cursor.execute(sql)

    data_result = cursor.fetchone()
    (id, hum, temp, moist, light, signal, time) = data_result

    hum = str(hum)
    temp = str(temp)
    moist = str(moist)
    light = str(light)
    time = str(time)
    x = {
        "data_id" : id,
        "humidity": hum,
        "temperature": temp,
        "moisture": moist,
        "light_intensity": light,
        "rssi": signal,
        "time": time,
    }


#og method commented out to try new method to include "export default" at beginning -
#this allows data.js to be imported to data_display.js
    with open("data.js", "a") as outfile: 
        json.dump(x, outfile, indent=2)
    print("Json File Created Successfully")    

makefile()
data()