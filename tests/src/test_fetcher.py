"""Module for fetching stock quotes asynchronously."""

import json
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from src.enums import AlphaVantageAPIConsts as AVAPIConsts
from src.fetcher import StockQuotesFetcher
from toolkit.api import AsyncAPIClient


@pytest.fixture
def fetcher() -> StockQuotesFetcher:
    """Fixture for creating a StockQuotesFetcher instance."""
    return StockQuotesFetcher(
        api_client=AsyncAPIClient(base_url=AVAPIConsts.BASE_URL), api_key="api_key"
    )


@pytest.mark.asyncio
async def test_fetch_stock_quote_success(fetcher: StockQuotesFetcher) -> None:
    """Test fetching stock quote successfully."""
    mock_response = httpx.Response(
        status_code=200,
        json={"test_key": "test_value"},
        request=httpx.Request("get", AVAPIConsts.BASE_URL),
    )

    async def mock_get(endpoint: str, params: dict[str, str]) -> httpx.Response:
        return mock_response

    with patch.object(fetcher, "_client", new_callable=AsyncMock) as mock_client:
        mock_client.get.side_effect = mock_get

        actual_content = await fetcher.fetch_stock_quote(
            endpoint="/", operation="GLOBAL", symbol="AAPL"
        )
        assert actual_content == mock_response.json()


@pytest.mark.asyncio
async def test_fetch_stock_quote_json_error(fetcher: StockQuotesFetcher) -> None:
    """Test fetching stock quote with JSON decode error."""
    mock_response = httpx.Response(
        status_code=200,
        request=httpx.Request("get", AVAPIConsts.BASE_URL),
    )

    async def mock_get(endpoint: str, params: dict[str, str]) -> httpx.Response:
        return mock_response

    with patch.object(fetcher, "_client", new_callable=AsyncMock) as mock_client:
        mock_client.get.side_effect = mock_get

        with pytest.raises(json.JSONDecodeError):
            await fetcher.fetch_stock_quote(
                endpoint="/", operation="GLOBAL", symbol="AAPL"
            )


def test_construct_params(fetcher: StockQuotesFetcher) -> None:
    """Test constructing parameters for fetching stock quotes."""
    actual_params = fetcher._construct_params(operation="GLOBAL", symbol="AAPL")
    expected_params = {"apikey": "api_key", "function": "GLOBAL", "symbol": "AAPL"}
    assert (
        actual_params == expected_params
    ), f"expect `{expected_params}` params, got `{actual_params}`"
