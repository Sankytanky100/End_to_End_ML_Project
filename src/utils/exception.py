"""Custom exception helpers used across the ML pipeline."""

from __future__ import annotations

from typing import Tuple


def error_message_detail(error: Exception | str, error_detail: Tuple[object, object, object]) -> str:
    """Build a rich error message that includes the filename and line number.

    Args:
        error: The original exception or a message string.
        error_detail: The tuple returned by ``sys.exc_info()``.

    Returns:
        A formatted error message string.
    """
    _, _, exc_tb = error_detail
    if exc_tb is None:
        return f"Error occurred: {error}"

    file_name = exc_tb.tb_frame.f_code.co_filename
    return (
        "Error occurred in python script name "
        f"[{file_name}] line number [{exc_tb.tb_lineno}] error message[{error}]"
    )


class CustomException(Exception):
    """Exception that enriches errors with file and line information."""

    def __init__(self, error: Exception | str, error_detail: Tuple[object, object, object]) -> None:
        super().__init__(str(error))
        self.error_message = error_message_detail(error, error_detail=error_detail)

    def __str__(self) -> str:
        return self.error_message
