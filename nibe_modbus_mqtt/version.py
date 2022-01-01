# -*- coding: utf-8 -*-
'''
app version and resources info
'''

import time
from platform import python_version
import pkg_resources

__version__ = '0.0.1'
app_name = 'nibe-modbus-mqtt'
# pylint: disable=consider-using-f-string
inst_id = '{0:010x}'.format(int(time.time() * 256))[:10]
app_instance = f'{app_name}_{inst_id}'

def get_version_info():
    '''get app version info'''

    ret = {
        'version': __version__,
    }

    return ret


def get_runtime_info():
    '''get app and resources runtime info'''

    modules = {
        'paho-mqtt': pkg_resources.get_distribution("paho-mqtt").version,
        'pymodbus': pkg_resources.get_distribution("pymodbus").version,
    }

    runtime = {
        'python_version': python_version(),
    }

    ret = {**get_version_info(), **runtime, 'python_modules': modules}

    return ret
