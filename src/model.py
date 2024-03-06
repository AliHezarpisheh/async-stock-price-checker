"""Module defining the Model class and the StockQuote dataclass."""

from dataclasses import dataclass


@dataclass(frozen=True)
class StockQuote:
    """Dataclass representing a stock quote."""

    symbol: str
    open: str
    high: str
    low: str
    price: str
    volume: str
    latest_trading_day: str
    previous_close: str
    change: str
    change_percent: str


class Model:
    """Representing the model of the financial data fetching and presentation app."""

    def __init__(self) -> None:
        """Initialize the Model with an empty list of stock quotes."""
        self.stock_quotes: list[StockQuote] = []

    def add_stock_quote(self, stock_quote: StockQuote) -> None:
        """Add a stock quote to the list of stock quotes.

        Parameters
        ----------
        stock_quote : StockQuote
            The stock quote to add.
        """
        self.stock_quotes.append(stock_quote)

    def remove_all_stock_quotes(self) -> None:
        """Remove all stock quotes from the list."""
        self.stock_quotes.clear()
