import os
from typing import Union

import discord
import requests
from dotenv import load_dotenv

from app.commands import GIF_COMMANDS
from app.models.gif import GifResponse

load_dotenv()

client = discord.Client()

DISCORD_TOKEN: Union[str, None] = os.getenv("DISCORD_TOKEN")
TENOR_KEY: Union[str, None] = os.getenv("TENOR_KEY")

RANDOM_URL: str = "https://g.tenor.com/v1/random?"

if DISCORD_TOKEN is None:
    raise ValueError("DISCORD_TOKEN is not set")


def get_gif(query: str) -> GifResponse:
    print(f"Getting gif for {query}")
    res: requests.Response = requests.get(
        RANDOM_URL, params={"key": TENOR_KEY, "q": f"anime {query}", "limit": "1"}
    )

    return GifResponse.from_json(res.json())


def create_embed(message: discord.Message, cmd: str) -> Union[discord.Embed, str]:
    msg: str

    embedded = discord.Embed()
    if len(message.mentions) > 0:
        text: str = "said hi" if cmd == "hi" else f"give a {cmd}"
        msg = f"**{message.author.name}** {text} to **{message.mentions[0].name}**!"
    else:
        if cmd == "hi":
            msg = f"**{message.author.name}** said hello to everyone!!"
        else:
            return "You need to mention someone to use the command!"

    embedded.description = msg
    embedded.set_image(url=get_gif(cmd).results[0].media[0].gif.url)
    embedded.set_footer(text="Powered by Tenor")

    return embedded


@client.event
async def on_ready() -> None:
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message: discord.Message) -> None:
    if message.author == client.user:
        return

    for cmd in GIF_COMMANDS:
        if message.content.startswith(f">{cmd}"):
            embed = create_embed(message, cmd)
            if isinstance(embed, discord.Embed):
                await message.channel.send(embed=embed)
            else:
                await message.channel.send(embed)


client.run(DISCORD_TOKEN)
