import pandas as pd
import numpy as np
import os
import sys


from config.config import SavePathConfig
from config.exception import CustomException
from dataclasses import dataclass
from config.logger import logging
from sklearn.model_selection import train_test_split
from utils.objects import make_directories

@dataclass
class DataIngestionConfig:
    raw_data_path: str = SavePathConfig.DATA_PATH
    train_data_path: str = SavePathConfig.TRAIN_DATA_PATH
    test_data_path: str = SavePathConfig.TEST_DATA_PATH


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initailize_data_ingestion(self):
        try:
            logging.info("Reading Data from path: {}".format(self.ingestion_config.raw_data_path))
            df = pd.read_csv(self.ingestion_config.raw_data_path)
            logging.info("Successfully read Data from path: {}".format(self.ingestion_config.raw_data_path))

            logging.info("Splitting Data")
            train_data, test_data = train_test_split(df, test_size= 0.2, random_state= 42)
            logging.info("Split completed successfully")

            logging.info("Saving data")
            
            make_directories(
                [
                    self.ingestion_config.train_data_path,
                    self.ingestion_config.test_data_path
                ]
            )

            train_data.to_csv(self.ingestion_config.train_data_path, index = False)

            test_data.to_csv(self.ingestion_config.test_data_path, index = False)

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        
        except Exception as e:
            raise CustomException(e, sys)