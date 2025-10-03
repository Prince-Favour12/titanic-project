import os
import sys
import pickle

from config.exception import CustomException
from config.logger import logging
from typing import List

def make_directories(paths: str|List[str]):
    """
    Create directories or folders for specific paths specified
    """
    try:
        if not isinstance(paths, str):
            for path in paths:
                os.makedirs(path, exist_ok= True)
                logging.info("Paths being created")
        else:
            os.makedirs(paths, exist_ok= True)
            logging.info("path created")

    except Exception as e:
        raise CustomException(e, sys)
    
def save_object(file_path, obj):
    try:
        if not os.path.exists(file_path):
            logging.error("File doesn't exist")

        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)

        logging.info("File saved successfully...")

    except Exception as e:
        raise CustomException(e, sys)