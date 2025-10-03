import pandas as pd
import numpy as np
import os
import sys


from config.config import SavePathConfig
from config.exception import CustomException
from dataclasses import dataclass
from config.logger import logging
from utils.objects import make_directories, save_object
from utils.train import evaluate_model, return_classification_report
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import (
    RandomForestClassifier,
    AdaBoostClassifier,
    GradientBoostingClassifier
)

from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from utils.mlflow_tracker import MLFlowTracker


@dataclass
class TrainConfig:
    train_path = SavePathConfig.TRAINING_PIPELINE



class TrainingData:
    def __init__(self):
        self.train_config = TrainConfig()
        self.mlflow_tracker = MLFlowTracker()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Split training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            models = {
                "Random Forest": RandomForestClassifier(),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(),
                "Logistic Classifier": LogisticRegression(),
                "K-Neighbours Classifier": KNeighborsClassifier(),
                "XGBRegressor": XGBClassifier(),
                "CatBoosting Classifier": CatBoostClassifier(verbose=False),
                "AdaBoost Classifier": AdaBoostClassifier()
            }

            # Evaluate all models
            model_report: dict = evaluate_model(X_train=X_train, y_train=y_train, 
                                                X_test=X_test, y_test=y_test, models=models)

            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No best model found", sys)
            logging.info("Best found model on both training and testing dataset")

            # Save best model
            make_directories(self.train_config.train_path)
            save_object(file_path=self.train_config.train_path, obj=best_model)

            predicted = best_model.predict(X_test)
            accuracy = accuracy_score(y_test, predicted)

            # === Log to MLflow ===
            for model_name, score in model_report.items():
                model = models[model_name]
                params = model.get_params() if hasattr(model, "get_params") else {}
                metrics = {"accuracy": score}
                self.mlflow_tracker.log_model(
                    model_name=model_name,
                    model=model,
                    params=params,
                    metrics=metrics,
                    tags={"pipeline": "classification", "stage": "training"}
                )

            return accuracy, return_classification_report(y_test, predicted)

        except Exception as e:
            raise CustomException(e, sys)
