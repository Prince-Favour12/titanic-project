# utils/objects.py

import os
import sys
import pickle

from config.exception import CustomException
from config.logger import logging
from typing import List

def make_directories(paths: str | List[str]):
    """
    Create directories for the given path(s). 
    If the path includes a file (e.g., artifacts/train_data.csv),
    it creates only the parent directory, not an extra folder for the file.
    """
    try:
        if isinstance(paths, str):
            paths = [paths]  

        for path in paths:
            dir_path = path if os.path.splitext(path)[1] == "" else os.path.dirname(path)
            
            if dir_path:  
                os.makedirs(dir_path, exist_ok=True)
                logging.info(f"Directory created or already exists: {dir_path}")

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
    

def load_object(file_path):
    try:
        if not os.path.exists(file_path):
            logging.error("File doesn't exist")
        
        with open(file_path, 'rb') as file_obj:
            results = pickle.load(file_obj)

        return results
    except Exception as e:
        raise CustomException(e, sys)