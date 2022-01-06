# -*- coding: utf-8 -*-
'''
Read data from modbus registers and send to MQTT
'''

import logging
import time
import json
from nibe_modbus_mqtt.registers import FAST_REGISTERS, SLOW_REGISTERS, REGULAR_REGISTERS
from nibe_modbus_mqtt.modbus import ModbusException

# create logger
logger = logging.getLogger(__name__)


class Jobs():
    def __init__(self, modbus, mqtt):
        self.modbus = modbus
        self.mqtt = mqtt
        self.prev_t_fast = 0.0
        self.prev_t_regular = 0.0
        self.prev_t_slow = 0.0
        self.last_regular_pos = 0
        self.last_slow_pos = 0

        # attrs for calc extra metrics:
        self.power_meters = {}

    def fix_value(self, raw_value, divisor, sign):
        value = None

        if raw_value >= (1 << 15) and sign == 'S':
            raw_value -= (1 << 16)

        if isinstance(divisor, int):
            value = float(raw_value) / divisor

        return value

    def slow_job(self):
        '''
        Batch of not frequently changing metrics.
        These registers must be read only one at a time.
        '''

        if self.last_slow_pos == len(SLOW_REGISTERS):
            self.last_slow_pos = 0

        register, description, divisor, sign = SLOW_REGISTERS[self.last_slow_pos]
        self.last_slow_pos += 1

        try:
            raw_value = self.modbus.read_slow_register(register)
        except ModbusException as exc:
            logger.error(exc)
            return

        t = time.perf_counter()
        if self.prev_t_slow > 0:
            duration = t - self.prev_t_slow
            logger.debug("duration=%f", duration)
        else:
            duration = None
        self.prev_t_slow = t

        value = self.fix_value(raw_value, divisor, sign)
        logger.info("%d %s = %f", register, description, value)

        payload = {register: value}
        self.mqtt.publish(json.dumps(payload))

    def regular_job(self):
        '''
        Batch of common metrics.
        These egisters must be read only one at a time.
        '''

        if self.last_regular_pos == len(REGULAR_REGISTERS):
            self.last_regular_pos = 0

        register, description, divisor, sign = REGULAR_REGISTERS[self.last_regular_pos]
        self.last_regular_pos += 1

        try:
            raw_value = self.modbus.read_slow_register(register)
        except ModbusException as exc:
            logger.error(exc)
            return

        t = time.perf_counter()
        if self.prev_t_regular > 0:
            duration = t - self.prev_t_regular
            logger.debug("duration=%f", duration)
        else:
            duration = None
        self.prev_t_regular = t

        value = self.fix_value(raw_value, divisor, sign)
        logger.info("%d %s = %f", register, description, value)

        payload = {register: value}
        self.mqtt.publish(json.dumps(payload))

    def fast_job(self):
        '''
        Faster reading of predefined metrics in SET.LOG in Nibe device.
        Can 20 registers at a time.
        '''

        try:
            registers = self.modbus.read_fast_registers(40083)
        except ModbusException as exc:
            logger.error(exc)
            return

        t = time.perf_counter()
        if self.prev_t_fast > 0:
            duration = t - self.prev_t_fast
            logger.debug("duration=%f", duration)
        else:
            duration = None
        self.prev_t_fast = t

        payload = {}
        i = 0
        imax = len(FAST_REGISTERS)

        while i < imax:
            if isinstance(FAST_REGISTERS[i], list):
                register, description, divisor, sign = FAST_REGISTERS[i]
                value = self.fix_value(registers[i], divisor, sign)
                logger.info("%d %s = %f", register, description, value)
                payload[register] = value

                # count extra metrics:
                # - power charge from current
                if (duration is not None) and description.endswith('[A]'):
                    key = f'{register}_C'
                    if key not in self.power_meters:
                        logger.debug("Init power meter %s...", key)
                        meter = 0
                    else:
                        meter = self.power_meters[key]
                    
                    meter += (value * duration)
                    self.power_meters[key] = meter
                    logger.info("%s = %f", key, meter)
                    payload[key] = meter
            i += 1

        self.mqtt.publish(json.dumps(payload))
