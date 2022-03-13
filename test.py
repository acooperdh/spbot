import pymongo as pm
import json
import os

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

client = pm.MongoClient(config["mongo_uri"])
db = client.get_database('SimplePicks')
print(db.list_collection_names())

users = db.Users
print(users)
