TOP_5_COMMENTS = [
    {"$group": {"_id": "$content", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 5},
]
LESS_THAN_5_LENGHT_COMMENTS = [
    {"$addFields": {"comment_lenght": {"$strLenCP": "$content"}}},
    {"$match": {"comment_lenght": {"$lt": 5}}},
]
