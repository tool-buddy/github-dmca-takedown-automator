"""
Configuration Loader for DMCA Takedown Requests

This module handles loading and validating DMCA takedown request
configurations from JSON files using Pydantic models.
"""

import json
from pathlib import Path
from typing import Union

from pydantic import ValidationError

from src.schemas import RequestConfig
from src.exceptions import ConfigError


def load_request_config(file_path: Union[str, Path]) -> RequestConfig:
    """
    Load and validate a DMCA config file.

    Args:
        file_path: Path to the JSON config file

    Returns:
        Validated RequestConfig object

    Raises:
        ConfigError: If there are issues with the config file
        ValidationError: If the config data fails validation
    """
    path = Path(file_path)

    # Check if file exists
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")

    # Check file extension
    if path.suffix.lower() != ".json":
        raise ConfigError(f"Config file must be JSON format: {path}")

    try:
        # Load JSON data
        with open(path, "r", encoding="utf-8") as f:
            config_data = json.load(f)

        return RequestConfig(**config_data)

    except ValidationError as e:
        raise ConfigError(
            f"Config validation failed: {e}"
        ) from e
    except json.JSONDecodeError as e:
        raise ConfigError(
            f"Invalid JSON format in config file: {e}", "format"
        ) from e
    except Exception as e:
        # Catch any other unexpected errors
        raise ConfigError(f"Error loading config file: {e}") from e
