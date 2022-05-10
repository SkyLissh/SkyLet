from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T", bound=BaseModel)


class ApiResponse(GenericModel, Generic[T]):
    data: list[T]
    pagination: Optional[dict[str, Any]]
