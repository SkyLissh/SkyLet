from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping

from app.models.base import Base


@dataclass()
class Stream(Base["Stream"]):
    id: str

    user_id: str
    user_name: str

    game_name: str

    type: str

    title: str
    viewer_count: int

    thumbnail_url: str

    started_at: datetime

    @staticmethod
    def from_json(json: Mapping[str, Any]) -> "Stream":
        return Stream(
            id=json["id"],
            user_id=json["user_id"],
            user_name=json["user_name"],
            game_name=json["game_name"],
            type=json["type"],
            title=json["title"],
            viewer_count=json["viewer_count"],
            started_at=datetime.strptime(json["started_at"], "%Y-%m-%dT%H:%M:%SZ"),
            thumbnail_url=json["thumbnail_url"]
            .replace("{width}", "1920")
            .replace("{height}", "1080"),
        )
