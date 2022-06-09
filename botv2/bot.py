# need to import cogs and exceptions as well as helper functions
# we want this bot to do it all so its going to have a decent amount going on
# first thing is first - we want to make sure the bot can handle the
# current role setup that we are using

# imports needed for the bot
import json
import os
import platform
import sys
import random
import disnake
import pymongo as pm
from api.users.users import check_user_role
from dotenv import load_dotenv
from disnake import ApplicationCommandInteraction
from disnake.ext import tasks, commands
from disnake.ext.commands import Bot, Context


# import the config file & dotenv file to get the bot token
if not os.path.isfile("config.json"):
    sys.exit("'config.json not found! please add it and try again")
else:
    with open("config.json") as file:
        config = json.load(file)

load_dotenv('.env')

forex = os.getenv('FOREX_ROLE')
lt = os.getenv('LONG_TERM_ROLE')
crypto = os.getenv('CRYPTO_ROLE')
stock = os.getenv('STOCK_ROLE')
diamond = os.getenv('DIAMOND_ROLE')
free_member = os.getenv('FREE_MEMBER_ROLE')
mongo_uri = os.getenv('MONGO_URI')

intents = disnake.Intents.default()
intents.members = True
bot = Bot(command_prefix=config["prefix"], intents=intents)

guilds = []
roles = []
channels = []
# removing default help command
bot.remove_command("help")

# on_ready runs whenever the bot is running


@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user.name}\ndisnake API version: {disnake.__version__}\nPython version: {platform.python_version()}\nRunning on: {platform.system()} {platform.release()} {os.name}\n-----------------")
    curr_guild = bot.guilds[0]
    for role in curr_guild.roles:
        print(role)
        roles.append(role)
    for role in roles:
        print("role: " + role.name + " id: " + str(role.id))
    for channel in curr_guild.channels:
        channels.append(channel)


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


@bot.event
async def on_slash_command(interaction: ApplicationCommandInteraction) -> None:
    print(
        f"Executed {interaction.data.name} command in {interaction.guild_id} by {interaction.author}")
    return


@bot.event
async def on_member_join(member: disnake.Member) -> None:
    print(f"Member joined: {member.name}")

    free_member = "973929610389626930"
    await member.add_roles(disnake.Object(id=free_member))
    return None


@bot.event
async def on_raw_reaction_add(payload: disnake.RawReactionActionEvent) -> None:
    if payload.message_id != 955966311450685520:
        return None
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
    # check the users information in the database.
    user = {"name": user.name, "discriminator": user.discriminator}
    user_info = await check_user_role(user, role_value)
    print(user_info)
    if user_info is None:
        print("User was not found in the database -- the have not signed up for a plan")
    elif user_info["discord_role"] == role_value:
        # now that we know the user check to see if they already have the role assigned
        if user.roles.length == 0:
            print("User does not have the role assigned")
            await user.add_roles(disnake.Object(id=role_value))
            print(f"Role {role_value} added to user")
        else:
            role_found = False
            for role in user.roles:
                if role.id == role_value:
                    print("User already has the role assigned")
                    role_found = True
                    break
            if not role_found:
                print("User does not have the role assigned")
                await user.add_roles(disnake.Object(id=role_value))
                print(f"Role {role_value} added to user")

    await remove_wrong_reaction(payload)
    return None


async def remove_wrong_reaction(payload: disnake.RawReactionActionEvent):
    channel = bot.get_channel(payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)
    await msg.remove_reaction(payload.emoji, payload.member)

if __name__ == "__main__":
    print('hello world')
    load_commands("slash")

token = os.getenv('DISNAKE_TOKEN')
bot.run(token)
