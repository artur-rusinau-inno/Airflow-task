TOP_5_COMMENTS = [
    {"$group": {"_id": "$content", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 5},
]
LESS_THAN_5_LENGHT_COMMENTS = [
    {"$addFields": {"comment_lenght": {"$strLenCP": "$content"}}},
    {"$match": {"comment_lenght": {"$lt": 5}}},
]
AVG_RATING_EACH_DAY = [
    {"$match": {"rating": {"$ne": "-"}}},
    {
        "$group": {
            "_id": "$created_date",
            "avg_rating": {"$avg": {"$toDouble": "$rating"}},
        }
    },
    {"$addFields": {"timestamp": {"$toLong": {"$toDate": "$_id"}}}},
    {
        "$project": {
            "_id": 0,
            "timestamp": 1,
            "avg_rating": {"$round": ["$avg_rating", 2]},
        }
    },
    {"$sort": {"timestamp": 1}},
]
