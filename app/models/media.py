from dataclasses import dataclass


@dataclass
class Media:
    url: str
    size: int
    preview: str

    @staticmethod
    def from_json(json: dict) -> "Media":
        return Media(
            url=json["url"],
            size=json["size"],
            preview=json["preview"],
        )
