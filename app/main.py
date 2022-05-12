import logging
import os
import platform
from typing import Union

import discord
from discord.ext import commands
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()

log: logging.Logger = logging.getLogger(__name__)

PREFIX: str = os.getenv("DISCORD_PREFIX") or ">"
DISCORD_TOKEN: Union[str, None] = os.getenv("DISCORD_TOKEN")

if DISCORD_TOKEN is None:
    log.error("DISCORD_TOKEN is not set")
    exit(0)

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(PREFIX), description="SkyLet discord bot"
)

modules: list[str] = ["app.cogs.twitch", "app.cogs.anti_spam"]

# Load all modules
for m in modules:
    bot.load_extension(m)
    log.debug(f"Loaded module {m}")

log.info(f"Loaded {len(modules)} modules")


@bot.event
async def on_ready() -> None:
    print(
        """\
    ░██████╗██╗░░██╗██╗░░░██╗██╗░░░░░███████╗████████╗
    ██╔════╝██║░██╔╝╚██╗░██╔╝██║░░░░░██╔════╝╚══██╔══╝
    ╚█████╗░█████═╝░░╚████╔╝░██║░░░░░█████╗░░░░░██║░░░
    ░╚═══██╗██╔═██╗░░░╚██╔╝░░██║░░░░░██╔══╝░░░░░██║░░░
    ██████╔╝██║░╚██╗░░░██║░░░███████╗███████╗░░░██║░░░
    ╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚══════╝░░░╚═╝░░░
    """
    )

    table_rows = [
        ["discord.py", f"v{discord.__version__}"],
        ["python", f"v{platform.python_version()}"],
        ["system", f"{platform.system()} v{platform.version()}"],
        ["discord user", f"{bot.user} (id: {bot.user.id})"],
        ["guilds", f"{len(bot.guilds)}"],
        ["users", f"{len(bot.users)}"],
    ]
    log.info("\n" + tabulate(table_rows))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    bot.run(DISCORD_TOKEN)
