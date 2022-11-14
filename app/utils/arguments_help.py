from discord.ext import commands as cmd

from app.utils.type_message import type_message


def argument_help(params: dict[str, cmd.Parameter]) -> str:
    if not params:
        return "No arguments"

    return "\n".join(
        f"`{param.name}`: {type_message(param.annotation)}" for param in params.values()
    )
