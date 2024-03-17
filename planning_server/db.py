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
    
    def get_day(self, date: datetime | None):
        date_to_get = date if date else datetime.now(tz=timezone.utc)
        date_to_get = date_to_get.replace(hour=0, minute=0, second=0, microsecond=0)

        result = self.collection.find_one({ "day": date_to_get })
        return result

    def insert_day(self, date: datetime, data: dict[str, int]):
        date_to_add = date if date else datetime.now(tz=timezone.utc)
        date_to_add = date_to_add.replace(hour=0, minute=0, second=0, microsecond=0)

        result = self.collection.find_one({ "day": date_to_add })
        if result is not None:
            for field in data:
                number_to_add = data[field]
                if field in result:
                    result[field] = result[field] + number_to_add
                else:
                    result[field] = number_to_add

            self.collection.replace_one({ "day": date_to_add }, result)

            return result.get("_id")

        return self.collection.insert_one({
            "day": date_to_add
        }).inserted_id
