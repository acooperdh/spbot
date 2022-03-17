""""
Copyright © Krypton 2021 - https://github.com/kkrypt0nn (https://krypt0n.co.uk)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""

import json
import os
import random
import sys

import aiohttp
import disnake
from dotenv import load_dotenv
from disnake.ext import commands
from disnake.ext.commands import Context
from disnake.abc import Snowflake
import pymongo as pm
from helpers import checks
import pprint
if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)
load_dotenv('../../.env')

forex = os.getenv('FOREX_ROLE')
lt = os.getenv('LONG_TERM_ROLE')
crypto = os.getenv('CRYPTO_ROLE')
stock = os.getenv('STOCK_ROLE')
diamond = os.getenv('DIAMOND_ROLE')


class Choice(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.choice = None

    @disnake.ui.button(label="Forex", style=disnake.ButtonStyle.blurple)
    async def confirm(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.lower()
        self.stop()

    @disnake.ui.button(label="Long Term", style=disnake.ButtonStyle.blurple)
    async def cancel(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.lower()
        self.stop()

    @disnake.ui.button(label="Crypto", style=disnake.ButtonStyle.blurple)
    async def cancel(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.lower()
        self.stop()


class RoleSelect(disnake.ui.Select):
    def __init__(self):

        options = [
            disnake.SelectOption(
                label="Forex", description="Silver Picks - Forex Plan", emoji="💹", value=forex
            ),
            disnake.SelectOption(
                label="Long Term", description="Silver Picks - Long Term Plan", emoji="📆", value=lt
            ),
            disnake.SelectOption(
                label="Crypto", description="Gold Picks - Crypto Plan", emoji="👛", value=crypto
            ),
            disnake.SelectOption(
                label="Equities", description="Gold Picks - Stocks Plan", emoji="📈", value=stock
            ),
            disnake.SelectOption(
                label="Diamond", description="Diamond Picks", emoji="💎", value=diamond
            )
        ]

        super().__init__(
            placeholder="Choose your plan!",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        users = pm.MongoClient(config["mongo_uri"]).get_database(
            'SimplePicks').Users
        user_choice = self.values[0]
        result_embed = disnake.Embed(color=0x9C84EF)
        result_embed.set_author(
            name=interaction.author.display_name, icon_url=interaction.author.avatar.url)
        # this is adding a trial role to the user

        # check user collection to determine if this user has a trial role
        # and if not then deny them access to the role
        user_string = str(interaction.author.name) + "#" + \
            str(interaction.author.discriminator)
        user_collection_data = users.find_one(
            {"discord_id": user_string})

        if user_collection_data is None:
            result_embed.description = f"You currently are not a member of this plan. If you wish to subscribe, please visit our website or contact an admin member and we would be more then happy to help! http://www.simplepicks.io "
        else:
            # if so then add role to user
            check_role = disnake.Object(int(user_choice))
            if interaction.author.get_role(int(user_choice)) is None:
                await interaction.author.add_roles(check_role)
            result_embed.description = f"hey {interaction.author} congrats! You have membership {user_collection_data}"
        await interaction.response.defer()
        await interaction.edit_original_message(embed=result_embed, content=None, view=None)


class RoleSelectView(disnake.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(RoleSelect())


class Fun(commands.Cog, name="role-normal"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="roles",
        description="Set your role in the server."
    )
    async def assign_role(self, context: Context) -> None:
        """
        Allow user to assign their role -- checks user's current role in MongoDB.
        :param context: The context in which the command has been executed.
        """
        view = RoleSelectView()
        await context.send("Please select your current plan", view=view)


def setup(bot):
    bot.add_cog(Fun(bot))
