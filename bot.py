""""
Copyright © Krypton 2021 - https://github.com/kkrypt0nn (https://krypt0n.co.uk)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""

import json
import os
import platform
import random
import sys
import disnake

from dotenv import load_dotenv
from disnake import ApplicationCommandInteraction
from disnake.ext import tasks, commands
from disnake.ext.commands import Bot
from disnake.ext.commands import Context

import exceptions
import pymongo as pm

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)
load_dotenv('.env')

# global variables used for role assignment
forex = os.getenv('FOREX_ROLE')
lt = os.getenv('LONG_TERM_ROLE')
crypto = os.getenv('CRYPTO_ROLE')
stock = os.getenv('STOCK_ROLE')
diamond = os.getenv('DIAMOND_ROLE')
mongo_uri = os.getenv('MONGO_URI')
"""
Setup bot intents (events restrictions)
For more information about intents, please go to the following websites:
https://docs.disnake.dev/en/latest/intents.html
https://docs.disnake.dev/en/latest/intents.html#privileged-intents


Default Intents:
intents.bans = True
intents.dm_messages = False
intents.dm_reactions = False
intents.dm_typing = False
intents.emojis = True
intents.guild_messages = True
intents.guild_reactions = True
intents.guild_typing = False
intents.guilds = True
intents.integrations = True
intents.invites = True
intents.reactions = True
intents.typing = False
intents.voice_states = False
intents.webhooks = False

