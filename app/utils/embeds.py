from discord import Embed

from app.models.stream import Stream
from app.models.user import User
from app.utils.format_number import format_number


def stream_embed(stream: Stream) -> Embed:
    views: str = format_number(stream.viewer_count)

    embed = Embed()
    embed.color = 0x6441A4

    embed.set_author(name=f"{stream.user_name} is live on Twitch")
    embed.title = stream.title
    embed.url = f"https://twitch.tv/{stream.user_name}"

    embed.description = f"Playing {stream.game_name} for {views} viewers"
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
