from discord import Embed

from app.models.stream import Stream
from app.models.user import User
from app.utils.format_number import format_number


def stream_embed(stream: Stream, user: User) -> Embed:
    embed = Embed()
    embed.color = 0x6441A4

    embed.set_author(
        name=f"{stream.user_name} is live on Twitch",
        url=stream.url,
        icon_url=user.profile_image_url,
    )
    embed.title = stream.title
    embed.url = stream.url

    embed.description = f"Playing {stream.game_name} for {stream.viewer_count} viewers"
    embed.set_image(url=stream.thumbnail_url)

    embed.set_footer(text="SkyLet")
    embed.timestamp = stream.started_at

    return embed


def user_embed(user: User, follows: int) -> Embed:
    followers: str = format_number(follows)

    embed = Embed()
    embed.color = 0x6441A4

    embed.title = f"{user.display_name} is on Twitch"
    embed.url = f"https://twitch.tv/{user.login}"

    embed.description = user.description
    embed.set_thumbnail(url=user.profile_image_url)

    embed.add_field(name=":busts_in_silhouette: Followers", value=followers)
    embed.add_field(name=":eyes: Views", value=user.view_count)

    embed.set_footer(text="Created at")
    embed.timestamp = user.created_at

    return embed
