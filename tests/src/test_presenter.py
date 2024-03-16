"""Module implementing a test suite for the Presenter class."""

from unittest.mock import MagicMock

import pytest

from src.fetcher import StockQuotesFetcher
from src.model import Model, StockQuote
from src.presenter import Presenter
from src.view import View


@pytest.fixture
def mock_view() -> View:
    """Fixture for creating a MagicMock instance of View.

    Returns
    -------
    View
        A MagicMock instance of View.
    """
    return MagicMock(spec=View)


@pytest.fixture
def mock_model() -> MagicMock:
    """
    Fixture for creating a MagicMock instance of Model.

    Returns
    -------
    MagicMock
        A MagicMock instance of Model.
    """
    return MagicMock(spec=Model)


@pytest.fixture
def mock_fetcher() -> StockQuotesFetcher:
    """
    Fixture for creating a MagicMock instance of StockQuotesFetcher.

    Returns
    -------
    StockQuotesFetcher
        A MagicMock instance of StockQuotesFetcher.
    """
    return MagicMock(spec=StockQuotesFetcher)


@pytest.fixture
def presenter(
    mock_view: MagicMock, mock_model: MagicMock, mock_fetcher: MagicMock
) -> Presenter:
    """
    Fixture for creating an instance of Presenter with mocked dependencies.

    Parameters
    ----------
    mock_view : MagicMock
        A MagicMock instance of View.
    mock_model : MagicMock
        A MagicMock instance of Model.
    mock_fetcher : MagicMock
        A MagicMock instance of StockQuotesFetcher.

    Returns
    -------
    Presenter
        An instance of Presenter with mocked dependencies.
    """
    return Presenter(view=mock_view, model=mock_model, fetcher=mock_fetcher)


@pytest.mark.asyncio
async def test_update_model(
    presenter: Presenter, mock_view: MagicMock, mock_fetcher: MagicMock
) -> None:
    """
    Test case to ensure that update_model method updates the model correctly.

    Parameters
    ----------
    presenter : Presenter
        An instance of Presenter.
    mock_view : MagicMock
        A MagicMock instance of View.
    mock_fetcher : MagicMock
        A MagicMock instance of StockQuotesFetcher.
    """
    mock_view.get_symbols.return_value = "AAPL"
    mock_fetcher.fetch_stock_quote.return_value = {
        "Global Quote": {
            "01. symbol": "AAPL",
            "02. open": "149.75",
            "03. high": "152.34",
            "04. low": "149.25",
            "05. price": "150.42",
            "06. volume": "1000000",
            "07. latest trading day": "2024-03-15",
            "08. previous close": "150.50",
            "09. change": "0.70",
            "10. change percent": "0.50%",
        },
    }
    await presenter.update_model()
    presenter._view.get_symbols.assert_called_once()  # type: ignore


def test_update_view(
    presenter: Presenter, mock_view: MagicMock, mock_model: MagicMock
) -> None:
    """
    Test case to ensure that update_view method updates the view correctly.

    Parameters
    ----------
    presenter : Presenter
        An instance of Presenter.
    mock_view : MagicMock
        A MagicMock instance of View.
    mock_model : MagicMock
        A MagicMock instance of Model.
    """
    mock_model.stock_quotes = [
        StockQuote(
            "AAPL",
            "150.42",
            "152.34",
            "149.25",
            "151.20",
            "1000000",
            "2024-03-15",
            "150.50",
            "0.70",
            "0.50%",
        )
    ]
    presenter.update_view()
    mock_view.show_stock_quotes.assert_called_with(stock_quotes=mock_model.stock_quotes)


