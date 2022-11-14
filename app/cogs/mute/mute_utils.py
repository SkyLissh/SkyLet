from typing import Union

from discord import ClientUser, Member, Role, TextChannel, utils
from discord.ext import commands as cmd

from app.utils.embeds import error_embed, info_embed, mute_embed


class MuteUtils:
    def __init__(self, bot: cmd.Bot, muted: int, verified: int, logs: int) -> None:
        self.muted = muted
        self.verified = verified
        self.logs = logs
        self.bot = bot

    async def check_roles(self, user: Member) -> list[Role]:
        muted = utils.get(user.guild.roles, id=self.muted)
        verified = utils.get(user.guild.roles, id=self.verified)

        if (not muted) or (not verified):
            return []

        return [muted, verified]

    async def mute_user(
        self, *, moderator: Union[Member, ClientUser], user: Member, reason: str
    ) -> None:
        muted, verified = await self.check_roles(user)

        channel = self.bot.get_channel(self.logs)
        assert isinstance(channel, TextChannel)

        if muted in user.roles:
            await channel.send(embed=error_embed(f"{user.mention} is already muted"))
            return

        await user.add_roles(muted)
        await user.remove_roles(verified)

        await channel.send(
            embed=mute_embed(
                moderator=moderator,
                user=user,
                reason=reason,
            )
        )

    async def unmute_user(self, user: Member) -> None:
        muted, verified = await self.check_roles(user)

        channel = self.bot.get_channel(self.logs)
        assert isinstance(channel, TextChannel)

        if verified in user.roles:
            await channel.send(embed=error_embed(f"{user.mention} is not muted"))
            return

        await user.add_roles(verified)
        await user.remove_roles(muted)

        await channel.send(embed=info_embed(f"{user.mention} has been unmuted"))
