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
temperature = resp_dict["2"]["state"]["temperature"]
lastupdated = resp_dict["2"]["state"]["lastupdated"]

#Connect to database and write latest sensor state
mydb = mysql.connector.connect(host=host,user=user,passwd=passwd)

mycursor = mydb.cursor()

sql = "INSERT INTO homeauto.state_data(lastupdated,state_type,state_value) values(%s,'temperature',%s)"
val = (lastupdated,temperature)
mycursor.execute(sql,val)
mydb.commit()
mydb.close()
