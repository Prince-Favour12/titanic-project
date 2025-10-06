from dotenv import load_dotenv
import os

load_dotenv()

class DataBaseConfig:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DATABASE_NAME: str = os.getenv("DB_NAME")
    DB_COLLECTION_NAME: str = os.getenv("DB_COLLECTION")

class SavePathConfig:
    DATA_PATH: str = os.getenv("DATA_PATH")
    TEST_DATA_PATH: str = os.getenv("TEST_DATA_PATH")
    TRAIN_DATA_PATH: str = os.getenv("TRAIN_DATA_PATH")
    ARTIFACT_DIR = "artifact"
    TRAINING_PIPELINE = os.path.join(ARTIFACT_DIR, "train_model.pkl")
    PREPROCESSOR_PIPELINE = os.path.join(ARTIFACT_DIR, "preprocessor.pkl")

class MlflowConfig:
    MLFLOW_TRACKING_URI: str = os.getenv("MLFLOW_TRACKING_URI")
    MLFLOW_EXPERIMENT_NAME: str = os.getenv("MLFLOW_EXPERIMENT_NAME")