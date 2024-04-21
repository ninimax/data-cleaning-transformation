import ingestor
from logger import *

if __name__ == "__main__":
    application_logger = get_logger(__name__, LoggerType.APPLICATION)

    application_logger.info("Program started")
    fleet_information = ingestor.read_data('../data/fleet_information.csv')
    maintenance_records = ingestor.read_data('../data/maintenance_records.csv')

    # print(fleet_information.head(6))
    application_logger.info("Program finished")
