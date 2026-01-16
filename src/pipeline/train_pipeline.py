"""Training pipeline that orchestrates ingestion, transformation, and training."""

from __future__ import annotations

from typing import Tuple

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.utils.logger import logging


class TrainPipeline:
    """End-to-end training pipeline entry point."""

    def run(self) -> Tuple[str, str, float]:
        """Run ingestion, transformation, and training steps.

        Returns:
            The train artifact path, test artifact path, and best model R2 score.
        """
        logging.info("Starting the training pipeline.")
        train_path, test_path = DataIngestion().initiate_data_ingestion()
        train_arr, test_arr, _ = DataTransformation().initiate_data_transformation(
            train_path, test_path
        )
        r2_score = ModelTrainer().initiate_model_trainer(train_arr, test_arr)
        logging.info("Training pipeline completed.")
        return train_path, test_path, r2_score


if __name__ == "__main__":
    TrainPipeline().run()
