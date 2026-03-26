from bot.database import files_col


async def total_users_count():
    user_ids = await files_col.distinct("user_id")
    return len(user_ids)


async def list_users():
    user_ids = await files_col.distinct("user_id")
    return user_ids


async def total_files_count():
    return await files_col.count_documents({})


async def user_stats(user_id: int):
    return await files_col.count_documents({"user_id": user_id})


async def top_users(limit=5):
    pipeline = [
        {"$group": {"_id": "$user_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit},
    ]
    return await files_col.aggregate(pipeline).to_list(length=limit)

async def is_served_user(user_id: int) -> bool:
    if not files_col:
        return False
    user = await files_col.find_one({"user_id": user_id})
    return bool(user)
