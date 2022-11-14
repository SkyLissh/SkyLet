from typing import Any

from discord import Member


def type_message(annotation: Any) -> str:
    if annotation is Member:
        return "Member (mention or id)"

    if annotation is str:
        return "Text (must contain spaces)"

    if annotation is int:
        return "Number"

    return "Unsupport type"
