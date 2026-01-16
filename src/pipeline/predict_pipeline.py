"""Prediction pipeline used by the Flask app."""

from __future__ import annotations

import os
import sys
from typing import Any

import pandas as pd

from src.utils.exception import CustomException
from src.utils.logger import logging
from src.utils.utils import load_object


class PredictPipeline:
    """Loads preprocessing/model artifacts and generates predictions."""

    def __init__(self):
        pass

    def predict(self, features: pd.DataFrame) -> Any:
        """Return model predictions for the provided features."""
        try:
            model_path=os.path.join("artifacts","model.pkl")
            preprocessor_path=os.path.join('artifacts','preprocessor.pkl')
            
            logging.info("Loading model and preprocessor artifacts.")
            
            model=load_object(file_path=model_path)

            preprocessor=load_object(file_path=preprocessor_path)
            
            data_scaled=preprocessor.transform(features)
            preds=model.predict(data_scaled)
            return preds
        
        except Exception as e:
            raise CustomException(e, sys.exc_info()) from e



class CustomData:
    """Container for user input that can be converted into a DataFrame."""

    def __init__(  self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education,
        lunch: str,
        test_preparation_course: str,
        reading_score: int,
        writing_score: int):

        self.gender = gender

        self.race_ethnicity = race_ethnicity

        self.parental_level_of_education = parental_level_of_education

        self.lunch = lunch

        self.test_preparation_course = test_preparation_course

        self.reading_score = reading_score

        self.writing_score = writing_score

    def get_data_as_data_frame(self) -> pd.DataFrame:
        """Convert the captured inputs into a pandas DataFrame."""
        try:
            custom_data_input_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys.exc_info()) from e
