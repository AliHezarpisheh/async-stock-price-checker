"""Module implementing a test suite for the stock quote model."""

import pytest

from src.model import Model, StockQuote


@pytest.fixture(scope="module")
def stock_quote() -> StockQuote:
    """Fixture function for creating a StockQuote instance."""
    return StockQuote(
        symbol="GOOGL",
        open="2710.00",
        high="2732.45",
        low="2704.10",
        price="2729.80",
        volume="1185947",
        latest_trading_day="2024-03-14",
        previous_close="2717.50",
        change="+12.30",
        change_percent="+0.45%",
    )


@pytest.fixture(scope="module")
def model() -> Model:
    """Fixture function for creating a Model instance."""
    return Model()


def test_stock_quote_immutability(stock_quote: StockQuote) -> None:
    """Verify the immutability of the StockQuote class."""
    with pytest.raises(AttributeError):
        stock_quote.symbol = "AAPL"  # type: ignore


@pytest.mark.smoke
def test_add_stock_quote(model: Model, stock_quote: StockQuote) -> None:
    """Verify the functionality of adding a stock quote to the model."""
    model.add_stock_quote(stock_quote=stock_quote)
    assert len(model.stock_quotes) == 1
    assert model.stock_quotes[0] == stock_quote


@pytest.mark.smoke
def test_remove_stock_quotes(model: Model) -> None:
    """Verify the functionality of removing all stock quotes."""
    model.remove_all_stock_quotes()
    assert len(model.stock_quotes) == 0
    assert model.stock_quotes == []
