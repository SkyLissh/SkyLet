from abc import ABC, abstractmethod
from typing import Any, Generic, Mapping, TypeVar

T = TypeVar("T")


class Base(ABC, Generic[T]):
    @staticmethod
    @abstractmethod
    def from_json(json: Mapping[str, Any]) -> T:
        pass
