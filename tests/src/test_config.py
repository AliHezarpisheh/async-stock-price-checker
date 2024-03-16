"""Module to test the functionality of the get_api_key function."""

import os
from typing import Generator

import pytest

from src.config import get_api_key


@pytest.fixture
def mock_api_key() -> Generator[str, None, None]:
    """Fixture to mock the API key.

    Yields
    ------
    str
        A mock API key.

    Raises
    ------
    AssertionError
        If the API key is not valid or missing.
    """
    mock_api_key = "mock_api_key"
    os.environ["ALPHAVANTAGE_API_KEY"] = mock_api_key
    yield mock_api_key
    del os.environ["ALPHAVANTAGE_API_KEY"]


@pytest.mark.smoke
def test_get_valid_api_key(mock_api_key: str) -> None:
    """Test case to validate retrieving a valid API key.

    Parameters
    ----------
    mock_api_key : str
        Mock API key.
    """
    api_key = get_api_key()
    assert api_key == mock_api_key


def test_get_missing_api_key() -> None:
    """Test case to validate handling missing API key.

    Raises
    ------
    ValueError
        If the API key is missing.
    """
    if "ALPHAVANTAGE_API_KEY" in os.environ:
        del os.environ["ALPHAVANTAGE_API_KEY"]

    with pytest.raises(ValueError):
        get_api_key()
