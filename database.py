
# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

import time
import config
from pymongo import MongoClient, ASCENDING
from pymongo.errors import PyMongoError

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

client = MongoClient(
    config.MONGO_URL,
    serverSelectionTimeoutMS=10000,
    connectTimeoutMS=10000,
    socketTimeoutMS=20000,
    maxPoolSize=10,
    retryWrites=True
)

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

db = client[config.DB_NAME]
users = db["users"]
posts = db["posts"]
force_sub_channels = db["force_sub_channels"]

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

try:
    client.admin.command("ping")
    print("✅ MongoDB connected successfully!")

except PyMongoError as error:
    raise RuntimeError(
        f"MongoDB connection failed: {error}"
    )

users.create_index(
    [("user_id", ASCENDING)],
    unique=True
)

posts.create_index(
    [("user_id", ASCENDING), ("time", ASCENDING)]
)

force_sub_channels.create_index(
    "chat_id",
    unique=True
)

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def add_user(user_id):

    if not user_id:
        return

    users.update_one(
        {"user_id": int(user_id)},
        {
            "$setOnInsert": {
                "user_id": int(user_id),
                "time": int(time.time())
            }
        },
        upsert=True
    )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def save_post(user_id, url, title):

    if not user_id or not url:
        return None

    result = posts.insert_one({
        "user_id": int(user_id),
        "url": url,
        "title": title or "Untitled",
        "time": int(time.time())
    })

    return result.inserted_id

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def total_users():
    return users.count_documents({})

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def total_posts():
    return posts.count_documents({})

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def close_database():
    client.close()

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #