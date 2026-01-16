"""Compatibility shim for legacy notebook imports.

Use ``src.components.data_transformation`` for the maintained implementation.
"""

from src.components.data_transformation import DataTransformation, DataTransformationConfig

__all__ = ["DataTransformation", "DataTransformationConfig"]
