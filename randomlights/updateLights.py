
#!/usr/bin/env python

import requests
import json
import mysql.connector
import os
import logging
import sys
import random
import datetime

#logging settings
logging.basicConfig(level=logging.INFO,filename='updateLights.log',format='%(levelname)s %(asctime)s: %(message)s')
logging.info('Running updateLightst')
logging.info('Logging initialized')
#Get DB and API settings from environmental variables
try:
    api_host = os.environ['HOMEAUTO_API_HOST']
    api_key = os.environ['HOMEAUTO_API_KEY']
except:
    logging.warning('Failed to get ENV variable')
    sys.exit()
else:
    logging.info('ENV fetched')

#set API part to get data from
api_sub_section = '/lights'
api_url = api_host+api_key+api_sub_section

#Fetch current sensor data
try:
    resp = requests.get(api_url)
    logging.info('API repsponse received with status: %s',resp.status_code)
    resp_dict = resp.json()
    logging.info('API repsonse parsed')
except:
    logging.warning('Failed to connect to API')
    sys.exit()

#parse response and log if light is on or off
for x in resp_dict:
	if resp_dict[x]["state"]["on"]:
		logging.info(resp_dict[x]["name"]+" is turned on!")
	else:
		logging.info(resp_dict[x]["name"]+" is turned off!")

#set schedule for updating light
turnOnStart = datetime.time(random.randint(9,13),random.randint(1,55),0)
turnOnEnd = datetime.time(13,57,0)
turnOffStart = datetime.time(random.randint(20,23),random.randint(1,55),0)
turnOffEnd = datetime.time(23,57,0) 
logging.info("Interval to turn light on is set between "+turnOnStart.strftime("%X")+" and "+turnOnEnd.strftime("%X"))
logging.info("Interval to turn light off is set between "+turnOffStart.strftime("%X")+" and "+turnOffEnd.strftime("%X"))


#Update lights based on schedule
currentTime = datetime.datetime.now().time()
logging.info("Current time is "+currentTime.strftime("%X"))

try:
	for x in resp_dict:
		api_update_section = "/"+x+"/state"
		if currentTime > turnOnStart and currentTime < turnOnEnd:
			payload = {"on":True}
			response = requests.put(api_url+api_update_section,data = json.dumps(payload))
			logging.info("Tried to turn on "+resp_dict[x]["name"]+" with response:")
			logging.info(response.text)
		elif currentTime > turnOffStart and currentTime < turnOffEnd:
			payload = {"on":False}
			print(json.dumps(payload))
			response = requests.put(api_url+api_update_section,data = json.dumps(payload))
			logging.info("Tried to turn off"+resp_dict[x]["name"]+ " with response:")
			logging.info(response.text)
		else:
			logging.info("No action required, not within time interval")
except:
	logging.warning("Failed to update lights")
	sys.exit()

logging.info("Running uppdateLight finished")

