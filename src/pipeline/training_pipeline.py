# src/pipeline/training_pipeline.py

import pandas as pd
import numpy as np
import sys

from prefect import flow
from config.logger import logging
from config.exception import CustomException

from src.components.data_ingestion import data_ingestion
from src.components.data_transformation import data_transformation
from src.components.train import trainer


@flow(name="TrainingPipeline")
def training_pipeline():
    try:
        logging.info("Starting Training Pipeline")

        train_path, test_path = data_ingestion()
        train_arr, test_arr = data_transformation(train_path, test_path)
        acc, classification = trainer(train_arr, test_arr)

        logging.info("Training Pipeline completed")

        return acc, classification
    except Exception as e:
        raise CustomException(e, sys)


if __name__ == "__main__":
    result = training_pipeline()
    print("Pipeline Result:", result)
