"""
Main entry point of the program for data cleaning and transformation.
"""
import json
import os

import ingestion
from src import logger, quality_checks

app_logger = logger.create_logger(logger.LoggerType.APPLICATION)
dq_logger = logger.create_logger(logger.LoggerType.DATA_QUALITY)

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_CONFIG_DIR = f"{ROOT_PATH}/data_sources.json"


def run():
    app_logger.info("Program started")

    fleet, maintenance = data_ingestion().values()

    log_duplicates(fleet)
    log_duplicates(maintenance)

    log_missing_vals(fleet)
    log_missing_vals(maintenance)

    log_missing_fleet_truck_ids(maintenance, fleet)

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
    except Exception as e:
        app_logger.error(e)


def load_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def log_duplicates(df):
    nbr_of_duplicates = quality_checks.count_full_duplicates(df)
    dq_logger.info(f"Duplicate records found for {df.name} data: {nbr_of_duplicates}")


def log_missing_vals(df):
    counters = quality_checks.count_missing_val_per_col(df)
    if not counters.empty:
        dq_logger.info(f"Missing data in {df.name}:")
        for key, value in counters.items():
            if value > 0:
                dq_logger.info(f"   {key}: {value} missing values")


def log_missing_fleet_truck_ids(df1, df2):
    ids_only_in_df1_but_not_df2 = quality_checks.get_items_existing_in_df1_only(df1, df2, "truck_id")
    dq_logger.info(f"Truck IDs missing from the fleet dataset: {', '.join(map(str, ids_only_in_df1_but_not_df2))}")


def data_transformation():
    return None


if __name__ == "__main__":
    run()
