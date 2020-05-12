FROM python:3

ADD mqtt.py /
ADD number_generator.py /
ADD status_check.py /


RUN pip install future
RUN pip install paho-mqtt

CMD [ "python", "./number_generator.py &" ]
CMD [ "python", "./status_check.py" ]