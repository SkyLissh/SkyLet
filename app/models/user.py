from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping

from app.models.base import Base


@dataclass()
class User(Base["User"]):
    id: int

    display_name: str
    login: str

    description: str
    profile_image_url: str

    created_at: datetime

    @staticmethod
    def from_json(json: Mapping[str, Any]) -> "User":
        return User(
            id=json["id"],
            display_name=json["display_name"],
            login=json["login"],
            description=json["description"],
            profile_image_url=json["profile_image_url"],
            created_at=datetime.strptime(json["created_at"], "%Y-%m-%dT%H:%M:%SZ"),
        )
