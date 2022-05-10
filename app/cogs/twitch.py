import re
from typing import Optional

from discord import TextChannel
from discord.ext import commands as cmd
from discord.ext import tasks

from app.models.api_response import ApiResponse
from app.models.stream import Stream
from app.models.user import User
from app.utils.chttp import chttp_twitch
from app.utils.embeds import stream_embed, user_embed


class Twitch(cmd.Cog):
    def __init__(self, bot: cmd.Bot, channel: int) -> None:
        self.bot = bot
        self.last_tick = False
        self.channel = channel
        # self.streamer = streamer

    @cmd.group()
    async def twitch(self, ctx: cmd.Context) -> None:
        """
        Twitch commands
        """
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid command passed")

    async def is_live(self, streamer: str) -> Optional[Stream]:
        res = await chttp_twitch.get("/streams", params={"user_login": streamer})
        res.raise_for_status()

        streams = ApiResponse[Stream].parse_obj(await res.json())

        if len(streams.data) == 0:
            return None

        return streams.data[0]

    async def get_streamer(self, streamer: str) -> Optional[User]:
        res = await chttp_twitch.get("/users", params={"login": streamer})
        res.raise_for_status()

        users = ApiResponse[User].parse_obj(await res.json())

        if len(users.data) == 0:
            return None

        return users.data[0]

    async def get_followers(self, id: int) -> int:
        res = await chttp_twitch.get("/users/follows", params={"to_id": id, "first": 1})
        res.raise_for_status()

        data = await res.json()

        return data["total"]

    @twitch.command()
    async def live(self, ctx: cmd.Context, *, streamer: str = "skylissh") -> None:
        if re.match(r"[\w]+$", streamer) is None:
            await ctx.send("Invalid streamer name")
            return

        if stream := await self.is_live(streamer):
            embed = stream_embed(stream)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{streamer} is not live")

    @twitch.command()
    async def info(self, ctx: cmd.Context, *, streamer: str = "skylissh") -> None:
        if re.match(r"[\w]+$", streamer) is None:
            await ctx.send("Invalid streamer name")
            return

        if user := await self.get_streamer(streamer):
            follows = await self.get_followers(user.id)

            embed = user_embed(user, follows)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{streamer} is not on Twitch")

    @tasks.loop(minutes=1)
    async def check_streams(self) -> None:

        if self.last_tick:
            return

        self.last_tick = True
        await self.bot.wait_until_ready()

        if stream := await self.is_live("skylissh"):
            embed = stream_embed(stream)
            channel = self.bot.get_channel(self.channel)

            if isinstance(channel, TextChannel):
                await channel.send(
                    ":red_circle: SkyLissh is live ||@everyone||", embed=embed
                )
                return

        self.last_tick = False

    @cmd.Cog.listener()
    async def on_ready(self) -> None:
        # await self.check_streams.start()
        pass


def setup(bot: cmd.Bot) -> None:
    bot.add_cog(Twitch(bot, 844345187819847701))
