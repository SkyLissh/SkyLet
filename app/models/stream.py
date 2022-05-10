from datetime import datetime

from pydantic import BaseModel, validator


class Stream(BaseModel):
    id: int

    user_id: int
    user_name: str

    game_name: str

    title: str
    viewer_count: int
    thumbnail_url: str

    started_at: datetime

    @validator("thumbnail_url")
    def parse_thumbnail_url(cls, v: str) -> str:
        return v.replace("{width}", "1920").replace("{height}", "1080")

    @validator("started_at")
    def parse_started_at(cls, v: str) -> datetime:
        return datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ")
