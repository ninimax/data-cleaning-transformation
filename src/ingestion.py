import pandas as pd

from src import logger

app_logger = logger.get_logger(__name__, logger.LoggerType.APPLICATION)
dq_logger = logger.get_logger(__name__, logger.LoggerType.DATA_QUALITY)


def read_as_dataframes(path):
    df = pd.read_csv(path)
    app_logger.debug(f"successfully loaded {path}")
    return df
