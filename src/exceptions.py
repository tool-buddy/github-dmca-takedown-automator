"""
Exception classes for the DMCA Takedown Automator

This module defines custom exception classes for different types of errors
that can occur during the DMCA takedown process.
"""

from typing import Optional, Dict, Any


class DMCAError(Exception):
    """Base exception class for all DMCA takedown automator errors."""


class ConfigError(DMCAError):
    """Exception for configuration related errors."""

    def __init__(self, message: str, field: Optional[str] = None) -> None:
        """
        Initialize a ConfigError with an error message and optional field name.

        Args:
            message: Description of the error
            field: Name of the field with the error, if applicable
        """
        super().__init__(message)
        self.field = field


class EmailError(DMCAError):
    """Exception for email related errors."""

    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize an EmailError with an error message and optional context information.

        Args:
            message: Description of the error
            context: Additional context information about the error
        """
        super().__init__(message)
        self.context = context or {}
