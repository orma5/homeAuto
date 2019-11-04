FROM python:3
COPY /statecapture/sensorTest.py /
RUN pip install requests mysql.connector
CMD [ "python", "./sensorTest.py" ]
