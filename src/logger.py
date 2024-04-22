import logging
import logging.config
import os
import sys
from enum import Enum

from dotenv import find_dotenv, load_dotenv

env_file = find_dotenv()
load_dotenv()

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class LoggerType(Enum):
    APPLICATION = 1
    DATA_QUALITY = 2


def get_logger(name, logger_type):
    sys.tracebacklimit = 0  # so no stack trace is presented
    config_path = f"{ROOT_PATH}/config/{"logging.dev.ini" if os.environ["ENV"] == "DEV" else "logging.prod.ini"}"
    logging.config.fileConfig(
        config_path,
        disable_existing_loggers=False,
        defaults={
            "logfilename": f"{ROOT_PATH}/logs/{'application_errors' if logger_type == LoggerType.APPLICATION else 'data_quality'}.log"},
    )

    return logging.getLogger(name)
