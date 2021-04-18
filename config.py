import os
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    TOKEN = '490eaa3a505a45713115889a8b06b76d64f55165'
    LOG_LEVEL = 'error'
    LOG_FILE = os.path.join(basedir, 'log.txt')
    PARALLEL = 4
    PAIR = 'XAU/USD'
    FROMDATE = datetime(2014, 3, 1)
    TODATE = datetime(2021, 3, 1)
