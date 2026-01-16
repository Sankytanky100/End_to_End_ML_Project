"""Utility helpers for serialization and model evaluation."""

from __future__ import annotations

import os
import sys
from typing import Any, Dict

import dill
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.utils.exception import CustomException


def save_object(obj: Any, file_path: str) -> None:
    """Serialize and save a Python object to disk.

    Args:
        obj: The object to serialize.
        file_path: Destination path for the serialized object.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys.exc_info()) from e


def evaluate_models(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    models: Dict[str, Any],
    param: Dict[str, Dict[str, list]],
) -> Dict[str, float]:
    """Run grid search for each model and return test scores.

    Args:
        X_train: Training features.
        y_train: Training labels.
        X_test: Test features.
        y_test: Test labels.
        models: Model name to estimator mapping.
        param: Model name to grid search parameters mapping.

    Returns:
        A mapping of model names to R2 test scores.
    """
    try:
        report: Dict[str, float] = {}

        for model_name, model in models.items():
            grid_params = param.get(model_name, {})
            gs = GridSearchCV(model, grid_params, cv=3)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys.exc_info()) from e


def load_object(file_path: str) -> Any:
    """Load a serialized object from disk."""
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys.exc_info()) from e
