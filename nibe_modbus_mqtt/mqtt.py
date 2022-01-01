# -*- coding: utf-8 -*-
'''
Connect to a MQTT broker
'''

import logging
import time
from socket import gaierror
import paho.mqtt.client as mqtt
from .version import app_instance

# create logger
logger = logging.getLogger(__name__)


class MqttException(Exception):
    def __init__(self, message):
        Exception.__init__(self, f'MQTT: {message}')


class Mqqt():
    def __init__(self, topic_publish: str, topic_subscribe: str) -> None:
        self.client = mqtt.Client(app_instance)
        self.client.connected_flag = False
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.client.on_message = self.on_message
        self.topic_publish = topic_publish
        self.topic_subscribe = topic_subscribe

    def connect(self, host: str, port: int, keepalive=30):
        try:
            self.client.connect(host, port, keepalive)
        except (ConnectionRefusedError, OSError, gaierror) as exc:
            raise MqttException(exc) from exc

    def is_connected(self):
        return self.client.connected_flag

    def on_connect(self, _, userdata, flags, ret):
        '''
        fired upon a successful connection

        ret values:
        0: Connection successful
        1: Connection refused - incorrect protocol version
        2: Connection refused - invalid client identifier
        3: Connection refused - server unavailable
        4: Connection refused - bad username or password
        5: Connection refused - not authorised
        6-255: Currently unused.
        '''
        if ret == 0:
            self.client.connected_flag = True
            logger.info("MQTT connected OK")
            logger.debug("userdata=%s, flags=%s, ret=%s", userdata, flags, ret)
        else:
            logger.error("MQTT connect ERROR: ret=%s", ret)

    def on_disconnect(self, _, userdata, ret):
        '''fired upon a disconnection'''

        self.client.connected_flag = False
        logger.error("MQTT disconnect")
        logger.debug("userdata=%s, ret=%s", userdata, ret)

    def on_publish(self, client, userdata, mid):
        '''fired upon a message published'''

        del client  # Ignored parameter
        logger.debug("MQTT published: userdata=%s, mid=%s", userdata, mid)

    def on_message(self, client, userdata, msg):
        '''receive message from MQTT'''

        del client  # Ignored parameter
        logger.info("MQTT receive: %s %s", msg.topic, msg.payload)
        logger.debug("userdata=%s", userdata)

    def loop(self):
        self.client.loop_start()

        while True:
            nattempts = 0
            while not self.is_connected():
                if nattempts > 0:
                    logger.error("MQTT connect wait... (attempt=%s)", nattempts)
                time.sleep(10)
                nattempts += 1
            time.sleep(1)

    def publish(self, payload):
        logging.info("MQTT publish: %s %s", self.topic_publish, payload)
        self.client.publish(self.topic_publish, payload)
