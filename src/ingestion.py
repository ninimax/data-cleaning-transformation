from logger import *
import pandas as pd

app_logger = get_logger(__name__, LoggerType.APPLICATION)
dq_logger = get_logger(__name__, LoggerType.DATA_QUALITY)


def read_data(path):
    df = pd.read_csv(path)
    app_logger.debug(f"successfully loaded {path}")
    return df