def test_handle_stock_quote_addition_with_invalid_data(
    presenter: Presenter, mock_model: MagicMock, mock_view: MagicMock
) -> None:
    """Test case to handle invalid stock data.

    Parameters
    ----------
    presenter : Presenter
        An instance of Presenter.
    mock_model : MagicMock
        A MagicMock instance of Model.
    mock_view : MagicMock
        A MagicMock instance of View.
    """
    stock_data = [{"symbol": "AAPL", "invalid_key": "150.42"}]
    presenter._prepare_stock_data = MagicMock(side_effect=ValueError("Invalid data"))  # type: ignore
    presenter._handle_stock_quote_addition(stock_data)

    assert mock_model.remove_all_stock_quotes.called
    assert mock_model.add_stock_quote.call_count == 0
    assert mock_view.show_external_service_error.call_count == 1
    assert mock_view.show_internal_error.call_count == 0


def test_handle_stock_quote_addition_with_exception(
    presenter: Presenter, mock_model: MagicMock, mock_view: MagicMock
) -> None:
    """
    Test case to ensure that handle_stock_quote_addition handles exceptions correctly.

    Parameters
    ----------
    presenter : Presenter
        An instance of Presenter.
    mock_model : MagicMock
        A MagicMock instance of Model.
    mock_view : MagicMock
        A MagicMock instance of View.
    """
    stock_data = [{"symbol": "AAPL", "price": "150.42"}]
    presenter._prepare_stock_data = MagicMock(side_effect=Exception("Unexpected error"))  # type: ignore
    presenter._handle_stock_quote_addition(stock_data)

    assert mock_model.remove_all_stock_quotes.called
    assert mock_model.add_stock_quote.call_count == 0
    assert mock_view.show_external_service_error.call_count == 0
    assert mock_view.show_internal_error.call_count == 1


@pytest.mark.parametrize(
    "stock_data, expected_output",
    [
        (
            {"Global Quote": {"01. symbol": "AAPL", "05. price": "150.42"}},
            {"symbol": "AAPL", "price": "150.42"},
        ),
        (
            {"Global Quote": {"01. symbol": "GOOGL", "05. price": "2809.02"}},
            {"symbol": "GOOGL", "price": "2809.02"},
        ),
    ],
)
def test_prepare_stock_data(
    presenter: Presenter,
    stock_data: dict[str, dict[str, str]],
    expected_output: dict[str, str],
) -> None:
    """
    Test case to ensure that prepare_stock_data method prepares stock data correctly.

    Parameters
    ----------
    presenter : Presenter
        An instance of Presenter.
    stock_data : dict[str, dict[str, str]]
        Input stock data.
    expected_output : dict[str, str]
        Expected prepared data.
    """
    prepared_data = presenter._prepare_stock_data(stock_data)
    assert prepared_data == expected_output


def test_prepare_invalid_stock_data(presenter: Presenter, mock_view: MagicMock) -> None:
    """
    Test case to ensure that prepare_stock_data handles invalid stock data correctly.

    Parameters
    ----------
    presenter : Presenter
        An instance of Presenter.
    mock_view : MagicMock
        A MagicMock instance of View.
    """
    presenter._prepare_stock_data({"Invalid": {"01. symbol": "AAPL"}})
    mock_view.show_external_service_error.assert_called_once()


@pytest.mark.parametrize(
    "symbols_string, expected_symbols_list",
    [
        ("AAPL", ["AAPL"]),
        ("AAPL, GOOGL", ["AAPL", "GOOGL"]),
        ("  AAPL,     GOOGL, AMZN  ", ["AAPL", "GOOGL", "AMZN"]),
    ],
)
def test_split_symbols(
    symbols_string: str, expected_symbols_list: list[str], presenter: Presenter
) -> None:
    """
    Test case to ensure that split_symbols method splits symbols correctly.

    Parameters
    ----------
    symbols_string : str
        Input string containing symbols.
    expected_symbols_list : list[str]
        Expected list of symbols.
    presenter : Presenter
        An instance of Presenter.
    """
    symbols_list = presenter._split_symbols(symbols_string)
    assert symbols_list == expected_symbols_list
