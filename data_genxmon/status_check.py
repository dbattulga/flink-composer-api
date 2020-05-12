from __future__ import absolute_import
from mqtt import MqttSubscriptionHandler

#f1 = open('endResults.csv', 'a+')

def f(msg):
    #f1.write(msg.decode())
    print(msg)


mp = MqttSubscriptionHandler("127.0.0.1", "status-checker", "test", "test") #host, client id, username & password
#mp = MqttSubscriptionHandler("172.16.98.9", "3", "mqtt-sub", "mqtt-sub") #host, client id, username & password
mp.add_subscription("T-N")
mp.connect()
mp.with_on_message_f(f)
mp.listen()
#f1.close()