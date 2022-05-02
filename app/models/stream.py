from dataclasses import dataclass


@dataclass()
class Stream:
    id: str

    user_id: str
    user_name: str

    game_name: str

    type: str

    title: str
    viewer_count: int

    thumbnail_url: str

    @staticmethod
    def from_json(json: dict) -> "Stream":
        return Stream(
            id=json["id"],
            user_id=json["user_id"],
            user_name=json["user_name"],
            game_name=json["game_name"],
            type=json["type"],
            title=json["title"],
            viewer_count=json["viewer_count"],
            thumbnail_url=json["thumbnail_url"]
            .replace("{width}", "1920")
            .replace("{height}", "1080"),
        )
