import time
from datetime import datetime
from time import strftime
from sense_hat import SenseHat
import glob
import MySQLdb
import getco2 


# Initialize Database.
db = MySQLdb.connect(host = "localhost", user = "root", passwd = "redacted", db="test_database")
cur = db.cursor()

# Retrieve SenseHat sensor data.
def get_sensehat_data(): 
    raw_sensor_data = []

    raw_sensor_data.append(MySensor.get_temperature())
    raw_sensor_data.append(MySensor.get_humidity())
    raw_sensor_data.append(MySensor.get_pressure())
    date_and_time = time.strftime("%m-%d-%Y") + " " + time.strftime("%H:%M:%S")
    raw_sensor_data.append(date_and_time)

    return raw_sensor_data

# Formats sensehat data into readable format.
def format_floats(list):
    # Skips last entry in list as it is a datetime.
    for i in range((len(list)-1)):
        roundedValue = round(list[i], 2)
        list[i] = roundedValue

def getCO2ppm():
    # Gets ppm from CO2 sensor                    
    ppm = float(getco2.readppm())  
    if (ppm == -1) :                
        ppm = float(getco2.readppm())
    return ppm                      
                                    
# Initialize SenseHat object                     
MySensor = SenseHat() 

# Updates the database every #update_frequency units of data captured
update_frequency =  10 

while True:
        # Populate list #raw_data with sensor infomration.
        raw_data = get_sensehat_data()
        time.sleep(2)
        format_floats(raw_data)
        print(raw_data)
        temp = raw_data[0]
        humid = raw_data[1]
        press = raw_data[2]
        tstamp = raw_data[3]
        ppm = getCO2ppm()
        
        # Insert sensor information into database.
        sql = ("""INSERT INTO sense_hat_data_char (temperature,humidity,pressure,ppm,timestamp) VALUES (%s,%s,%s,%s,%s)""", (temp,humid,press,ppm,tstamp))
        try:
                print("writing to database...\nwriting to database...\nwriting to database...")
                # Execute insertion.
                cur.execute(*sql)
                db.commit()
                print("Write Complete.\n")

        except KeyboardInterrupt:
                pass
        except:
                # Error, prevent changes to database.
                db.rollback()
                print("Failed to Write")

        # Close connections.
        cur.close()
        db.close()
        break
