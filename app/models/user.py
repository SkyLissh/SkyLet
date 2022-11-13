from datetime import datetime

from pydantic import BaseModel, validator

from app.utils.format_number import format_number


class User(BaseModel):
    id: int

    display_name: str
    login: str

    description: str
    profile_image_url: str

    view_count: str
    created_at: datetime

    @validator("view_count")
    def parse_view_count(cls, v: int) -> str:
        return format_number(v)
