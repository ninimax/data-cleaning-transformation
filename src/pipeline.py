"""
Main entry point of the program for data cleaning and transformation.
"""
import json
import os

import pandas as pd

# disable warnings while using pipe(), default='warn'
pd.options.mode.chained_assignment = None

from src import ingestion, logger, quality_checks, processing

app_logger = logger.create_logger(logger.LoggerType.APPLICATION)
dq_logger = logger.create_logger(logger.LoggerType.DATA_QUALITY)

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_CONFIG_DIR = f"{ROOT_PATH}/data_sources.json"


def run(fleet_data_path, maintenance_data_path, export_file_path):
    """
    The program runs and does the follows:
    1) data ingestion:
        read csv files of fleet and maintenance based on the
        configurations defined in data_sources.json.
    2) data quality assessment:
        check and log for duplicated rows, missing values, and truck_id
        present in the maintenance dataset but not in the fleet dataset.
    3) data cleaning and transformation:
        drop fully duplicated rows,
        standardize text and dates of selected columns,
        apply one-hot encoding on service_type,
        add column email_valid for rows with valid technician_email address.
    4) data integration:
        merge the cleaned and processed fleet and maintenance dataframe into
        one and export as a csv file actual_fleet_maintenance_MERGED.csv
    """

    app_logger.info("Program started")

    try:
        fleet, maintenance = data_ingestion(fleet_data_path,
                                            maintenance_data_path).values()

        data_quality_assessment(fleet, maintenance)

        processed_fleet, processed_maintenance = data_cleaning_transformation(
            fleet,
            maintenance).values()

        merged_fleet_maintenance = data_integration(processed_fleet,
                                                    processed_maintenance)

        processing.export_to_csv(
            merged_fleet_maintenance,
            export_file_path)

        app_logger.info(
            f"Data cleaning and transformation completed. Exported to file:\n"
            f"{export_file_path}")
    except Exception as e:
        app_logger.error(e)


app_logger.info("Program finished")


def data_ingestion(fleet_data_path, maintenance_data_path):
    try:
        df_fleet = ingestion.read_csv_as_dataframes(fleet_data_path)
        df_maintenance = ingestion.read_csv_as_dataframes(
            maintenance_data_path)
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


def data_quality_assessment(fleet, maintenance):
    log_duplicates(fleet)
    log_duplicates(maintenance)

    log_missing_vals(fleet)
    log_missing_vals(maintenance)

    log_missing_fleet_truck_ids(maintenance, fleet)


def log_duplicates(df):
    nbr_of_duplicates = quality_checks.count_full_duplicates(df)
    dq_logger.warning(
        f"Duplicate records found for {df.name} data: {nbr_of_duplicates}")


def log_missing_vals(df):
    counters = quality_checks.count_missing_val_per_col(df)
    if not counters.empty:
        dq_logger.warning(f"Missing data in {df.name}:")
        for key, value in counters.items():
            if value > 0:
                dq_logger.warning(f"   {key}: {value} missing values")


def log_missing_fleet_truck_ids(df1, df2):
    ids_only_in_df1_but_not_df2 = (
        quality_checks.get_items_existing_in_df1_only(
            df1, df2, "truck_id"))
    dq_logger.warning(
        f"Truck IDs missing from the fleet dataset: "
        f"{', '.join(map(str, ids_only_in_df1_but_not_df2))}")


def data_cleaning_transformation(fleet, maintenance):
    processed_fleet = (fleet.
                       pipe(processing.drop_duplicates).
                       pipe(processing.standardize_dates,
                            column_name="purchase_date"))

    processed_maintenance = (maintenance.
                             pipe(processing.drop_duplicates).
                             pipe(processing.standardize_dates,
                                  column_name="maintenance_date").
                             pipe(processing.standardize_text_lower_stripped,
                                  column_name="service_type").
                             pipe(processing.encode_one_hot,
                                  column_name="service_type").
                             pipe(processing.add_column_email_valid,
                                  column_name="technician_email"))

    return {
        "fleet": processed_fleet,
        "maintenance": processed_maintenance
    }


def data_integration(fleet, maintenance):
    merged_fleet_maintenance = processing.merge(
        fleet,
        maintenance,
        "truck_id")
    return merged_fleet_maintenance


if __name__ == "__main__":
    json_obj = load_json(JSON_CONFIG_DIR)
    fleet_data_path = f"{ROOT_PATH}{json_obj['fleet']["path"]}"
    maintenance_data_path = f"{ROOT_PATH}{json_obj['maintenance']["path"]}"
    export_file_path = f"{ROOT_PATH}{json_obj['export']["path"]}"
    run(fleet_data_path, maintenance_data_path, export_file_path)
