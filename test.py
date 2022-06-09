import pymongo as pm
import json
import os
from dotenv import load_dotenv

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

load_dotenv('.env')
mongo_uri = os.getenv('MONGO_URI')
client = pm.MongoClient(mongo_uri, serverSelectionTimeoutMS=100000)
db = client.get_database('SimplePicks')
print(db.list_collection_names())

users = db.Users
print(users)
