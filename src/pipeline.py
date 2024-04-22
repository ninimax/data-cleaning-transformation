"""
Main entry point of the program for data cleaning and transformation.
"""
import ingestion
from logger import *

application_logger = get_logger(__name__, LoggerType.APPLICATION)

if __name__ == "__main__":
    application_logger.info("Program started\n")

# data ingestion
application_logger.info("***START OF DATA INGESTION***")
try:
    fleet_information = ingestion.read_data('../data/fleet_information.csv')
    maintenance_records = ingestion.read_data('../data/maintenance_records.csv')
except FileNotFoundError as e:
    application_logger.exception(e)
application_logger.info("***END OF DATA INGESTION***\n")

# date cleaning
application_logger.info("***START OF DATA CLEANING***")
application_logger.info("***END OF DATA CLEANING***\n")

# data transformation
application_logger.info("***START OF DATA TRANSFORMATION***")
application_logger.info("***END OF DATA TRANSFORMATION***\n")

application_logger.info("Program finished")
