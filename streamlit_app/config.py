'''
Configuration Module
'''
import logging
import os
from dataclasses import dataclass, field
from typing import Sequence


@dataclass
class Config():
    '''
    Configuration class
    '''
    # Logger Stuff
    LOGGER_NAME = os.environ.get('LOGGER_NAME', 'root')
    LOG_LEVEL = getattr(logging, os.environ.get('LOG_LEVEL', 'INFO'), logging.INFO)
    LOGGING_CONFIG_FILE = os.environ.get('LOGGING_CONFIG_FILE', './logging.config')
    DEBUG = os.environ.get('DEBUG')


config = Config()
