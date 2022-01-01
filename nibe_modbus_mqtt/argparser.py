# -*- coding: utf-8 -*-
'''cmd line argument and ENV parser'''

import logging
import os
from argparse import ArgumentParser, ArgumentTypeError
from nibe_modbus_mqtt.version import __version__, app_name, get_runtime_info

LOG_LEVEL_STRINGS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
LOG_LEVEL_DEFAULT = 'INFO'
LOG_VERBOSE_DEFAULT = False
MQTT_BROKER_PORT = 1883
MQTT_KEEPALIVE = 30
MQTT_TOPIC_PUBLISH = 'nibe/R'
MQTT_TOPIC_SUBSCRIBE = 'nibe/W'
MODBUS_SLAVE_PORT = 502
MODBUS_TIMEOUT = 10
REGISTERS_CONFIG = 'conf/nibe.yml'


def log_level_string_to_int(arg_string: str) -> int:
    '''get log level int from string'''

    log_level_string = arg_string.upper()
    if log_level_string not in LOG_LEVEL_STRINGS:
        message = (f"invalid choice: {log_level_string} "
                   f"(choose from {LOG_LEVEL_STRINGS})")
        raise ArgumentTypeError(message)

    log_level_int = getattr(logging, log_level_string, logging.INFO)
    # check the log_level_choices have not changed from our expected values
    assert isinstance(log_level_int, int)

    return log_level_int


def get_pars():
    '''
    get parameters from from command line arguments
    defaults overriden by ENVs
    '''

    env_vars = {
        'MQTT_BROKER_HOST': {
            'required': True
        },
        'MQTT_BROKER_PORT': {
            'default': MQTT_BROKER_PORT
        },
        'MQTT_KEEPALIVE': {
            'default': MQTT_KEEPALIVE
        },
        'MQTT_TOPIC_PUBLISH': {
            'default': MQTT_TOPIC_PUBLISH
        },
        'MQTT_TOPIC_SUBSCRIBE': {
            'default': MQTT_TOPIC_SUBSCRIBE
        },
        'MODBUS_SLAVE_HOST': {
            'required': True
        },
        'MODBUS_SLAVE_PORT': {
            'default': MODBUS_SLAVE_PORT
        },
        'MODBUS_TIMEOUT': {
            'default': MODBUS_TIMEOUT
        },
        # 'REGISTERS_CONFIG': {
        #     'default': REGISTERS_CONFIG
        # },
        'LOG_LEVEL': {
            'default': LOG_LEVEL_DEFAULT
        },
        'LOG_VERBOSE': {
            'default': LOG_VERBOSE_DEFAULT
        },
    }

    # defaults overriden from ENVs
    for env_var, env_pars in env_vars.items():
        if env_var in os.environ:
            default = os.environ[env_var]
            if 'default' in env_pars:
                if isinstance(env_pars['default'], bool):
                    default = bool(os.environ[env_var])
                elif isinstance(env_pars['default'], int):
                    default = int(os.environ[env_var])
            env_pars['default'] = default
            env_pars['required'] = False

    parser = ArgumentParser(description=f'{app_name} {__version__}')

    parser.add_argument('-q',
                        '--mqtt-broker-host',
                        action='store',
                        dest='mqtt_broker_host',
                        help='MQTT broker host address',
                        type=str,
                        **env_vars['MQTT_BROKER_HOST'])
    parser.add_argument('-p',
                        '--mqtt-broker-port',
                        action='store',
                        dest='mqtt_broker_port',
                        help=('MQTT broker port '
                              f'(default {MQTT_BROKER_PORT})'),
                        type=int,
                        **env_vars['MQTT_BROKER_PORT'])
    parser.add_argument('-k',
                        '--mqtt-keepalive',
                        action='store',
                        dest='mqtt_keepalive',
                        help=('MQTT keepalive timeout in seconds '
                              f'(default {MQTT_KEEPALIVE})'),
                        type=int,
                        **env_vars['MQTT_KEEPALIVE'])
    parser.add_argument('-t',
                        '--mqtt-topic-publish',
                        action='store',
                        dest='mqtt_topic_publish',
                        help=('MQTT publish topic for emit pump metrics '
                              f'(default {MQTT_TOPIC_PUBLISH})'),
                        type=str,
                        **env_vars['MQTT_TOPIC_PUBLISH'])
    parser.add_argument('-r',
                        '--mqtt-topic-subscribe',
                        action='store',
                        dest='mqtt_topic_subscribe',
                        help=('MQTT subscribe topic for pump settings'
                              f'(default {MQTT_TOPIC_SUBSCRIBE})'),
                        type=str,
                        **env_vars['MQTT_TOPIC_SUBSCRIBE'])
    parser.add_argument('-m',
                        '--modbus-slave-host',
                        action='store',
                        dest='modbus_slave_host',
                        help='Modbus slave TCP host',
                        type=str,
                        **env_vars['MODBUS_SLAVE_HOST'])
    parser.add_argument('-P',
                        '--modbus-slave-port',
                        action='store',
                        dest='modbus_slave_port',
                        help=('Modbus slave TCP port '
                              f'(default {MODBUS_SLAVE_PORT})'),
                        type=int,
                        **env_vars['MODBUS_SLAVE_PORT'])
    parser.add_argument('-T',
                        '--modbus-timeout',
                        action='store',
                        dest='modbus_timeout',
                        help=('Modbus timeout in seconds'
                              f'(default {MODBUS_TIMEOUT})'),
                        type=int,
                        **env_vars['MODBUS_TIMEOUT'])
    # parser.add_argument('-c',
    #                     '--nibe-config',
    #                     action='store',
    #                     dest='conf_fname',
    #                     help=('Nibe modbus registers config yaml file '
    #                           f'(default {REGISTERS_CONFIG})'),
    #                     type=str,
    #                     **env_vars['REGISTERS_CONFIG'])
    parser.add_argument('-V',
                        '--version',
                        action='version',
                        version=str(get_runtime_info()))
    parser.add_argument('-l',
                        '--log-level',
                        action='store',
                        dest='log_level',
                        help=("set the logging output level. "
                              f"{LOG_LEVEL_STRINGS} "
                              f"(default {LOG_LEVEL_DEFAULT})"),
                        type=log_level_string_to_int,
                        **env_vars['LOG_LEVEL'])
    parser.add_argument('-v',
                        '--log-verbose',
                        action='store_true',
                        dest='log_verbose',
                        help='most verbose debug level '
                        '(console only; useful for a bug hunt :)',
                        **env_vars['LOG_VERBOSE'])

    return parser.parse_args()


# get parameters from command line arguments
pars = get_pars()
