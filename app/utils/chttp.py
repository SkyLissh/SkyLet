import asyncio
import logging
import os
import time
from math import ceil
from typing import Any, Optional

import aiohttp

from app.models.token import Token
from app.utils.chttp_response import CHTTPResponse


class TwitchCHTTP:
    def __init__(self) -> None:
        self.aiohttp = aiohttp.ClientSession()
        self.base_url = "https://api.twitch.tv/helix"
        self.token: Optional[Token] = None
        self.logger = logging.getLogger("chttp.twitch")
        self.client_config = {
            "client_id": os.getenv("TWITCH_CLIENT_ID") or "",
            "client_secret": os.getenv("TWITCH_CLIENT_SECRET") or "",
            "grant_type": "client_credentials",
        }

    @property
    def base_headers(self) -> dict[str, str]:
        token = self.token.access_token if self.token else ""

        return {
            "Accept": "application/vnd.twitchtv.v5+json",
            "Authorization": f"Bearer {token}",
            "Client-ID": self.client_config["client_id"],
        }

    async def _get_access_token(self) -> None:
        """
        Obtain an App access token from Twitch's OAuth Client Crdentials Flow.
        https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/#oauth-client-credentials-flow
        """

        params = self.client_config
        async with self.aiohttp.post(
            "https://id.twitch.tv/oauth2/token", params=params
        ) as res:
            if res.status > 399:
                self.logger.exception(f"Error {res.status} while getting access token")
                self.logger.fatal(f"{await res.text()}")
                self.token = None

            token = Token.parse_obj(await res.json())
            try:
                token.expires_in += time.time()
            except KeyError:
                self.logger.warning("Failed to set token expiration time")

            self.logger.info(
                "Obtain access token for Twitch API: %s",
                str(token).replace(token.access_token, "[REDACTED]"),
            )

            self.token = token

    async def get(
        self, url: str, params: Optional[dict[str, Any]] = None
    ) -> CHTTPResponse:
        """
        Perform an HTTP GET request to Twitch API
        """
        if self.token is None or self.token.expires_in < time.time() + 1:
            await self._get_access_token()

        ctime = time.time()
        async with self.aiohttp.get(
            f"{self.base_url}{url}", headers=self.base_headers, params=params
        ) as res:
            self.logger.debug(
                "GET %s%s %i (%ims)",
                res.url.host,
                res.url.path,
                res.status,
                round((time.time() - ctime) * 1000),
            )

            if res.status > 399:
                self.logger.fatal(f"{await res.text()}")

            if (
                int(res.headers.get("RateLimit-Remaining", 99)) <= 5
                and res.status == 200
            ):
                bucket_reset = float(res.headers.get("RateLimit-Reset", time.time()))
                wait_time = ceil(bucket_reset - time.time() + 0.5)

                self.logger.warning(f"RateLimit bucket exhausted, waiting {wait_time}s")

                await asyncio.sleep(wait_time)

            return await CHTTPResponse.make(res)


chttp_twitch = TwitchCHTTP()
