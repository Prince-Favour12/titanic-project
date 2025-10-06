import pandas as pd
import numpy as np
import os
import sys


from config.config import SavePathConfig
from utils.objects import load_object
from config.exception import CustomException

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            model_path = SavePathConfig.TRAINING_PIPELINE
            preprocessor_path = SavePathConfig.PREPROCESSOR_PIPELINE

            # Check if files exist
            if not os.path.exists(model_path) or not os.path.exists(preprocessor_path):
                raise FileNotFoundError(
                    f"Model or preprocessor not found. Please run training first."
                )

            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)

            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            return preds[0]

        except Exception as e:
            raise CustomException(e, sys)

        


class CustomData:
    def __init__(
            self,
            sex: str,
            age: int,
            sibsp: int,
            parch: int,
            fare: float,
            embarked: str,
            classes: str,
            identity: str,
            alone: int
    ):
        self.sex = sex
        self.age = age
        self.sibsp = sibsp
        self.parch = parch
        self.fare = fare
        self.embarked = embarked
        self.classes = classes,
        self.identity = identity,
        self.alone = alone

    def get_data_as_frame(self):
        try:
            custom_data_input = {
                "sex": [self.sex],
                "age": [self.age],
                "sibsp": [self.sibsp],
                "parch": [self.parch],
                "fare": [self.fare],
                "embarked": [self.embarked],
                "class": [self.classes],
                "identity": [self.identity],
                "alone": [self.alone]
            }

            return pd.DataFrame(custom_data_input)
        except Exception as e:
            raise CustomException(e, sys)