import requests
import json
import mysql.connector
import os

#Get DB and API settings from environmental variables
host = os.environ['MYSQL_HOST']
user = os.environ['MYSQL_USER']
passwd = os.environ['MYSQL_PWD']
api_host = os.environ['HOMEAUTO_API_HOST']
api_key = os.environ['HOMEAUTO_API_KEY']

#set API part to get data from
api_sub_section = '/sensors'
api_url = api_host+api_key+api_sub_section

#Fetch current sensor data
resp = requests.get(api_url)

resp_dict = resp.json()
temperature = resp_dict["2"]["state"]["temperature"] / 100.0
lastupdated_2 = resp_dict["2"]["state"]["lastupdated"]
humidity = resp_dict["3"]["state"]["humidity"] / 100.0
lastupdated_3 = resp_dict["3"]["state"]["lastupdated"]
pressure = resp_dict["4"]["state"]["pressure"]
lastupdated_4 = resp_dict["4"]["state"]["lastupdated"]

#Connect to database and write latest sensor state
mydb = mysql.connector.connect(host=host,user=user,passwd=passwd)

mycursor = mydb.cursor()

sql = "INSERT INTO homeauto.state_data(lastupdated,state_type,state_value,state_uom) values(%s,'temperature',%s,'C')"
val = (lastupdated_2,temperature)
mycursor.execute(sql,val)
mydb.commit()
sql = "INSERT INTO homeauto.state_data(lastupdated,state_type,state_value,state_uom) values(%s,'humidity',%s,'pp')"
val = (lastupdated_3,humidity)
mycursor.execute(sql,val)
mydb.commit()
sql = "INSERT INTO homeauto.state_data(lastupdated,state_type,state_value,state_uom) values(%s,'pressure',%s,'hPa')"
val = (lastupdated_3,pressure)
mycursor.execute(sql,val)
mydb.commit()
mydb.close()
