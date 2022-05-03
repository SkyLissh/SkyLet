from typing import Any, Generic, Mapping, Type, TypeVar

from app.models.base import Base

T = TypeVar("T", bound=Base)
E = TypeVar("E")


class ApiResponse(Generic[T]):
    def __init__(self, json: Mapping[str, Any], response: Type[T]) -> None:
        self.json = json
        self.response = response

    @property
    def data(self) -> list[T]:
        return [self.response.from_json(d) for d in self.json["data"]]
