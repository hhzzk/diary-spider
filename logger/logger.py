import logging, os, gzip
from os.path import basename
from time import localtime, strftime
from logging.handlers import RotatingFileHandler

from config.config import LOG_NAME, LOGS, \
                          OLD_LOGS, LOG_FILE, \
                          MAX_LOG_SIZE, LOG_BACKUP_COUNT

class CompactRotatingFileHandler(RotatingFileHandler):
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0,
                 encoding=None, delay=0):
        RotatingFileHandler.__init__(self, filename, mode, maxBytes,
                                     backupCount, encoding, delay)

    def doRollover(self):
        super(CompactRotatingFileHandler, self).doRollover()
        old_log = self.baseFilename + ".1"
        with open(old_log) as log:
            with gzip.open(MINER_OLD_LOGS + basename(old_log) + \
                           strftime("-%Y-%m-%d-%H:%M:%S.gz",
                                    localtime()), 'wb') as comp_log:
                comp_log.writelines(log)
        os.remove(old_log)

if not os.path.exists(LOGS):
    os.makedirs(LOGS)
if not os.path.exists(OLD_LOGS):
    os.makedirs(OLD_LOGS)

FORMATTER = logging.Formatter('%(asctime)s - %(process)d - %(thread)d - %(name)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s')
CH = logging.StreamHandler()
CH.setFormatter(FORMATTER)

def create_logger(logname, logfile, loglevel=logging.INFO):
    logger = logging.getLogger(logname)
    # levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
    logger.setLevel(loglevel)
    fh = CompactRotatingFileHandler(logfile, maxBytes=LOG_SIZE,
                                    backupCount=BACKUP_COUNT)
    fh.setFormatter(FORMATTER)
    logger.addHandler(fh)
    logger.addHandler(CH)
    return logger

# Create diary logger.
dlogger = create_logger(LOG_NAME, LOG_FILE)
