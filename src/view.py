"""Module defining the View class for the financial data fetching and presentation app.

Module includes the View class, which is responsible for displaying information to the
user using the rich library.
"""

from rich.console import Console
from rich.table import Table

from .enums import ViewMessages
from .model import StockQuote


class View:
    """Class representing the view in the app."""

    def __init__(self) -> None:
        """Initialize the View class with a rich console."""
        self.console = Console()

    def show_divider(self) -> None:
        """Display a divider line."""
        self.console.print(ViewMessages.DIVIDER)

    def welcome(self) -> None:
        """Display the welcome message."""
        self.console.clear()
        self.console.print(ViewMessages.WELCOME_MESSAGE)
        self.show_divider()

    def show_stock_quotes(self, stock_quotes: list[StockQuote]) -> None:
        """Display stock quotes in a rich table.

        Parameters
        ----------
        - stock_quotes : list[StockQuote]:
            List of StockQuote objects to display.
        """
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Symbol", style="cyan", justify="center")
        table.add_column("Open", style="green", justify="center")
        table.add_column("High", style="green", justify="center")
        table.add_column("Low", style="green", justify="center")
        table.add_column("Price", style="green", justify="center")
        table.add_column("Volume", style="green", justify="center")
        table.add_column("Latest Trading Day", style="green", justify="center")
        table.add_column("Previous Close", style="green", justify="center")
        table.add_column("Change", style="green", justify="center")
        table.add_column("Change Percent", style="green", justify="center")

        for quote in stock_quotes:
            change_percent = (
                float(quote.change_percent[:-1])
                if quote.change_percent.endswith("%")
                else float(quote.change_percent)
            )

            table.add_row(
                quote.symbol,
                f"${float(quote.open):,.2f}",
                f"${float(quote.high):,.2f}",
                f"${float(quote.low):,.2f}",
                f"${float(quote.price):,.2f}",
                f"{int(quote.volume):,}",
                f"{quote.latest_trading_day}",
                f"${float(quote.previous_close):,.2f}",
                f"${float(quote.change):,.2f}",
                f"{float(change_percent):,.2f}%",
            )

        self.console.clear()
        self.console.print(table)
        self.show_divider()

    def show_external_service_error(self) -> None:
        """Display an external service error message."""
        self.console.clear()
        self.console.print(ViewMessages.EXTERNAL_ERROR)
        self.show_divider()

    def show_internal_error(self) -> None:
        """Display an internal error message."""
        self.console.clear()
        self.console.print(ViewMessages.INTERNAL_ERROR)
        self.show_divider()

    def get_symbols(self) -> str:
        """Get user input for stock symbols."""
        return self.console.input(ViewMessages.SYMBOL_RETRIEVAL)
