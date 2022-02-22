from dataclasses import dataclass
from typing import List

from app.models.gif_formats import GifFormat


@dataclass
class GifObject:
    id: str
    title: str
    url: str
    media: List[GifFormat]

    @staticmethod
    def from_json(json: dict) -> "GifObject":
        return GifObject(
            id=json["id"],
            title=json["title"],
            url=json["url"],
            media=[GifFormat.from_json(media) for media in json["media"]],
        )


@dataclass
class GifResponse:
    results: List[GifObject]
    next: str

    @staticmethod
    def from_json(json: dict) -> "GifResponse":
        return GifResponse(
            results=[GifObject.from_json(result) for result in json["results"]],
            next=json["next"],
        )
