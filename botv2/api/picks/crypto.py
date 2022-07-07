import pymongo as pm
import os
import json
import requests
from pycoingecko import CoinGeckoAPI
from dotenv import load_dotenv
import time
cg = CoinGeckoAPI()
print(len(cg.get_coins_list()))
for i in range(100):
    price = cg.get_price(ids="bitcoin,litecoin,ethereum", vs_currencies="usd")
    print(price)
    time.sleep(15)


async def create_position()
