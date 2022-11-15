from typing import Optional

from discord import Member, Message, User
from discord.ext import commands as cmd
from discord.ext.commands.errors import MemberNotFound

from app.client import SkyLet
from app.cogs.mute.mute_utils import MuteUtils
from app.decorators.auth import is_mod
from app.utils.embeds import error_embed


class AntiSpam(cmd.Cog):
    last_message: Optional[Message] = None
    last_message_content: Optional[str] = None
    spam_count: int = 0

    whitelist: list[int] = [844338338562310186, 844390801907515422]

    def __init__(self, bot: cmd.Bot, muted: int, verified: int, logs: int) -> None:
        self.bot = bot
        self.muted = muted
        self.verified = verified
        self.logs = logs
        self.mute_utils = MuteUtils(bot, muted, verified, logs)

    @cmd.command()
    @is_mod()
    async def mute(self, ctx: cmd.Context[SkyLet], user: Member, reason: str) -> None:
        try:
            if user.bot:
                await ctx.send(embed=error_embed("Bots cannot be muted"))
                return

            assert isinstance(ctx.author, Member)
            await self.mute_utils.mute_user(
                moderator=ctx.author,
                user=user,
                reason=reason,
            )
        except MemberNotFound:
            await ctx.send(embed=error_embed("Please mention a valid user to mute"))

    @cmd.command()
    @is_mod()
    async def unmute(self, ctx: cmd.Context[SkyLet], user: Member) -> None:
        try:
            await self.mute_utils.unmute_user(user)
        except MemberNotFound:
            await ctx.send(embed=error_embed("Please mention a user to mute"))

    @cmd.Cog.listener()
    async def on_message(self, message: Message) -> None:
        message_content = f"{message.author.id}: {message.content}"
        mentions = message.raw_mentions
        self.bot

        if message.author.bot:
            return

        if isinstance(message.author, User):
            return

        roles_id: list[int] = [role.id for role in message.author.roles]
        check_roles: bool = any(item in roles_id for item in self.whitelist)

        if check_roles:
            return

        if message_content == self.last_message_content:
            self.spam_count += 1
            await message.delete()
        else:
            self.last_message = message
            self.last_message_content = message_content
            self.spam_count = 0

        if len(mentions) > 10:
            await message.delete()
            self.spam_count += 2

        if self.spam_count > 3:
            self.spam_count = 0

            assert self.bot.user is not None
            await self.mute_utils.mute_user(
                moderator=self.bot.user, user=message.author, reason="Spamming"
            )


async def setup(bot: cmd.Bot) -> None:
    muted_role = 847192861627645982
    verified_role = 844333947366539274
    logs_channel = 976242439373328404

    await bot.add_cog(AntiSpam(bot, muted_role, verified_role, logs_channel))
