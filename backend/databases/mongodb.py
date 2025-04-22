from pymongo import MongoClient
from pymongo.collection import Collection
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "research_assistant"

client = MongoClient(MONGO_URI)
db = client["research_assistant"]
conversations_collection = db["conversations"]
research_collection = db["research"]
users_collection = db["users"]

client = None
db = None

# def init_mongo():
#     global client, db
#     client = MongoClient(MONGO_URI)
#     db = client[DB_NAME]
#     db.command("ping")  # Test connection

# def get_collection(collection_name: str) -> Collection:
#     if db is None:
#         init_mongo()
#     return db[collection_name]

def insert_research(data: dict, user_id: str) -> str:
    
    data["user_id"] = user_id
    result = research_collection.insert_one(data)
    return str(result.inserted_id)

def get_user_by_email(email: str) -> dict:
    user = users_collection.find_one({"email": email})
    return user

def insert_user(user: dict) -> str:
    result = users_collection.insert_one(user)
    return str(result.inserted_id)