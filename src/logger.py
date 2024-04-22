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
    APPLICATION = "application_errors"
    DATA_QUALITY = "data_quality"


def create_logger(logger_type):
    sys.tracebacklimit = 0  # so no stack trace is presented
    env = os.environ["env"]

    log_level = logging.DEBUG if env == "dev" else logging.WARN
    log_path = f"{ROOT_PATH}/logs/{logger_type.value}.log"
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    logger = logging.getLogger(logger_type.name)
    file_handler = logging.FileHandler(log_path, mode="w")
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(log_level)

    return logger
