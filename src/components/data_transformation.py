"""Data transformation component for feature preprocessing."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.utils.exception import CustomException
from src.utils.logger import logging 
from src.utils.utils import save_object 

@dataclass
class DataTransformationConfig:
    """Configuration for data transformation artifacts."""

    preprocessor_ob_file_path: str = os.path.join("artifacts", "preprocessor.pkl")

class DataTransformation:
    """Builds preprocessing pipelines and applies them to datasets."""

    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self) -> ColumnTransformer:
        """Create the preprocessing pipeline for numerical and categorical features."""
        try:
            numerical_column = ["writing_score", "reading_score"]
            categorical_column = ["gender", "race_ethnicity", "parental_level_of_education", "lunch", "test_preparation_course"]

            num_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy='median')), 
                ("scaler", StandardScaler())
            ])

            cat_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder", OneHotEncoder(handle_unknown="ignore")),
            ])

            logging.info(f"Categorical columns encoding completed: {categorical_column}")
            logging.info(f"Numerical columns standard scaling completed: {numerical_column}")

            preprocessor = ColumnTransformer(
                transformers=[
                    ("num_pipeline", num_pipeline, numerical_column),
                    ("cat_pipeline", cat_pipeline, categorical_column)
                ]
            )

            return preprocessor
        
        except Exception as e:
            raise CustomException("Error occurred while creating data transformer object", sys.exc_info()) from e
    
    def initiate_data_transformation(self, train_path: str, test_path: str) -> Tuple[np.ndarray, np.ndarray, str]:
        """Apply preprocessing, save the transformer, and return arrays."""
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and Test data completed")
            logging.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = "math_score"
           
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessing object on training dataframe and testing dataframe")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]  

            
            logging.info("Saved preprocessing object")
            save_object(obj=preprocessing_obj, file_path=self.data_transformation_config.preprocessor_ob_file_path)
            return (train_arr, test_arr, self.data_transformation_config.preprocessor_ob_file_path)

        except Exception as e:
            raise CustomException("Error transforming data", sys.exc_info()) from e
