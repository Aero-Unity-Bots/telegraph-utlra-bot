
# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

from database import users

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def get_user_settings(
    user_id,
    telegram_first_name=None
):

    data = users.find_one(
        {"user_id": user_id}
    )

    account_name = (
        data.get("account_name")
        if data and data.get("account_name")
        else telegram_first_name
    )

    author_name = (
        data.get("author_name")
        if data and data.get("author_name")
        else "Unknown"
    )

    return {
        "account_name": account_name or "User",
        "author_name": author_name
    }

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def reset_user_settings(user_id):

    users.update_one(
        {"user_id": int(user_id)},
        {
            "$unset": {
                "account_name": "",
                "author_name": ""
            }
        }
    )

    return True

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #