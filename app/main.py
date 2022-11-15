import asyncio
import importlib.util
import logging
import os
from typing import Optional

import discord
from discord.ext import commands
from dotenv import load_dotenv

from app.client import SkyLet

load_dotenv()
discord.utils.setup_logging()
log: logging.Logger = logging.getLogger(__name__)


async def main():
    PREFIX: str = os.getenv("DISCORD_PREFIX", ">")
    DISCORD_TOKEN: Optional[str] = os.getenv("DISCORD_TOKEN")

    if DISCORD_TOKEN is None:
        log.error("DISCORD_TOKEN is not set")
        exit(0)

    intents = discord.Intents.default()
    intents.message_content = True

    bot = SkyLet(
        command_prefix=commands.when_mentioned_or(PREFIX),
        description="SkyLet discord bot",
        intents=intents,
    )

    await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    spec = importlib.util.find_spec("uvloop")
    if spec is not None:
        import uvloop  # type: ignore

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    else:
        log.warning("uvloop is not installed, falling back to asyncio")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Stopping bot")
