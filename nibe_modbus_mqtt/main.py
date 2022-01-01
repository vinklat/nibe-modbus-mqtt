# -*- coding: utf-8 -*-
'''
MQTT bridge for a Nibe heat pump connected to the Modbus
'''

from apscheduler.schedulers.background import BackgroundScheduler
from nibe_modbus_mqtt.argparser import pars
from nibe_modbus_mqtt.logger import logger
from nibe_modbus_mqtt.modbus import Modbus
from nibe_modbus_mqtt.jobs import Jobs
from nibe_modbus_mqtt.version import app_instance
from nibe_modbus_mqtt.mqtt import Mqqt, MqttException


def main():
    logger.info("Starting %s", app_instance)
    modbus = Modbus()
    modbus.connect(pars.modbus_slave_host,
                   pars.modbus_slave_port,
                   timeout=pars.modbus_timeout)

    mqtt = Mqqt(pars.mqtt_topic_publish, pars.mqtt_topic_subscribe)
    jobs = Jobs(modbus, mqtt)
    sched = BackgroundScheduler(daemon=True)

    sched.add_job(jobs.fast_job, 'interval', seconds=9.98)
    sched.add_job(jobs.regular_job, 'interval', seconds=5.14)
    sched.add_job(jobs.slow_job, 'interval', seconds=15.33)
    sched.start()

    try:
        mqtt.connect(
            pars.mqtt_broker_host,
            pars.mqtt_broker_port,
            keepalive=pars.mqtt_keepalive,
        )
    except MqttException as exc:
        logger.critical(exc)
        return

    # forever loop
    mqtt.loop()
