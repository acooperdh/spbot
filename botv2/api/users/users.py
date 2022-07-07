import pymongo as pm
import os
import json
import asyncio
import disnake
import time


async def check_user_role(user, role):
    # TODO: mongo uri needs to be imported from .env
    users = pm.MongoClient("mongodb+srv://drew:gangShit420@cluster0.648jx.mongodb.net/SimplePicks?retryWrites=true&w=majority"
                           ).get_database("SimplePicks").Users
    find_user = users.find_one(
        {"discord_id": str(user["name"]) + "#" + str(user["discriminator"])})
    print(find_user)
    if find_user is None or find_user["discord_role"] != role:
        return None
    return find_user

    # # this works for now
    # user = {"name": "Tarek Fahmyy", "discriminator": "1277"}
    # role = "948740878736953404"
    # loop = asyncio.get_event_loop()
    # asyncio.ensure_future(check_user_role(user, role))
    # loop.run_forever()
    # loop.close()


# user = {"name": "Abdulrahman", "discriminator": "2474"}
# role = "948740878736953404"
# loop = asyncio.get_event_loop()
# asyncio.ensure_future(check_user_role(user, role))
# loop.run_forever()
# loop.close()
