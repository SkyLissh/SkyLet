from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int

    display_name: str
    login: str

    description: str
    profile_image_url: str

    created_at: datetime
