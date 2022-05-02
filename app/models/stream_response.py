from dataclasses import dataclass

from app.models.stream import Stream


@dataclass
class StreamResponse:
    data: list[Stream]

    @staticmethod
    def from_json(json: dict) -> "StreamResponse":
        return StreamResponse(
            data=[Stream.from_json(stream) for stream in json["data"]]
        )
