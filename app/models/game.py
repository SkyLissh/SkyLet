import time

from pydantic import BaseModel, validator


class Game(BaseModel):
    id: int
    name: str
    box_art_url: str

    @validator("box_art_url")
    def parse_box_art_url(cls, v: str) -> str:
        url = v.replace("{width}", "600").replace("{height}", "800")
        return f"{url}?{int(time.time())}"
