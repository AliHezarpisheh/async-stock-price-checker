"""Module defining constants for the AlphaVantage API and messages for the app view."""

from enum import StrEnum


class AlphaVantageAPIConsts(StrEnum):
    """Constants for the AlphaVantage API."""

    BASE_URL = "https://www.alphavantage.co"
    ENDPOINT = "/query"
    OPERATION = "GLOBAL_QUOTE"


class ViewMessages(StrEnum):
    """Messages for the application view."""

    WELCOME_MESSAGE = """
[bold magenta]
    ╔══════════════════════════════╗
    ║   Welcome to the Async Stock ║
    ║      Price Checker 📈🚀      ║
    ╚══════════════════════════════╝
[/bold magenta]
[bold cyan]Instructions:[/bold cyan]
- Enter the stock symbols you want to check.
- Separate multiple symbols with commas.

For example: [italic]AAPL, GOOGL, MSFT[/italic]

[bold cyan]Get started by entering your symbols below:[/bold cyan]
"""
    DIVIDER = "[dim]\u2500" * 50 + "[/dim]"
    INTERNAL_ERROR = (
        "[bold red]Error: Internal error. Please contact support.[/bold red]\n"
    )
    EXTERNAL_ERROR = (
        "[bold red]Error: External service error. Please try again later."
        "[/bold red]\n"
    )
    SYMBOL_RETRIEVAL = "Enter stock symbols (comma-separated): "
