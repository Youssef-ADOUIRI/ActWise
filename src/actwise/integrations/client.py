"""A client of the ActWise HTTP API, shared by the UI, the Slack bot and the MCP server."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import httpx

DEFAULT_URL = "http://localhost:8000"
TIMEOUT = 60.0  # seconds: the API stops calling models after 50


class ApiError(Exception):
    """The API refused the request or did not answer; the message says why."""


def detail(response: httpx.Response) -> str:
    """The API's error message: FastAPI's `detail`, or the raw body."""
    try:
        found = response.json()["detail"]
    except (ValueError, KeyError, TypeError):
        return response.text
    if isinstance(found, list):  # input validation errors
        return "; ".join(str(error.get("msg")) for error in found)
    return str(found)


class ApiClient:
    """POST to the API at `url`, with `key` in X-API-Key when the API needs one."""

    def __init__(self, url: str, key: str | None, transport: httpx.BaseTransport | None = None):
        """`transport` replaces the network in tests."""
        self.url = url
        headers = {"X-API-Key": key} if key else {}
        self.http = httpx.Client(
            base_url=url, headers=headers, timeout=TIMEOUT, transport=transport
        )

    @classmethod
    def from_env(cls, env: Mapping[str, str]) -> ApiClient:
        """ACTWISE_API_URL (default localhost:8000) and ACTWISE_API_KEY."""
        return cls(env.get("ACTWISE_API_URL") or DEFAULT_URL, env.get("ACTWISE_API_KEY") or None)

    def post(self, path: str, **request: Any) -> dict[str, Any]:
        """The JSON reply; `ApiError` for an error status or an API that did not answer."""
        try:
            response = self.http.post(path, **request)
        except httpx.HTTPError as exc:
            raise ApiError(f"The ActWise API at {self.url} did not answer: {exc!r}") from exc
        if response.is_error:
            raise ApiError(f"Error {response.status_code}: {detail(response)}")
        return response.json()
