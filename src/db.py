# db.py
import os
from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/lango")
client = MongoClient(MONGO_URI)
db = client.get_default_database()