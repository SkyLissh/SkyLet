import re
from typing import Optional

from discord import TextChannel
from discord.ext import commands as cmd
from discord.ext import tasks

from app.cogs.twitch.api import TwitchAPI
from app.models import User
from app.utils.embeds import error_embed, stream_embed, user_embed


class Twitch(cmd.Cog):
    def __init__(self, bot: cmd.Bot, channel: int) -> None:
        self.bot = bot
        self.last_tick = False
        self.channel = channel
        self.api = TwitchAPI()
        # self.streamer = streamer

    async def valid_streamer(self, ctx: cmd.Context, streamer: str) -> Optional[User]:
        if re.match(r"^[a-zA-Z0-9_]{4,25}$", streamer) is None:
            await ctx.send(embed=error_embed("Invalid username"))
            return None

        user = await self.api.get_user(streamer)

        if not user:
            await ctx.send(embed=error_embed(f"{streamer} is not on Twitch"))
            return None

        return user

    @cmd.command()
    async def twitch(self, ctx: cmd.Context, *, streamer: str = "skylissh") -> None:
        """
        Check if a streamer is live on Twitch
        """

        user = await self.valid_streamer(ctx, streamer)

        if not user:
            return

        if stream := await self.api.is_live(streamer):
            game = await self.api.get_game(stream.game_id)

            assert game is not None

            embed = stream_embed(stream=stream, user=user, game=game)
            await ctx.send(embed=embed)
        else:
            follows = await self.api.get_followers(user.id)

            embed = user_embed(user=user, follows=follows)
            await ctx.send(embed=embed)

    @tasks.loop(minutes=1)
    async def check_streams(self) -> None:
        await self.bot.wait_until_ready()

        stream = await self.api.is_live("skylissh")

        if stream and (not self.last_tick):
            user = await self.api.get_user("skylissh")
            assert user is not None

            game = await self.api.get_game(stream.game_id)
            assert game is not None

            embed = stream_embed(stream=stream, user=user, game=game)
            channel = self.bot.get_channel(self.channel)

            if isinstance(channel, TextChannel):
                await channel.send(
                    ":red_circle: SkyLissh is live ||@everyone||", embed=embed
                )

                self.last_tick = True

        elif not stream and self.last_tick:
            self.last_tick = False

    @cmd.Cog.listener()
    async def on_ready(self) -> None:
        await self.check_streams.start()


async def setup(bot: cmd.Bot) -> None:
    await bot.add_cog(Twitch(bot, 844345187819847701))
