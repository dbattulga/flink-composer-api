from __future__ import absolute_import
from mqtt import MqttPublishHandler
import random
import time

mqttph = MqttPublishHandler('127.0.0.1', 'data-generator', 'test', 'test') #host, client id, username & password
#mqttph = MqttPublishHandler('172.16.96.43', 'data-generator', 'test', 'test') #host, client id, username & password
mqttph.connect()

number = 0

while True:
    mqttph.publish("T-1", number)
    #print (number)
    time.sleep(1) # sleep for seconds
    number += 1

mqttph.disconnect()