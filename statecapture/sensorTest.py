#!/usr/bin/env python

import requests
import json
import mysql.connector
import os
import logging
import sys

#logging settings
logging.basicConfig(level=logging.INFO,filename='/var/log/sensorTest.log',format='%(levelname)s %(asctime)s: %(message)s')
#logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logging.info('Running sensorTest')
logging.info('Loggin initialized')

#Get DB and API settings from environmental variables
try:
    host = os.environ['MYSQL_HOST']
    user = os.environ['MYSQL_USER']
    passwd = os.environ['MYSQL_PWD']
    api_host = os.environ['HOMEAUTO_API_HOST']
    api_key = os.environ['HOMEAUTO_API_KEY']
except:
    logging.warning('Failed to get ENV variable')
    sys.exit()
else:
    logging.info('ENV fetched')

#set API part to get data from
api_sub_section = '/sensors'
api_url = api_host+api_key+api_sub_section

#Fetch current sensor data
try:
    resp = requests.get(api_url)
    logging.info('API repsponse received with status: %s',resp.status_code)

    resp_dict = resp.json()

    temperature = resp_dict["2"]["state"]["temperature"] / 100.0
    lastupdated_2 = resp_dict["2"]["state"]["lastupdated"]
    humidity = resp_dict["3"]["state"]["humidity"] / 100.0
    lastupdated_3 = resp_dict["3"]["state"]["lastupdated"]
    pressure = resp_dict["4"]["state"]["pressure"]
    lastupdated_4 = resp_dict["4"]["state"]["lastupdated"]
    logging.info('API repsonse parsed')
except:
    logging.warning('Failed to connect to API')
    sys.exit()

#Connect to database and write latest sensor state
try:
    logging.info('Connecting to database host: %s with user: %s',host,user)
    mydb = mysql.connector.connect(host=host,user=user,passwd=passwd)
    logging.info('Connection successfull')
    mycursor = mydb.cursor()

    sql = "INSERT INTO homeauto.state_data(lastupdated,state_type,state_value,state_uom) values(%s,'temperature',%s,'C')"
    val = (lastupdated_2,temperature)
    mycursor.execute(sql,val)
    mydb.commit()
    logging.info('Temperature value insert with value: %s', temperature)
    sql = "INSERT INTO homeauto.state_data(lastupdated,state_type,state_value,state_uom) values(%s,'humidity',%s,'pp')"
    val = (lastupdated_3,humidity)
    mycursor.execute(sql,val)
    mydb.commit()
    logging.info('Humidity insert with value: %s',humidity)
    sql = "INSERT INTO homeauto.state_data(lastupdated,state_type,state_value,state_uom) values(%s,'pressure',%s,'hPa')"
    val = (lastupdated_3,pressure)
    mycursor.execute(sql,val)
    mydb.commit()
    logging.info('Pressure insert with value: %s',pressure)
    mydb.close()
    logging.info('Database connection closed')
except:
    logging.warning('Failed to connect or write to database')
    sys.exit()

logging.info('Running sensortest finished!')
