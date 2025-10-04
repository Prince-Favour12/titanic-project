# utils/train.py

import pandas as pd
import numpy as np
import os
import sys

from config.logger import logging
from config.exception import CustomException

from sklearn.metrics import accuracy_score, classification_report

def evaluate_model(X_train, y_train, X_test, y_test, models):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]

            model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = accuracy_score(y_train, y_train_pred)

            test_model_score = accuracy_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report
    
    except Exception as e:
        raise CustomException(e, sys)
    
def return_classification_report(y_true, y_pred):
    try:
        return classification_report(y_true, y_pred)
    except Exception as e:
        raise CustomException(e, sys)