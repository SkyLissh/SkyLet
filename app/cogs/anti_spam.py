from typing import Optional

from discord import Member, Message, TextChannel, User, utils
from discord.ext import commands as cmd


class AntiSpam(cmd.Cog):
    last_message: Optional[Message] = None
    last_message_content: Optional[str] = None
    spam_count: int = 0

    whitelist: list[int] = [844338338562310186, 844338338562310186]

    def __init__(self, bot: cmd.Bot, muted: int, verified: int, logs: int) -> None:
        self.bot = bot
        self.muted = muted
        self.verified = verified
        self.logs = logs

    @cmd.group()
    async def antispam(self, ctx: cmd.Context) -> None:
        """
        Anti-spam commands
        """
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid command passed")

    async def mute_user(self, user: Member) -> None:
        muted = utils.get(user.guild.roles, id=self.muted)
        verified = utils.get(user.guild.roles, id=self.verified)

        if (not muted) or (not verified):
            return

        if muted in user.roles:
            return

        await user.add_roles(muted)
        await user.remove_roles(verified)

        channel = self.bot.get_channel(self.logs)

        if isinstance(channel, TextChannel):
            await channel.send(f"{user.mention} has been muted for spamming")

    @cmd.Cog.listener()
    async def on_message(self, message: Message) -> None:
        message_content = f"{message.author.id}: {message.content}"
        mentions = message.raw_mentions

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

        if self.spam_count > 1:
            self.spam_count = 0

            await self.mute_user(message.author)


def setup(bot: cmd.Bot) -> None:
    muted_role = 847192861627645982
    verified_role = 844333947366539274
    logs_channel = 844344065024720908

    bot.add_cog(AntiSpam(bot, muted_role, verified_role, logs_channel))
