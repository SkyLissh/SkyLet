from discord import Embed

from app.models.stream import Stream
from app.models.user import User


def stream_embed(stream: Stream) -> Embed:
    embed = Embed()
    embed.color = 0x6441A4
    embed.set_author(name=f"{stream.user_name} is live on Twitch")
    embed.title = stream.title
    embed.url = f"https://twitch.tv/{stream.user_name}"
    embed.description = f"Playing {stream.game_name} for {stream.viewer_count} viewers"
    embed.set_image(url=f"{stream.thumbnail_url}")
    embed.set_footer(text="SkyLet")
    embed.timestamp = stream.started_at

    return embed


def user_embed(user: User) -> Embed:
    embed = Embed()
    embed.color = 0x6441A4
    embed.title = f"{user.display_name} is on Twitch"
    embed.url = f"https://twitch.tv/{user.login}"
    embed.description = f"{user.description}"
    embed.set_thumbnail(url=f"{user.profile_image_url}")
    embed.set_footer(text="Created at")
    embed.timestamp = user.created_at

    return embed
