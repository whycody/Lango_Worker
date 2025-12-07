from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/lango")

client = MongoClient(MONGO_URI)
db = client.get_database()