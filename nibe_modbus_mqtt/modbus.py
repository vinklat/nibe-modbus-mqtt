# -*- coding: utf-8 -*-
'''
Connect to a Nibe Modbus tcp slave device
'''

import logging
from modbus_tk import modbus_tcp, hooks
from modbus_tk.defines import READ_HOLDING_REGISTERS

# create logger
logger = logging.getLogger(__name__)


class ModbusException(Exception):
    def __init__(self, message):
        Exception.__init__(self, f'Modbus: {message}')


class Modbus():
    '''
    Send / receive data from a Nibe heat pump
    '''
    def __init__(self):
        self.master = None
        self.recv_total = 0
        self.recv_bytes = 0
        self.recv_invalid = 0
        self.send_total = 0
        self.send_bytes = 0
        hooks.install_hook('modbus.Master.before_send', self.on_before_send)
        hooks.install_hook('modbus.Master.after_recv', self.on_after_recv)
        hooks.install_hook('modbus_tcp.TcpMaster.after_connect', self.on_after_connect)

    def on_after_connect(self, _):
        logger.info("Modbus connected OK")

    def on_before_send(self, data):
        _, bytes_data = data
        size = len(bytes_data)
        self.send_total += 1
        self.send_bytes += size
        logger.debug("n=%d, size=%d, data=%s", self.send_total, size, bytes_data)
        logger.debug("bytes_total=%d", self.send_bytes)

    def on_after_recv(self, data):
        _, bytes_data = data
        size = len(bytes_data)
        self.recv_total += 1
        self.recv_bytes += size
        if size < 10:
            logger.error("received invalid value")
            self.recv_invalid += 1
        logger.debug("n=%d, size=%d, data=%s", self.recv_total, size, bytes_data)
        logger.debug("bytes_total=%d, invalid_total=%d", self.recv_bytes,
                     self.recv_invalid)

    def connect(self, host, port, timeout=10):
        self.master = modbus_tcp.TcpMaster(host=host, port=port)
        self.master.set_timeout(timeout)

    def read_slow_register(self, register):
        try:
            registers = self.master.execute(1, READ_HOLDING_REGISTERS, register, 1)
        except (ConnectionRefusedError, OSError) as exc:
            raise ModbusException(exc) from exc
        return registers[0]

    def read_fast_registers(self, register, count=20):
        try:
            registers = self.master.execute(1, READ_HOLDING_REGISTERS, register, count)
        except (ConnectionRefusedError, OSError) as exc:
            raise ModbusException(exc) from exc
        return registers
