FROM python:3
COPY /statecapture/sensorTest.py /
RUN pip install requests json mysql.connector os
CMD [ "python", "./sensorTest.py" ]
