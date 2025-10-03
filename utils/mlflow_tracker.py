# utils/mlflow_tracker.py

import mlflow
import mlflow.sklearn
from datetime import datetime

from config.config import MlflowConfig

class MLFlowTracker:
    def __init__(self, experiment_name: str = MlflowConfig.MLFLOW_EXPERIMENT_NAME):
        """
        Initialize MLflow tracker with an experiment name.
        """
        mlflow.set_tracking_uri(MlflowConfig.MLFLOW_TRACKING_URI)  # Change if remote server
        mlflow.set_experiment(experiment_name)

    def log_model(self, model_name: str, model, params: dict, metrics: dict, tags: dict = None):
        """
        Logs model, parameters, metrics, and optional tags into MLflow.
        """
        with mlflow.start_run(run_name=model_name + "_" + datetime.now().strftime("%Y%m%d_%H%M%S")):
            # Log parameters
            mlflow.log_params(params)

            # Log metrics
            mlflow.log_metrics(metrics)

            # Log tags if provided
            if tags:
                mlflow.set_tags(tags)

            # Log the model itself
            mlflow.sklearn.log_model(model, artifact_path=model_name.replace(" ", "_"))
            
            print(f"[MLflow] Logged {model_name} with accuracy: {metrics.get('accuracy')}")
