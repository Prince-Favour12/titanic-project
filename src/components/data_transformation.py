# src/components/data_transformation.py

import pandas as pd
import numpy as np
import os
import sys


from config.config import SavePathConfig
from config.exception import CustomException
from dataclasses import dataclass
from config.logger import logging
from utils.objects import make_directories, save_object
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from prefect import task


@dataclass
class DataTransformationConfig:
    preprocessor_path = SavePathConfig.PREPROCESSOR_PIPELINE


class DataTransformation:
    def __init__(self):
        self.transformation_config = DataTransformationConfig()

    def get_prepocessor_instance(self):
        try:
            categorical_features = ['sex', 'embarked', 'class', 'identity']
            numerical_features = ['age', 'sibsp', 'parch', 'fare', 'alone']
            num_pipeline = Pipeline(
                steps= [
                    ('scaler', StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps= [
                    ('one_hot_encoder', OneHotEncoder(sparse_output= False)),
                    ('scaler', StandardScaler())
                ]
            )
            logging.info("Numerical columns scaling completed")
            logging.info("Categorical columns encoding completed")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_features),
                    ("cat_pipeline", cat_pipeline, categorical_features)
                ]
            )

            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):

        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Read train and test data completed")

            logging.info("obtaining preprocessing object")

            preprocessing_obj = self.get_prepocessor_instance()

            target_column_name = "survived"

            input_feature_train_df = train_df.drop(target_column_name, axis= 1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(target_column_name, axis= 1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe"
            )

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)

            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]

            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            logging.info("Saved preprocessing object.")

            make_directories(
                self.transformation_config.preprocessor_path
            )


            save_object(

                file_path = self.transformation_config.preprocessor_path,
                obj = preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.transformation_config.preprocessor_path
            )
        except Exception as e:
            raise CustomException(e,sys)


@task
def data_transformation(train_path, test_path):
    try:
        transformation = DataTransformation()
        train_arr, test_arr, _ = transformation.initiate_data_transformation(train_path, test_path)
        return train_arr, test_arr
    except Exception as e:
        raise CustomException(e, sys)
