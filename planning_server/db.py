from datetime import datetime, timezone

from pymongo import MongoClient
from pymongo.collection import Collection

from planning_server.types import Day


class Database:

    collection: Collection

    def __init__(self):
        CONNECTION_STRING = "mongodb://user:password@localhost:27017"

        client = MongoClient(CONNECTION_STRING)
        self.collection = client.database.days

    def get_day(self, date: datetime | None) -> Day:
        date_to_get = date if date else datetime.now(tz=timezone.utc)
        date_to_get = date_to_get.replace(
            hour=0, minute=0, second=0, microsecond=0)

        day_dict: dict[str, datetime | int] = {"day": date_to_get}
        result = self.collection.find_one(day_dict)
        if result is None:
            self.collection.insert_one(day_dict)
        return Day.from_dict(day_dict)

    def set_items_in_day(self, date: datetime | None, data: dict[str, int]) -> Day:
        date_to_add = date if date else datetime.now(tz=timezone.utc)
        date_to_add = date_to_add.replace(
            hour=0, minute=0, second=0, microsecond=0)

        result: dict[str, datetime | int] | None = self.collection.find_one({"day": date_to_add})
        result = result if result is not None else {"day": date_to_add}
        for field in data:
            result[field] = data[field]

        if result is not None:
            self.collection.replace_one({"day": date_to_add}, result)
        else:
            self.collection.insert_one(result).inserted_id
        return Day.from_dict(result)

    def remove_item_from_day(self, date: datetime | None, item: str) -> Day:
        date_to_remove_from = date if date else datetime.now(tz=timezone.utc)
        date_to_remove_from = date_to_remove_from.replace(
            hour=0, minute=0, second=0, microsecond=0)

        result = self.collection.find_one({"day": date_to_remove_from})
        if result is not None:
            if item in result:
                del result[item]

            self.collection.replace_one({"day": date_to_remove_from}, result)

        return Day.from_dict(result)