Privileged Intents (Needs to be enabled on dev page), please use them only if you need them:
intents.members = True
intents.messages = True
intents.presences = True
"""

intents = disnake.Intents.default()

bot = Bot(command_prefix=config["prefix"], intents=intents)


@bot.event
async def on_ready() -> None:
    """
    The code in this even is executed when the bot is ready
    """
    print(f"Logged in as {bot.user.name}")
    print(f"disnake API version: {disnake.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    curr_guild = bot.guilds
    for role in curr_guild[0].roles:
        print(f"name: {role.name} id: {role.id}")
    print("--------------------")
    channels = bot.guilds[0].channels
    chnl = None
    for channel in channels:
        if channel.id == 953863639310417980:
            chnl = channel
        print(f"name: {channel.name} id: {channel.id}")
    print("--------------------")
    # this code is used to send the role message to the role channel,
    # which is used to allow users to assign their own roles
    print(f"Current channel: {chnl.name}")
    # text = "React to this message with the proper emoji to get a role!" + \
    #     "\n💎 - Diamond Picks \n\n" + "💰 - Gold Picks Crypto \n\n📈 - Gold Picks Stocks \n\n" + \
    #     "💹 - Silver Picks Forex \n\n 📅 - Silver Picks Long Term \n"
    # msg = await chnl.send(content=text)
    # await msg.add_reaction("💎")
    # await msg.add_reaction("💰")
    # await msg.add_reaction("📈")
    # await msg.add_reaction("💹")
    # await msg.add_reaction("📅")
    status_task.start()


@tasks.loop(minutes=1.0)
async def status_task() -> None:
    """
    Setup the game status task of the bot
    """
    statuses = ["with you!", "with Krypton!", "with humans!"]
    await bot.change_presence(activity=disnake.Game(random.choice(statuses)))


# Removes the default help command of discord.py to be able to create our
# custom help command.
bot.remove_command("help")


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
    """
    This will automatically load slash commands and normal commands located in their respective folder.

    If you want to remove slash commands, which is not recommended due to the Message Intent being a privileged intent, you can remove the loading of slash commands below.
    """
    load_commands("slash")
    load_commands("normal")


@bot.event
async def on_message(message: disnake.Message) -> None:
    """
    The code in this event is executed every time someone sends a message, with or without the prefix
    :param message: The message that was sent.
    """
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)


# on_reaction_add(reactionn: disnake.Reaction, user: disnake.User)
# on_raw_reaction_add(payload: disnake.RawReactionActionEvent)

async def remove_wrong_reaction(payload: disnake.RawReactionActionEvent) -> None:
    """
    This function is used to remove the wrong reaction that was added.
    :param payload: The payload of the reaction that was added.
    """
    channel = bot.get_channel(payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)
    await msg.remove_reaction(payload.emoji, payload.member)

# TODO: Move these events into their own class / file
# makes more sense for code organization


@bot.event
async def on_raw_reaction_add(payload: disnake.RawReactionActionEvent) -> None:
    if payload.message_id != 955966311450685520:
        return
    role_reaction = payload.emoji.name
    user = payload.member
    print(payload)
    if payload.member.name == 'SimplePicks' and payload.member.discriminator == '4406':
        return
    if role_reaction == "💎":
        print("Diamond selected by " + user.name)
        role_value = diamond
    elif role_reaction == "💰":
        print("Crypto selected by " + user.name)
        role_value = crypto
    elif role_reaction == "📈":
        print("Stock selected by " + user.name)
        role_value = stock
    else:
        print("No role selected by " + user.name)
        if payload.message_id == 955966311450685520:
            await remove_wrong_reaction(payload)
        return

    users = pm.MongoClient(str(mongo_uri)).get_database("SimplePicks").Users
    user_data = users.find_one(
        {"discord_id": str(payload.member.name + "#" + payload.member.discriminator)})

    if user_data is None:
        print("user is not in the database, they need to sign up online")
    else:
        if user_data["discord_role"] == role_value:
            print("user already has the role ... no need to add it")
            await user.add_roles(disnake.Object(id=role_value))
            await remove_wrong_reaction(payload)
            print("role added")
        else:
            print(
                "user is not supposed to have this role, they are supposed to have another role " +
                user_data["discord_id"])
            channel = bot.get_channel(payload.channel_id)
            print("channel on removing reaction role")
            print(channel)
            print("msg on removing reaction role")
            msg = await channel.fetch_message(payload.message_id)
            print(msg)
            await remove_wrong_reaction(payload)


@bot.event
async def on_slash_command(interaction: ApplicationCommandInteraction) -> None:
    """
    The code in this event is executed every time a slash command has been *successfully* executed
    :param interaction: The slash command that has been executed.
    """
    print(
        f"Executed {interaction.data.name} command in {interaction.guild.name} (ID: {interaction.guild.id}) by {interaction.author} (ID: {interaction.author.id})")


@bot.event
async def on_slash_command_error(interaction: ApplicationCommandInteraction, error: Exception) -> None:
    """
    The code in this event is executed every time a valid slash command catches an error
    :param interaction: The slash command that failed executing.
    :param error: The error that has been faced.
    """
    if isinstance(error, exceptions.UserBlacklisted):
        """
        The code here will only execute if the error is an instance of 'UserBlacklisted', which can occur when using
        the @checks.is_owner() check in your command, or you can raise the error by yourself.

        'hidden=True' will make so that only the user who execute the command can see the message
        """
        embed = disnake.Embed(
            title="Error!",
            description="You are blacklisted from using the bot.",
            color=0xE02B2B
        )
        print("A blacklisted user tried to execute a command.")
        return await interaction.send(embed=embed, ephemeral=True)
    elif isinstance(error, commands.errors.MissingPermissions):
        embed = disnake.Embed(
            title="Error!",
            description="You are missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to execute this command!",
            color=0xE02B2B
        )
        print("A blacklisted user tried to execute a command.")
        return await interaction.send(embed=embed, ephemeral=True)
    raise error


@bot.event
async def on_command_completion(context: Context) -> None:
    """
    The code in this event is executed every time a normal command has been *successfully* executed
    :param context: The context of the command that has been executed.
    """
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    print(
        f"Executed {executed_command} command in {context.guild.name} (ID: {context.message.guild.id}) by {context.message.author} (ID: {context.message.author.id})")


@bot.event
async def on_command_error(context: Context, error) -> None:
    """
    The code in this event is executed every time a normal valid command catches an error
    :param context: The normal command that failed executing.
    :param error: The error that has been faced.
    """
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = disnake.Embed(
            title="Hey, please slow down!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = disnake.Embed(
            title="Error!",
            description="You are missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to execute this command!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = disnake.Embed(
            title="Error!",
            description=str(error).capitalize(),
            # We need to capitalize because the command arguments have no
            # capital letter in the code.
            color=0xE02B2B
        )
        await context.send(embed=embed)
    raise error


# Run the bot with the token
token = os.getenv('DISCORD_TOKEN')
bot.run(token)
