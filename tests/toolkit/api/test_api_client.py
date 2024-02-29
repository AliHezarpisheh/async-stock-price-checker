"""
Module providing tests for the AsyncAPIClient class in toolkit.api.api_client module.
"""

from http import HTTPStatus
from unittest import mock

import httpx
import pytest

from toolkit.api.api_client import AsyncAPIClient


@pytest.fixture
def async_client() -> AsyncAPIClient:
    """Fixture providing an instance of AsyncAPIClient with a base URL."""
    base_url = "https://www.example.com"
    return AsyncAPIClient(base_url=base_url)


@pytest.mark.asyncio
async def test_get(async_client: AsyncAPIClient) -> None:
    """
    Test the 'get' method of AsyncAPIClient.

    The method should make an asynchronous GET request and return the expected response.
    """
    with mock.patch.object(
        async_client._client,
        "request",
        new_callable=mock.AsyncMock,
    ) as mock_request:
        mock_response = httpx.Response(
            status_code=200,
            content=b"test",
            request=httpx.Request("GET", "https://example.com/endpoint"),
        )
        mock_request.return_value = mock_response
        response = await async_client.get("/endpoint")

        assert response.status_code == HTTPStatus.OK
        assert response.text == "test"

        mock_request.assert_awaited_once()


@pytest.mark.asyncio
async def test_post(async_client: AsyncAPIClient) -> None:
    """
    Test the 'post' method of AsyncAPIClient.

    The method should make an asynchronous POST request and return the expected
    response.
    """
    with mock.patch.object(
        async_client._client,
        "request",
        new_callable=mock.AsyncMock,
    ) as mock_request:
        mock_response = httpx.Response(
            status_code=201,
            content=b"test",
            request=httpx.Request("POST", "https://example.com/endpoint"),
        )
        mock_request.return_value = mock_response
        response = await async_client.post("/endpoint")

        assert response.status_code == HTTPStatus.CREATED
        assert response.text == "test"

        mock_request.assert_awaited_once()


@pytest.mark.asyncio
async def test_put(async_client: AsyncAPIClient) -> None:
    """
    Test the 'put' method of AsyncAPIClient.

    The method should make an asynchronous PUT request and return the expected response.
    """
    with mock.patch.object(
        async_client._client,
        "request",
        new_callable=mock.AsyncMock,
    ) as mock_request:
        mock_response = httpx.Response(
            status_code=200,
            content=b"test",
            request=httpx.Request("PUT", "https://example.com/endpoint"),
        )
        mock_request.return_value = mock_response
        response = await async_client.put("/endpoint")

        assert response.status_code == HTTPStatus.OK
        assert response.text == "test"

        mock_request.assert_awaited_once()


@pytest.mark.asyncio
async def test_patch(async_client: AsyncAPIClient) -> None:
    """
    Test the 'patch' method of AsyncAPIClient.

    The method should make an asynchronous PATCH request and return the expected
    response.
    """
    with mock.patch.object(
        async_client._client,
        "request",
        new_callable=mock.AsyncMock,
    ) as mock_request:
        mock_response = httpx.Response(
            status_code=200,
            content=b"test",
            request=httpx.Request("PATCH", "https://example.com/endpoint"),
        )
        mock_request.return_value = mock_response
        response = await async_client.patch("/endpoint")

        assert response.status_code == HTTPStatus.OK
        assert response.text == "test"

        mock_request.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete(async_client: AsyncAPIClient) -> None:
    """
    Test the 'delete' method of AsyncAPIClient.

    The method should make an asynchronous DELETE request and return the expected
    response.
    """
    with mock.patch.object(
        async_client._client,
        "request",
        new_callable=mock.AsyncMock,
    ) as mock_request:
        mock_response = httpx.Response(
            status_code=201,
            content=b"test",
            request=httpx.Request("DELETE", "https://example.com/endpoint"),
        )
        mock_request.return_value = mock_response
        response = await async_client.delete("/endpoint")

        assert response.status_code == HTTPStatus.CREATED
        assert response.text == "test"

        mock_request.assert_awaited_once()


@pytest.mark.asyncio
async def test_close(async_client: AsyncAPIClient) -> None:
    """
    Test the 'close' method of AsyncAPIClient.

    The method should close the underlying asynchronous HTTP client.
    """
    with mock.patch.object(
        async_client._client, "aclose", new_callable=mock.AsyncMock
    ) as mock_aclose:
        await async_client.close()

        mock_aclose.assert_called_once()
