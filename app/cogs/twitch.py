from discord.ext.commands import Bot, Cog, Context, command

from app.utils.chttp import chttp_twitch


class Twitch(Cog):
    def __init__(self, bot: Bot, streamer: str) -> None:
        self.bot = bot
        self.streamer = streamer

    async def is_live(self) -> bool:
        res_json = await chttp_twitch.get("/streams", params={"user_login": "skylet"})
