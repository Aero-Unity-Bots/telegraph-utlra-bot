# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #

from pymongo import MongoClient
import config
import time


# ---------------- CONNECTION ---------------- #

client = MongoClient(
    config.MONGO_URL,
    serverSelectionTimeoutMS=5000
)

db = client[config.DB_NAME]


# ---------------- COLLECTIONS ---------------- #

users = db.users
posts = db.posts


# ---------------- INDEXES ---------------- #

users.create_index(
    "user_id",
    unique=True
)

posts.create_index(
    "user_id"
)


# ---------------- USER ---------------- #

def add_user(user_id):

    if not user_id:
        return

    users.update_one(
        {"user_id": user_id},
        {
            "$setOnInsert": {
                "user_id": user_id,
                "time": int(time.time())
            }
        },
        upsert=True
    )


# ---------------- POSTS ---------------- #

def save_post(
    user_id,
    url,
    title
):

    posts.insert_one(
        {
            "user_id": user_id,
            "url": url,
            "title": title,
            "time": int(time.time())
        }
    )


# ---------------- STATS ---------------- #

def total_users():

    return users.count_documents({})


def total_posts():

    return posts.count_documents({})


# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #