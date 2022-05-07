from json import loads
from typing import Any
import aiohttp


class exceptions:
    class HTTPError(Exception):
        pass

    class RatelimitExceeded(Exception):
        pass


class CHTTPResponse:
    def __init__(self, aiorequest: aiohttp.ClientResponse, text: str) -> None:
        self._aiorequest = aiorequest
        self._text = text

    @staticmethod
    async def make(aiorequest: aiohttp.ClientResponse) -> "CHTTPResponse":
        return CHTTPResponse(aiorequest, await aiorequest.text())

    async def json(self) -> dict[str, Any]:
        return loads(self._text)

    def raise_for_status(self) -> None:
        if self._aiorequest.status > 399:
            raise exceptions.HTTPError(
                f"Request failed with status code {self._aiorequest.status}"
            )

    @property
    def status(self) -> int:
        return self._aiorequest.status

    async def text(self) -> str:
        return self._text
