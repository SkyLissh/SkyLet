import time
from datetime import datetime

from pydantic import BaseModel, validator

from app.utils.format_number import format_number


class Stream(BaseModel):
    id: int

    user_id: int
    user_name: str
    user_login: str

    game_name: str
    game_id: str

    title: str
    viewer_count: str
    thumbnail_url: str

    started_at: datetime
    url: str = "https://twitch.tv/{user_login}"

    @validator("thumbnail_url")
    def parse_thumbnail_url(cls, v: str) -> str:
        url = v.replace("{width}", "1920").replace("{height}", "1080")
        return f"{url}?{int(time.time())}"

    @validator("viewer_count")
    def parse_viewer_count(cls, v: int) -> str:
        return format_number(int(v))
