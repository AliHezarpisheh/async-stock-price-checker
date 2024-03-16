"""Module defining the Presenter class.

This module includes the Presenter class, which handles the updating of the model and
view based on user input and external data fetching.
"""

import asyncio
import logging
from typing import Any

from .enums import AlphaVantageAPIConsts as AVAPIConsts
from .fetcher import StockQuotesFetcher
from .model import Model, StockQuote
from .view import View

logger = logging.getLogger(__name__)


class Presenter:
    """Presenter for the financial data fetching and presentation application."""

    def __init__(self, view: View, model: Model, fetcher: StockQuotesFetcher) -> None:
        """Initialize the Presenter with references to the View, Model, and Fetcher.

        Parameters
        ----------
        view : View
            The application view.
        model : Model
            The application model.
        fetcher : StockQuotesFetcher
            The fetcher for stock quotes.
        """
        self._view = view
        self._model = model
        self._fetcher = fetcher

    async def update_model(self) -> None:
        """Update the model based on user input and external data fetching.

        This method retrieves user input for stock symbols, fetches stock quotes
        asynchronously, and updates the model accordingly.
        """
        symbols_string = self._view.get_symbols()
        symbols_list = self._split_symbols(symbols_string=symbols_string)
        stock_data = await self._fetch_stock_quotes(symbols_list=symbols_list)
        self._handle_stock_quote_addition(stock_data=stock_data)

    def update_view(self) -> None:
        """Update the view based on the current state of the model.

        This method updates the view with the latest stock quotes from the model.
        """
        stock_quotes = self._model.stock_quotes
        self._view.show_stock_quotes(stock_quotes=stock_quotes)

    async def _fetch_stock_quotes(self, symbols_list: list[str]) -> Any:
        """Fetch stock quotes asynchronously for the given list of symbols.

        Parameters
        ----------
        symbols_list : list
            List of stock symbols.

        Returns
        -------
        Any
            An object containing stock quote data.
        """
        tasks = [
            self._fetcher.fetch_stock_quote(
                endpoint=AVAPIConsts.ENDPOINT,
                operation=AVAPIConsts.OPERATION,
                symbol=symbol,
            )
            for symbol in symbols_list
        ]

        return await asyncio.gather(*tasks)

    def _handle_stock_quote_addition(self, stock_data: list[dict[str, Any]]) -> None:
        """Handle the addition of stock quotes to the model.

        This method processes the fetched stock data, creates StockQuote instances,
        and adds them to the model.

        Parameters
        ----------
        stock_data : list
            List of dictionaries containing stock quote data.
        """
        self._model.remove_all_stock_quotes()
        for json_stock_quote in stock_data:
            try:
                json_stock_quote = self._prepare_stock_data(json_stock_quote)
                stock_quote = StockQuote(**json_stock_quote)
                self._model.add_stock_quote(stock_quote=stock_quote)
            except (TypeError, ValueError) as error:
                logger.error("Error creating StockQuote instance: %s", error)
                self._view.show_external_service_error()
            except Exception as error:
                logger.critical("Unexpected error occurred: %s", error, exc_info=True)
                self._view.show_internal_error()

    def _prepare_stock_data(self, stock_data: dict[str, Any]) -> dict[str, Any]:
        """Prepare stock data by extracting relevant information.

        Parameters
        ----------
        stock_data : dict
            Dictionary containing raw stock data.

        Returns
        -------
        dict
            Dictionary containing processed stock data.
        """
        try:
            symbol_data = stock_data["Global Quote"]
            valid_stock_data = {
                key.split(". ")[1].replace(" ", "_"): value
                for key, value in symbol_data.items()
            }
            return valid_stock_data
        except KeyError as error:
            logger.error(
                "Global Quote is not present in the response, Error: %s", error
            )
            self._view.show_external_service_error()
            return {}

    def _split_symbols(self, symbols_string: str) -> list[str]:
        """Split a comma-separated string of symbols into a list.

        Parameters
        ----------
        symbols_string : str
            Comma-separated string of stock symbols.

        Returns
        -------
        list
            List of stock symbols.
        """
        symbols_list = [symbol.strip() for symbol in symbols_string.split(",")]
        return symbols_list
