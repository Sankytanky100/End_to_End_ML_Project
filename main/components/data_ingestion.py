"""Compatibility shim for legacy imports.

Use ``src.components.data_ingestion`` for the maintained implementation.
"""

from src.components.data_ingestion import DataIngestion, DataIngestionConfig

__all__ = ["DataIngestion", "DataIngestionConfig"]
