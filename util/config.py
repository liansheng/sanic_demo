#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: config.py.py
@time: 8/21/18 6:49 PM
"""
import os
import sys
import socket
from sanic import log

kafka_host = "172.16.1.120:19092, 172.16.1.121:19092, 172.16.1.122:19092"
# kafka_host = "172.16.1.122:19092"

default_head_portrait = "/static/img/user/head/default_head_portrait.png"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_IMG_DIR = os.path.join(BASE_DIR, "static", "img")
CAPTCHA_URL = os.path.join(STATIC_IMG_DIR, "captcha.png")
CAPTCHA_TIMEOUT = 5 * 60
CAPTCHA_COLOR = {
    "dark": {
        "text": (93, 192, 255),
        "bg": (42, 45, 50)
    },
    "bright": {
        "text": (88, 68, 207),
        "bg": (237, 237, 237)
    },
}
IMG_RELATIVE_PATH = "/static/img/"
HEAD_PATH = "/var/www/static/img/user/head/"
IMG_PATH = "/var/www/static/"


EXPIRATION_DELTA = 60 * 60 * 24

hostname = socket.gethostname()
hostname = "xianshang"
if hostname == "ubuntu":
    do_main = "http://192.168.1.133:9999"
    REDIS_CONFIG = {"redis": {"address": ("localhost", 6379)}}
    DATABASE_CONFIG = {
        "host": "localhost",
        "port": 27017,
        "name": "account_center",
    }
else:
    do_main = "http://192.168.1.220"
    REDIS_CONFIG = {"redis": {"address": ("192.168.1.220", 6379), "password": "fawo"}}
    DATABASE_CONFIG = {
        "host": "192.168.1.220",
        "port": 27017,
        "name": "account_center",
    }

LOG_SETTINGS_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'loggers': {
        # 'root': {
        #     'level': ['debug', "info", "error"],
        #     'handlers': ['console', 'error'],
        #     'propagate': True
        # },
        "user": {
            "level": "INFO",
            "handlers": ["debug", "info", "error"]
        },
        "root": {
            "level": "INFO",
            "handlers": ["console"]
        },
        "sanic.error": {
            "level": "INFO",
            "handlers": ["error_console"],
            "propagate": True,
            "qualname": "sanic.error"
        },

        "sanic.access": {
            "level": "INFO",
            "handlers": ["access_console"],
            "propagate": True,
            "qualname": "sanic.access"
        }
    },
    'handlers': {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stderr
        },
        "access_console": {
            "class": "logging.StreamHandler",
            "formatter": "access",
            "stream": sys.stdout
        },

        "info": {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'generic',
            'filename': './log/info.log',
            'maxBytes': 1024 * 1024 * 20,
            'backupCount': 50,
            'encoding': 'utf-8'
        },
        "debug": {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'generic',
            'filename': './log/debug.log',
            'maxBytes': 1024 * 1024 * 20,
            'backupCount': 50,
            'encoding': 'utf-8'
        },
        'error': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'generic',
            'filename': './log/error.log',
            'maxBytes': 1024 * 1024 * 20,
            'backupCount': 50,
            'encoding': 'utf-8'
        },

    },
    'formatters': {
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter"
        },
        "access": {
            "format": "%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: " +
                      "%(request)s %(message)s %(status)d %(byte)d",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter"
        },
        "max": {
            # headers host request
            "format": "%(asctime)s - (%(name)s)[%(levelname)s][%(host)s] - [%(headers)s]: " +
                      "%(request)s %(message)s ",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter"
        },

    },

}

if __name__ == '__main__':
    print(CAPTCHA_URL)
    print(BASE_DIR)
    print(os.path.abspath(__file__))
