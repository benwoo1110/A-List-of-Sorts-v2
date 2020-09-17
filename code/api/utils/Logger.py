import logging
import os
import sys
import glob
import traceback
from functools import wraps
from datetime import datetime


class Logger:
    FORMATTER = logging.Formatter('[%(asctime)s %(levelname)s] [%(name)s] %(message)s', datefmt='%H:%M:%S')
    LOG_FILENAME = datetime.now().strftime("./logs/%d-%m-%Y_%H-%M-%S.log")
    LOGS_LOCATION = "./logs/"

    isSetUp = False
    logger = logging.getLogger()

    @staticmethod
    def setUp(loggerName:str, maxKeepLog:int, consoleLevel:str, fileLevel:str):
        if Logger.isSetUp:
            Logger.logger.error("Logger has already been setup!")
            return

        # Setup log file directory
        logFiles = glob.glob(os.path.join(Logger.LOGS_LOCATION, "*.log"))
        logFiles.sort(key=os.path.getmtime)
        for i in range(len(logFiles) - max(0, maxKeepLog-1)):
            os.remove(logFiles[i])

        # Console logging
        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setLevel(Logger.levelFromString(fileLevel))
        consoleHandler.setFormatter(Logger.FORMATTER)

        # Logging to log file
        fileHandler = logging.FileHandler(Logger.LOG_FILENAME)
        fileHandler.setLevel(Logger.levelFromString(fileLevel))
        fileHandler.setFormatter(Logger.FORMATTER)

        # Create logging object
        Logger.logger = logging.getLogger(loggerName)
        Logger.logger.setLevel(logging.DEBUG)
        Logger.logger.addHandler(consoleHandler)
        Logger.logger.addHandler(fileHandler)

        isSetUp = True

    @staticmethod
    def get() -> logging.getLogger:
        return Logger.logger

    @staticmethod
    def method():
        def inner_function(func):
            @wraps(func)
            def log_method(*args, **kwargs):
                Logger.logger.debug('Running {} with arguments {} {}'.format(func.__name__, args, kwargs))
                return func(*args, **kwargs)
            return log_method
        return inner_function

    @staticmethod
    def levelFromString(level:str) -> int:
        return os.environ.get("LOGLEVEL", level.upper())