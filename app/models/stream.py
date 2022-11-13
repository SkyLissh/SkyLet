from datetime import datetime

from pydantic import BaseModel, validator

from app.utils.format_number import format_number


class Stream(BaseModel):
    id: int

    user_id: int
    user_name: str
    user_login: str

    game_name: str

    title: str
    viewer_count: str
    thumbnail_url: str

    started_at: datetime
    url: str

    @validator("thumbnail_url")
    def parse_thumbnail_url(cls, v: str) -> str:
        dt = datetime.now()
        v.replace("{width}", "1920").replace("{height}", "1080")
        return f"{v}?{int(dt.timestamp())}"

    @validator("viewer_count")
    def parse_viewer_count(cls, v: int) -> str:
        return format_number(v)

    @validator("url")
    def parse_url(cls, v: str, values: "Stream") -> str:
        return f"https://twitch.tv/{values.user_login}"
