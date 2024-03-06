"""Configuration module for Alpha Vantage API keys and environment variables."""

import logging
import os

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()


def get_api_key() -> str:
    """
    Retrieve the Alpha Vantage API key from the environment variables.

    Preconditions
    -------------
    - The `ALPHAVANTAGE_API_KEY` environment variable is expected to contain API key.

    Postconditions
    --------------
    - If successful, returns the Alpha Vantage API key as a string.

    Raises
    ------
    ValueError
        If the `ALPHAVANTAGE_API_KEY` environment variable is not set.
    TypeError
        If the retrieved API key is not a string.

    Returns
    -------
    str
        The Alpha Vantage API key.
    """
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")

    if api_key is None:
        msg = "`ALPHAVANTAGE_API_KEY` is not set in the environment!"
        logger.warning(msg)
        raise ValueError(msg)

    if not isinstance(api_key, str):
        raise TypeError("API key must be a string.")

    logger.debug("Alpha Vantage API key retrieved successfully.")
    return api_key
