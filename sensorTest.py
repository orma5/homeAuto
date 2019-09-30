import requests
import json
import mysql.connector

resp = requests.get('http://192.168.1.204:80/api/07919579F9/sensors')

resp_dict = resp.json()
temperature = resp_dict["2"]["state"]["temperature"]
lastupdated = resp_dict["2"]["state"]["lastupdated"]

mydb = mysql.connector.connect(host="192.168.1.22",user="administrator",passwd="1qaz!QAZ")

mycursor = mydb.cursor()

sql = "INSERT INTO homeauto.state_data(lastupdated,state_type,state_value) values(%s,'temperature',%s)"
val = (lastupdated,temperature)
mycursor.execute(sql,val)
mydb.commit()
