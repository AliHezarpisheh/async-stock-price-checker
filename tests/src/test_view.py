"""Module implementing a test suite for the View class."""

from unittest.mock import patch

import pytest
import rich

from src.enums import ViewMessages
from src.model import StockQuote
from src.view import View


@pytest.fixture(scope="module")
def view() -> View:
    """
    Fixture for initializing a View instance.

    Returns
    -------
    View
        An instance of the View class.
    """
    return View()


def test_show_divider(view: View) -> None:
    """
    Test for the show_divider method of the View class.

    Parameters
    ----------
    view : View
        An instance of the View class.
    """
    with patch("rich.console.Console.print") as mock_print:
        view.show_divider()

        mock_print.assert_called_once_with(ViewMessages.DIVIDER)


def test_welcome(view: View) -> None:
    """
    Test for the welcome method of the View class.

    Parameters
    ----------
    view : View
        An instance of the View class.
    """
    with patch.object(view.console, "print") as mock_print:
        view.welcome()

        first_call = mock_print.call_args_list[0]
        second_call = mock_print.call_args_list[1]
        assert mock_print.call_count == 2
        assert first_call[0][0] == ViewMessages.WELCOME_MESSAGE
        assert second_call[0][0] == ViewMessages.DIVIDER


@pytest.mark.parametrize(
    "stock_quotes",
    (
        [
            StockQuote(
                "AAPL",
                "123.45",
                "130.20",
                "120.30",
                "125.67",
                "1000000",
                "2024-03-15",
                "120.50",
                "5.17",
                "+4.32%",
            ),
            StockQuote(
                "GOOGL",
                "2000.00",
                "2050.00",
                "1990.00",
                "2025.50",
                "500000",
                "2024-03-15",
                "1998.75",
                "26.75",
                "+1.34%",
            ),
        ],
    ),
)
def test_show_stock_quotes(view: View, stock_quotes: list[StockQuote]) -> None:
    """
    Test for the show_stock_quotes method of the View class.

    Parameters
    ----------
    view : View
        An instance of the View class.
    stock_quotes : list[StockQuote]
        List of StockQuote objects.
    """
    with patch.object(view, "console") as mock_console:
        view.show_stock_quotes(stock_quotes)

        mock_console.clear.assert_called_once()

        print_first_call = mock_console.print.call_args_list[0]
        printed_table = print_first_call[0][0]

        assert isinstance(printed_table, rich.table.Table)
        expected_headers = [
            "Symbol",
            "Open",
            "High",
            "Low",
            "Price",
            "Volume",
            "Latest Trading Day",
            "Previous Close",
            "Change",
            "Change Percent",
        ]
        for index, header in enumerate(expected_headers):
            assert printed_table.columns[index].header == header

        print_second_call = mock_console.print.call_args_list[1]
        assert mock_console.print.call_count == 2
        assert print_second_call[0][0] == ViewMessages.DIVIDER


def test_show_external_service_error(view: View) -> None:
    """
    Test for the show_external_service_error method of the View class.

    Parameters
    ----------
    view : View
        An instance of the View class.
    """
    with patch("rich.console.Console.print") as mock_print:
        view.show_external_service_error()

        first_call = mock_print.call_args_list[0]
        second_call = mock_print.call_args_list[1]
        assert mock_print.call_count == 2
        assert first_call[0][0] == ViewMessages.EXTERNAL_ERROR
        assert second_call[0][0] == ViewMessages.DIVIDER


def test_show_internal_error(view: View) -> None:
    """
    Test for the show_internal_error method of the View class.

    Parameters
    ----------
    view : View
        An instance of the View class.
    """
    with patch("rich.console.Console.print") as mock_print:
        view.show_internal_error()

        first_call = mock_print.call_args_list[0]
        second_call = mock_print.call_args_list[1]
        assert mock_print.call_count == 2
        assert first_call[0][0] == ViewMessages.INTERNAL_ERROR
        assert second_call[0][0] == ViewMessages.DIVIDER


def test_get_symbols(view: View) -> None:
    """
    Test for the get_symbols method of the View class.

    Parameters
    ----------
    view : View
        An instance of the View class.
    """
    with patch("rich.console.Console.input") as mock_input:
        view.get_symbols()

        mock_input.assert_called_once_with(ViewMessages.SYMBOL_RETRIEVAL)
