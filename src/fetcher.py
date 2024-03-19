"""Asynchronous stock quotes fetching module.

Asynchronous stock quotes fetching module with an abstract base class and a concrete
implementation utilizing an AsyncAPIClient.
"""

import json
import logging
from abc import ABC, abstractmethod
from typing import Any

from toolkit.api import AsyncAPIClient

logger = logging.getLogger(__name__)


class StockQuotesFetcherInterface(ABC):
    """Abstract base class for asynchronously fetching stock quotes."""

    @abstractmethod
    async def fetch_stock_quote(
        self, endpoint: str, operation: str, symbol: str
    ) -> dict[str, Any]:
        """
        Asynchronously fetches the stock quote for the given symbol.

        Parameters
        ----------
        endpoint : str
            The API endpoint.
        operation : str
            The function used in query params.
        symbol : str
            The stock symbol for which the quote needs to be fetched.

        Returns
        -------
        dict[str, Any]
            A dictionary containing the fetched stock quote information.
        """


class StockQuotesFetcher(StockQuotesFetcherInterface):
    """Concrete implementation of StockQuotesFetcherInterface."""

    def __init__(self, api_client: AsyncAPIClient, api_key: str) -> None:
        """Initialize the StockQuotesFetcher with the provided AsyncAPIClient."""
        self._client = api_client
        self._api_key = api_key

    async def fetch_stock_quote(
        self, endpoint: str, operation: str, symbol: str
    ) -> Any:
        """
        Asynchronously fetch the stock quote for the given symbol.

        Parameters
        ----------
        endpoint : str
            The API endpoint.
        operation : str
            The function used in query params.
        symbol : str
            The stock symbol for which the quote needs to be fetched.

        Returns
        -------
        Any
            An object containing the fetched stock quote information.
        """
        params = self._construct_params(operation=operation, symbol=symbol)

        response = await self._client.get(endpoint=endpoint, params=params)
        logger.info(
            "Successfully fetched API: %s %s",
            response.status_code,
            response.request.url,
        )

        try:
            return response.json()
        except json.JSONDecodeError as error:
            logger.error(
                "Failed to parse JSON: error: %s, content: %s",
                error,
                response.text[:30],
            )
            raise
        except Exception as error:
            logger.critical("An unexpected error occurred: %s", error, exc_info=True)
            raise

    def _construct_params(self, operation: str, symbol: str) -> dict[str, str]:
        """
        Construct the parameters for the API request.

        Parameters
        ----------
        operation : str
            The function used in query params.
        symbol : str
            The stock symbol for which the parameters are constructed.

        Returns
        -------
        dict[str, str]
            A dictionary containing the constructed parameters.
        """
        params = {"apikey": self._api_key, "function": operation, "symbol": symbol}
        return params
