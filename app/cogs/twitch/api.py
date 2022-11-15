from typing import Optional

from app.models import ApiResponse, Follower, Game, Stream, User
from app.utils.chttp import chttp_twitch


class TwitchAPI:
    async def is_live(self, streamer: str) -> Optional[Stream]:
        res = await chttp_twitch.get("/streams", params={"user_login": streamer})
        res.raise_for_status()

        streams = ApiResponse[Stream].parse_obj(await res.json())

        if len(streams.data) == 0:
            return None

        return streams.data[0]

    async def get_user(self, username: str) -> Optional[User]:
        res = await chttp_twitch.get("/users", params={"login": username})
        res.raise_for_status()

        users = ApiResponse[User].parse_obj(await res.json())

        if len(users.data) == 0:
            return None

        return users.data[0]

    async def get_followers(self, id: int) -> int:
        res = await chttp_twitch.get("/users/follows", params={"to_id": id, "first": 1})
        res.raise_for_status()

        data = ApiResponse[Follower].parse_obj(await res.json())
        assert data.total is not None

        return data.total

    async def get_game(self, id: str) -> Optional[Game]:
        res = await chttp_twitch.get("/games", params={"id": id})
        res.raise_for_status()

        games = ApiResponse[Game].parse_obj(await res.json())

        if len(games.data) == 0:
            return None

        return games.data[0]
