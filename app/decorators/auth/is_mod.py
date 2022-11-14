from discord import Member
from discord.ext import commands as cmd
from discord.ext.commands._types import Check

from app.utils.embeds import error_embed


def is_mod() -> Check:
    async def predicate(ctx: cmd.Context) -> bool:
        user = ctx.author
        assert isinstance(user, Member)

        if user.guild_permissions.kick_members or await ctx.bot.is_owner(user):
            return True

        await ctx.send(
            embed=error_embed("You do not have permission to use this command")
        )
        return False

    return cmd.check(predicate)
