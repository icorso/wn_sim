import hashlib
import logging
import os
import random
import sys
from collections import namedtuple
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler
from urllib.parse import urlunparse

from faker import Factory

from constants import Currency

LOGFILE = str(os.path.dirname(os.path.abspath(__file__))) + "/wnapi.log"
LOGGER_FORMAT = '%(asctime)s - %(message)s'
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler(sys.stdout)
f_handler = RotatingFileHandler(LOGFILE, maxBytes=(1048576 * 3), backupCount=2)
# f_handler = logging.FileHandler(LOGFILE)
c_handler.setLevel(logging.WARN)
f_handler.setLevel(logging.WARN)

# Create formatters and add it to handlers
c_format = logging.Formatter(LOGGER_FORMAT)
f_format = logging.Formatter(LOGGER_FORMAT)
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)
