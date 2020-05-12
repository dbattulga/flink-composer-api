from __future__ import absolute_import, annotations

import logging
import os
import json

import paho.mqtt.client as mqtt

logger = logging.getLogger("uhopper.utils.mqtt")


def get_mqtt_connection_details() -> dict:
    logger.debug("Reading mqtt connection details from environment..")
    return {
        "user": os.environ["MQTT_USER"],
        "password": os.environ["MQTT_PASSWORD"],
        "host": os.environ["MQTT_HOST"],
        "client_id": os.environ["MQTT_CLIENT_ID"],
        "port": int(os.environ["MQTT_PORT"]) if "MQTT_PORT" in os.environ else 1883,
        "base_topic": os.environ["MQTT_BASE_TOPIC"] if "MQTT_BASE_TOPIC" in os.environ else None
    }


def get_mqtt_publisher_from_env() -> MqttPublishHandler:
    details = get_mqtt_connection_details()
    return MqttPublishHandler(
        details["host"],
        details["client_id"],
        details["user"],
        details["password"],
        port=details["port"],
        base_topic=details["base_topic"]
    )


def get_mqtt_subscriber_from_env(on_message_f=None) -> MqttSubscriptionHandler:
    details = get_mqtt_connection_details()
    return MqttSubscriptionHandler(
        details["host"],
        details["client_id"],
        details["user"],
        details["password"],
        port=details["port"],
        on_message_f=on_message_f,
        base_topic=details["base_topic"]
    )


class MqttHandler(object):

    def __init__(self, host: str, client_id: str, user: str, password: str, port: int = 1883, base_topic: str = None) -> None:
        self._host = host
        self._port = port
        self._base_topic = base_topic

        self._client = mqtt.Client(client_id=client_id)
        self._client.username_pw_set(user, password=password)
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect

    def _complete_topic(self, topic: str):
        prefix = "" if not self._base_topic else "%s/" % self._base_topic
        return "%s%s" % (prefix, topic)

    # TODO if connection fails no error is returned !!!
    def connect(self, keep_alive: int = 60) -> None:
        self._client.connect(self._host, port=self._port, keepalive=keep_alive)

    def disconnect(self) -> None:
        self._client.loop_stop()
        self._client.disconnect()

    @staticmethod
    def _on_connect(client, user_data, flags, rc):
        if rc != 0:
            logger.error("Error while connecting to broker: return code was [%s] and user_data [%s]" % (rc, user_data))
            raise Exception("Could not connect to broker: return code was %d" % rc)

        logger.info("Successfully connected to broker(result code %d)" % rc)

    @staticmethod
    def _on_disconnect(client, userdata, rc):
        logger.info("Disconnecting from broker: client [%s], user data [%s], rc [%s]" % (client, userdata, rc))


class MqttPublishHandler(MqttHandler):

    def publish(self, topic: str, payload: str, qos: int = 1, retain: bool = False) -> None:
        logger.debug("New message ready to send on topic [%s]: %s" % (topic, payload))
        self._client.publish(self._complete_topic(topic), payload, qos=qos, retain=retain)

    def publish_data(self, topic: str, payload: dict, qos: int = 1, retain: bool = False) -> None:
        self.publish(topic, json.dumps(payload), qos=qos, retain=retain)

    def connect(self, keep_alive: int = 60) -> None:
        super().connect(keep_alive)
        self._client.loop_start()

    def disconnect(self) -> None:
        self._client.loop_stop()
        super().disconnect()


class MqttSubscriptionHandler(MqttHandler):

    def __init__(self, host, client_id, user, password, on_message_f=None, port=1883, base_topic: str = None):
        super().__init__(host, client_id, user, password, port=port, base_topic=base_topic)
        self._client.on_message = self._on_message
        self._on_message_f = on_message_f if on_message_f else \
            lambda x: logger.warning("Undefined on_message_f for MQTT subscriber")
        self._topics = []

    def _on_connect(self, client, user_data, flags, rc):
        if rc != 0:
            logger.error("Error while connecting to broker: return code was [%s] and user_data [%s]" % (rc, user_data))
            raise Exception("Could not connect to broker: return code was %d" % rc)

        logger.info("Successfully connected to broker (result code %d)" % rc)
        for (topic, qos) in self._topics:
            sub_topic = self._complete_topic(topic)
            logger.debug("Subscribing to topic [%s]" % sub_topic)
            self._client.subscribe(sub_topic, qos=qos)

    def with_on_message_f(self, on_message_f):
        self._on_message_f = on_message_f

    def listen(self):
        logger.info("Starting listening...")
        self._client.loop_forever()

    def add_subscription(self, topic, qos=1):
        logger.debug("Adding topic [%s] to list of subscriptions with qos=%d" % (topic, qos))
        self._topics.append((topic, qos))

    def _on_message(self, client, user_data, msg):
        logger.debug("New message: client [%s], user_data [%s], topic [%s], payload [%s]" % (client, user_data, msg.topic, str(msg.payload)))
        self._on_message_f(msg.payload)
