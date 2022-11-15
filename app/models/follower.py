from datetime import datetime

from pydantic import BaseModel


class Follower(BaseModel):
    from_id: str
    from_login: str
    from_name: str

    to_id: str
    to_name: str

    followed_at: datetime
