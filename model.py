""" database model
"""

import os

import pymongo
from dotenv import load_dotenv

load_dotenv()
client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = client["gym"]

product = db["product"]
user = db["user"]