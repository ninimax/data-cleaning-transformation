"""
Main entry point of the program for data cleaning and transformation.
"""
import json
import os

import ingestion
from src import logger, quality_checks

application_logger = logger.get_logger(__name__, logger.LoggerType.APPLICATION)

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_CONFIG_DIR = f"{ROOT_PATH}/config/data_sources.json"


def load_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


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
        application_logger.error(e)


def data_cleaning(df):
    nbr_of_duplicates = quality_checks.count_full_duplicates(df)

    if nbr_of_duplicates >= 2:
        application_logger.info(f"Duplicate records found for {df.name} data: {nbr_of_duplicates}")


def data_transformation():
    return None


def run():
    application_logger.info("Program started")
    fleet, maintenance = data_ingestion().values()
    data_cleaning(fleet)
    data_cleaning(maintenance)

    data_transformation()
    application_logger.info("Program finished")


if __name__ == "__main__":
    run()
