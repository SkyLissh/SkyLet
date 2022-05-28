from typing import Optional

from discord import Member, Message, Role, TextChannel, User, utils
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

    async def check_roles(self, user: Member) -> list[Role]:
        muted = utils.get(user.guild.roles, id=self.muted)
        verified = utils.get(user.guild.roles, id=self.verified)

        if (not muted) or (not verified):
            return []

        return [muted, verified]

    async def text_channel(self, id: int) -> TextChannel:
        channel = self.bot.get_channel(id)

        if not isinstance(channel, TextChannel):
            raise ValueError("Channel is not a text channel")

        return channel

    async def mute_user(self, user: Member) -> None:
        muted, verified = await self.check_roles(user)

        channel = await self.text_channel(self.logs)

        if muted in user.roles:
            await channel.send(f"{user.mention} is already muted")
            return

        await user.add_roles(muted)
        await user.remove_roles(verified)

        await channel.send(f"{user.mention} has been muted")

    async def unmute_user(self, user: Member) -> None:
        muted, verified = await self.check_roles(user)

        channel = await self.text_channel(self.logs)

        if verified in user.roles:
            await channel.send(f"{user.mention} is not muted")
            return

        await user.add_roles(verified)
        await user.remove_roles(muted)

        await channel.send(f"{user.mention} has been unmuted")

    @cmd.command()
    async def mute(self, ctx: cmd.Context) -> None:
        try:
            user = ctx.message.mentions[0]

            if user.bot:
                await ctx.send("Bots cannot be muted")
                return

            if not isinstance(user, Member):
                return

            await self.mute_user(user)
        except IndexError:
            await ctx.send("Please mention a user to mute")

    @cmd.command()
    async def unmute(self, ctx: cmd.Context) -> None:
        try:
            user = ctx.message.mentions[0]

            if not isinstance(user, Member):
                return

            await self.unmute_user(user)
        except IndexError:
            await ctx.send("Please mention a user to unmute")

    @cmd.Cog.listener()
    async def on_message(self, message: Message) -> None:
        message_content = f"{message.author.id}: {message.content}"
        mentions = message.raw_mentions

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

            await self.mute_user(message.author)


def setup(bot: cmd.Bot) -> None:
    muted_role = 847192861627645982
    verified_role = 844333947366539274
    logs_channel = 976242439373328404

    bot.add_cog(AntiSpam(bot, muted_role, verified_role, logs_channel))
