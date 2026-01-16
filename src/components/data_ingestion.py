"""Data ingestion component for the student performance dataset."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split

from src.utils.exception import CustomException
from src.utils.logger import logging
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainer
from src.components.model_trainer import ModelTrainerConfig


@dataclass
class DataIngestionConfig:
    """File paths used by the ingestion step."""

    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")
    raw_data_path: str = os.path.join("artifacts", "data.csv")

class DataIngestion:
    """Loads raw data and writes train/test artifacts to disk."""

    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self) -> Tuple[str, str]:
        """Execute data ingestion and return artifact paths."""
        logging.info("Entered the data ingestion method or component")
        try:
            df = pd.read_csv(os.path.join("notebook", "data", "stud.csv"))
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train Test Split Initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)

            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of the data is completed")

            return (self.ingestion_config.train_data_path, self.ingestion_config.test_data_path)
        except Exception as e:
            error_msg = f"Error occurred during data ingestion: {e}"
            logging.error(error_msg)
            raise CustomException(error_msg, sys.exc_info()) from e

if __name__ == "__main__":
    obj = DataIngestion()
    # Assign default values to paths
    train_data, test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data)

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))
