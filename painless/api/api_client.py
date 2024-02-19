from urllib.parse import urljoin
from typing import Union

import httpx

from painless.api.helper.enums import AuthScheme
from painless.api.helper.exceptions import InvalidAuthSchemeError


class AsyncAPIClient:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.bas_url = base_url
        self.api_key = api_key

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        aut_scheme: AuthScheme,
        headers: Union[dict[str, str], None] = None,
        **kwargs: dict,
    ) -> httpx.Response:
        full_url = urljoin(self.bas_url, endpoint)
        headers = headers or {}
        auth_header = self.prepare_auth_header(auth_scheme=aut_scheme)

        with httpx.AsyncClient as client:
            response: httpx.Response = await client.request(
                method, full_url, headers=headers, **kwargs
            )
            response.raise_for_status()
            return response

    def prepare_auth_header(self, auth_scheme: AuthScheme) -> dict[str, str]:
        auth_schemes = [auth_scheme.value for auth_scheme in AuthScheme]
        if auth_scheme not in auth_schemes:
            raise InvalidAuthSchemeError(
                f"Invalid authorization scheme: `{auth_scheme}`\n"
                f"Available schemes are {tuple(auth_schemes)}"
            )

        authorization = f"{auth_scheme} {self.api_key}"
        return {"Authorization": authorization}
