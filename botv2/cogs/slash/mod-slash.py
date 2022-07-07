import json
import os
import sys

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands

if not os.path.isfile("config.json"):
    print("fucking idiot forgot the config.json file")
else:
    with open("config.json") as file:
        config = json.load(file)


class Mod(commands.Cog, name="mod-slash"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="nick",
        description="Change the nickname of a user",
        options=[
            Option(
                name="user",
                description="The user to change the nickname of",
                type=OptionType.user,
                required=True,
            ),
            Option(
                name="nickname",
                description="The nickname to change the user to",
                type=OptionType.string,
                required=True,
            )
        ],
    )
    async def nick(self, interaction: ApplicationCommandInteraction, user: disnake.User, nickname: str = "") -> None:
        member = await interaction.guild.get_or_fetch_member(user.id)

        try:
            await member.edit(nick=nickname)
            embed = disnake.Embed(
                title="Changed Nickname!",
                description=f"**{member}'s** new nickname is **{nickname}**!",
                color=0x9C84EF
            )
            await interaction.send(embed=embed)
        except BaseException:
            embed = disnake.Embed(
                title="Error",
                description="An error occured while trying to change the nickname of the user"
            )
            await interaction.send_embed(embed)


def setup(bot):
    bot.add_cog(Mod(bot))
