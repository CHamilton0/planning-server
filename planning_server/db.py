from datetime import datetime, timezone

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

class Database:
   
    collection: Collection
   
    def __init__(self):
        CONNECTION_STRING = "mongodb://user:password@localhost:27017"
        
        client = MongoClient(CONNECTION_STRING)
        self.collection = client.database.days

    def insert_day(self, date: datetime | None):
        today_date = date if date else datetime.now(tz=timezone.utc)
        today_date = today_date.replace(hour=0, minute=0, second=0, microsecond=0)

        result = self.collection.find_one({ "day": today_date })
        if result is not None:
            return result.get("_id")

        return self.collection.insert_one({
            "day": today_date
        }).inserted_id
