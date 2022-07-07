# main file

import json
import os
import platform
import sys
import random
import disnake
import exceptions
import pymongo as pm

from dotenv import load_dotenv
from disnkae import ApplicationCommandInteraction
from disnake.ext import tasks, commands
from disnake.ext.commands import Bot, Context

if not os.path.isfile("config.json"):
    sys.exit("'config.json not found! please add it and try again")
else:
    with open("config.json") as file:
        config = json.load(file)

load_dotenv('../.env')

forex = os.getenv('FOREX_ROLE')
lt = os.getenv('LONG_TERM_ROLE')
crypto = os.getenv('CRYPTO_ROLE')
stock = os.getenv('STOCK_ROLE')
diamond = os.getenv('DIAMOND_ROLE')
mongo_uri = os.getenv('MONGO_URI')

intents = disnake.Intents.default()

bot = Bot(command_prefix=config["prefix"], intents=intents)

# removing default help command
bot.remove_command("help")

# on_ready runs whenever the bot is running


@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user.name}\ndisnake API version: {disnake.__version__}\nPython version: {platform.python_version()}\nRunning on: {platform.system()} {platform.release()} {os.name}\n-----------------")
    curr_guild = bot.guilds
    status_task.start()


@tasks.loop(minutes=0.5)
async def status_task() -> None:
    statuses = ['with you!', 'with Drew', 'with humans!']
    await bot.change_presence(activity=disnake.Game(random.choice(statuses)))


def load_commands(command_type: str) -> None:
    for file in os.listdir(f"./cogs/{command_type}"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{command_type}.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


if __name__ == "__main__":
    load_commands("slash")
    load_commands("normal")
