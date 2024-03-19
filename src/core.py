"""Module providing an asynchronous financial data fetching and presentation app.

This module includes the main asynchronous function for running a financial data
fetching and presentation application. It utilizes the AlphaVantage API for retrieving
stock quotes.
"""

import logging

from toolkit.api import AsyncAPIClient

from .config import get_api_key
from .enums import AlphaVantageAPIConsts as AVAPIConsts
from .fetcher import StockQuotesFetcher
from .model import Model
from .presenter import Presenter
from .view import View

logger = logging.getLogger(__name__)


async def main() -> None:  # pragma: no cover
    """
    Initialize the main asynchronous function for the application.

    This function initializes the necessary components such as the model, view,
    API client, fetcher, and presenter. It then enters a loop where the model is updated
    asynchronously, and the view is updated accordingly.
    """
    model = Model()
    view = View()

    api_key = get_api_key()
    api_client = AsyncAPIClient(base_url=AVAPIConsts.BASE_URL)
    fetcher = StockQuotesFetcher(api_client=api_client, api_key=api_key)

    presenter = Presenter(model=model, view=view, fetcher=fetcher)

    view.welcome()
    logger.debug("Application Has been Started.")
    while True:
        await presenter.update_model()
        presenter.update_view()
