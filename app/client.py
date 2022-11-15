import logging
import platform
import traceback

import discord
from discord.ext import commands as cmd
from discord.ext.commands._types import BotT
from tabulate import tabulate

from app.utils.embeds import error_embed, invalid_command_embed

ArgumentError = (
    cmd.MissingRequiredArgument,
    cmd.BadArgument,
    cmd.TooManyArguments,
    cmd.UserInputError,
)


class SkyLet(cmd.Bot):
    log = logging.getLogger("app.skylet")
    modules: list[str] = ["app.cogs.twitch.twitch", "app.cogs.mute.mute"]

    async def on_ready(self) -> None:
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
        assert self.user is not None

        table_rows = [
            ["discord.py", f"v{discord.__version__}"],
            ["python", f"v{platform.python_version()}"],
            ["system", f"{platform.system()} v{platform.version()}"],
            ["discord user", f"{self.user} (id: {self.user.id})"],
            ["guilds", f"{len(self.guilds)}"],
            ["users", f"{len(self.users)}"],
        ]
        self.log.info("\n" + tabulate(table_rows))

    async def on_command_error(self, ctx: cmd.Context[BotT], error: Exception) -> None:
        if isinstance(error, cmd.CommandNotFound):
            await ctx.send(embed=error_embed("Command not found"))
            return

        assert ctx.command is not None

        if isinstance(error, ArgumentError):
            await ctx.send(embed=invalid_command_embed(ctx.command))
            return

        if isinstance(error, cmd.MemberNotFound):
            await ctx.send(embed=error_embed("Member not found"))
            return

        self.log.error(f"Error in command {ctx.command}: {error} - type: {type(error)}")
        self.log.exception(
            "".join(traceback.format_exception(type(error), error, error.__traceback__))
        )

    async def setup_hook(self) -> None:
        for m in self.modules:
            await self.load_extension(m)
            self.log.info(f"Loaded module {m}")

        self.log.info(f"Loaded {len(self.modules)} modules")
