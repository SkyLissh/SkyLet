from dataclasses import dataclass

from app.models.media import Media


@dataclass
class GifFormat:
    gif: Media
    medium_gif: Media
    webm: Media

    @staticmethod
    def from_json(json: dict) -> "GifFormat":
        return GifFormat(
            gif=Media.from_json(json["gif"]),
            medium_gif=Media.from_json(json["mediumgif"]),
            webm=Media.from_json(json["webm"]),
        )
