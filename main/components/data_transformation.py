import os
import sys 
from dataclass import dataclass

import numpy as np
import pandas as pd 

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.utils.exception import CustomException
from src.utils.logger import logging 

@dataclass
class DataTransformationConfig:
    preprocessor_ob_file_path=os.path.join('artifacts', 'preprocessor.pk1')

class DataTransforamtion:
    def __init__(self):
        self.data_transformation_config = DataTransforamtionConfig()

    def get_data_transformer_object(self):
        try:
            numerical_column = ["writing_score", "reading_score"]
            categorical_column =["gender", "race_ethnicity","parental_level_of_education", "lunch", "test_preparation_course"]

            num_pipeline=Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy='median')), 
                    ("scaler", StandardScaler())
                ]
            )
            cat_pipeline=Pipeline(
                    steps = [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("one_hot_encoder", OneHotEncoder()),
                        ("scaler", StandardScaler())

                    ]

            )

            logging.info(f"Categorical columns encoding completed :{categorical_column} ")
            logging.info(f"Numerical columns standard scaling completed :{numerical_column}")

            preprocessor = ColumnTransformer(

                [
                    ("num_pipeline", num_pipeline, numerical_column),
                    ("cat_pipeline", cat_pipeline, categorical_column)
                ]
            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)


             