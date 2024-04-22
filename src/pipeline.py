"""
Main entry point of the program for data cleaning and transformation.
"""
import json

import ingestion
from logger import *

application_logger = get_logger(__name__, LoggerType.APPLICATION)

JSON_CONFIG_DIR = "../config/data_sources.json"


def load_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def run():
    fleet_information = None
    maintenance_records = None

    application_logger.info("Program started\n")

    # read config
    data_resources = load_json(JSON_CONFIG_DIR)

    # data ingestion
    application_logger.info("***START OF DATA INGESTION***")
    try:
        fleet_information = ingestion.read_data(data_resources["fleet"]["path"])
        maintenance_records = ingestion.read_data(data_resources["fleet"]["path"])
    except FileNotFoundError as e:
        application_logger.exception(e)
    application_logger.info("***END OF DATA INGESTION***\n")

    # data cleaning
    application_logger.info("***START OF DATA CLEANING***")
    application_logger.info("***END OF DATA CLEANING***\n")

    # data transformation
    application_logger.info("***START OF DATA TRANSFORMATION***")
    application_logger.info("***END OF DATA TRANSFORMATION***\n")

    application_logger.info("Program finished")


if __name__ == "__main__":
    run()
