"""
Main entry point of the program for data cleaning and transformation.
"""
import json
import os

import ingestion
from src import logger, quality_checks

app_logger = logger.get_logger(__name__, logger.LoggerType.APPLICATION)
dq_logger = logger.get_logger(__name__, logger.LoggerType.DATA_QUALITY)

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_CONFIG_DIR = f"{ROOT_PATH}/config/data_sources.json"


def run():
    app_logger.info("Program started")
    fleet, maintenance = data_ingestion().values()
    data_cleaning(fleet)
    data_cleaning(maintenance)

    data_transformation()
    app_logger.info("Program finished")


def data_ingestion():
    try:
        json_obj = load_json(JSON_CONFIG_DIR)
        df_fleet = ingestion.read_as_dataframes(f"{ROOT_PATH}/{json_obj['fleet']["path"]}")
        df_maintenance = ingestion.read_as_dataframes(f"{ROOT_PATH}/{json_obj['maintenance']["path"]}")
        df_fleet.name = "fleet"
        df_maintenance.name = "maintenance"
        return {
            "fleet": df_fleet,
            "maintenance": df_maintenance
        }
    except FileNotFoundError as e:
        app_logger.error(e)


def load_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def data_cleaning(df):
    nbr_of_duplicates = quality_checks.count_full_duplicates(df)
    dq_logger.info(f"Duplicate records found for {df.name} data: {nbr_of_duplicates}")

    counters = quality_checks.count_missing_val_per_col(df)
    if not counters.empty:
        dq_logger.info(f"Missing data in {df.name}:")
        for key, value in counters.items():
            if value > 0:
                dq_logger.info(f"{key}: {value} missing values")


def data_transformation():
    return None


if __name__ == "__main__":
    run()
