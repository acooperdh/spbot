""""
Copyright © Krypton 2021 - https://github.com/kkrypt0nn (https://krypt0n.co.uk)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""

import json
import os
import sys
import disnake


from dotenv import load_dotenv
from pathlib import Path
from disnake import ApplicationCommandInteraction, OptionType, Option
from disnake.ext import commands
import pymongo
from pymongo import MongoClient
from helpers import checks

# Only if you want to use variables that are in the config.json file.
if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

dotenv_path = Path('../../.env')
load_dotenv(dotenv_path)


client = MongoClient(os.getenv("MONGO_URI"))

# Here we name the cog and create a new class for the cog.


class Picks(commands.Cog, name="picks-slash"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide
    # "self" as first parameter.
    @commands.slash_command(
        name="setpick",
        description="Use this command to set a position",
        guild_ids=[909632077039829052],
        options=[
            Option(
                name="type",
                description="Buy or Sell",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="Ticker",
                description="gives the format for the pick you wish to make",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="Entry",
                description="gives the entry price for the pick you wish to make",
                type=OptionType.number,
                required=True
            ),
            Option(
                name="price_target",
                description="price target for position",
                type=OptionType.number,
                required=True
            ),
            Option(
                name="risk",
                description="mental stoploss",
                type=OptionType.number,
                required=True
            ),
            Option(
                name="hold_time",
                description="holding period",
                type=OptionType.string,  # string that hsould be converted to a number once inputted,
                required=False
            ),
            Option(
                name="mental_stoploss",
                description="mental stoploss",
                type=OptionType.number,
                required=False
            ),
            Option(
                name="actual_stoploss",
                description="stoploss",
                type=OptionType.number,
                required=False
            )
        ]
    )
    # This will only allow non-blacklisted members to execute the command
    async def setpick(self, interaction: ApplicationCommandInteraction, type: str, ticker: str, entry: float, price_target: float, risk: float, hold_time: str = "", mental_stoploss: float = 0.0, actual_stoploss: float = 0.0):
        """
        This command does it all
        Note: This is a SLASH command
        :param interaction: sets a pick
        """
        # client = await MongoClient(config["mongo_url"])
        # db = client.position
        # print(db)
        send_message = await interaction.send("Setting Pick")
        print(type)
        print(ticker)
        print(price_target)
        # Do your stuff here
        embed = disnake.Embed(
            title=f"{type} {ticker} @ {entry}",
            description=f"{type} {ticker} @ {entry} \n PT: {price_target} \n Risk: {risk*100}%\n Hold Time: {hold_time} \n{mental_stoploss} \n{actual_stoploss}",
            color=0x00ff00
        )
        await interaction.send(embed=embed)
        # Don't forget to remove "pass", that's just because there's no content
        # in the method.
        pass


# And then we finally add the cog to the bot so that it can load, unload,
# reload and use it's content.
def setup(bot):
    bot.add_cog(Picks(bot))
