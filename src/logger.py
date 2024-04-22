import logging
import logging.config
import os
import sys
from enum import Enum

from dotenv import find_dotenv, load_dotenv

env_file = find_dotenv()
load_dotenv()

CONFIG_DIR = "../config"
LOG_DIR = "../logs"


class LoggerType(Enum):
    APPLICATION = 1
    DATA_QUALITY = 2


def get_logger(name, logger_type):
    sys.tracebacklimit = 0 # so no stack trace is presented
    log_configs = {"DEV": "logging.dev.ini", "PROD": "logging.prod.ini"}
    config = log_configs.get(os.environ["ENV"], "logging.dev.ini")
    config_path = "/".join([CONFIG_DIR, config])

    logging.config.fileConfig(
        config_path,
        disable_existing_loggers=False,
        defaults={
            "logfilename": f"{LOG_DIR}/{'application_errors' if logger_type == LoggerType.APPLICATION else 'data_quality'}.log"},
    )

    return logging.getLogger(name)
