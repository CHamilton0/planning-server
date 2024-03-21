from datetime import datetime, timezone

from pymongo import MongoClient
from pymongo.collection import Collection

from planning_server.types import Day, Item


class Database:

    days_collection: Collection
    goals_collection: Collection

    def __init__(self):
        CONNECTION_STRING = "mongodb://user:password@localhost:27017"

        client = MongoClient(CONNECTION_STRING)
        self.days_collection = client.database.days
        self.goals_collection = client.database.goals

    def set_goal_times(self, data: dict[str, int]) -> list[Item]:
        self.goals_collection.update_one({}, {'$set': data}, upsert=True)

        items: list[Item] = []
        for (name, hours) in data.items():
            items.append(Item(name, hours))

        return items

    def get_goal_times(self) -> list[Item]:

        return []

    def get_day(self, date: datetime | None) -> Day:
        date_to_get = date if date else datetime.now(tz=timezone.utc)
        date_to_get = date_to_get.replace(
            hour=0, minute=0, second=0, microsecond=0)

        day_dict: dict[str, datetime | int] = {"day": date_to_get}
        result = self.days_collection.find_one(day_dict)
        if result is None:
            self.days_collection.insert_one(day_dict)
        return Day.from_dict(day_dict)

    def set_items_in_day(self, date: datetime | None, data: dict[str, int]) -> Day:
        date_to_add = date if date else datetime.now(tz=timezone.utc)
        date_to_add = date_to_add.replace(
            hour=0, minute=0, second=0, microsecond=0)

        result: dict[str, datetime | int] | None = self.days_collection.find_one({"day": date_to_add})
        result = result if result is not None else {"day": date_to_add}
        for field in data:
            result[field] = data[field]

        if result is not None:
            self.days_collection.replace_one({"day": date_to_add}, result)
        else:
            self.days_collection.insert_one(result).inserted_id
        return Day.from_dict(result)

    def remove_item_from_day(self, date: datetime | None, item: str) -> Day:
        date_to_remove_from = date if date else datetime.now(tz=timezone.utc)
        date_to_remove_from = date_to_remove_from.replace(
            hour=0, minute=0, second=0, microsecond=0)

        result = self.days_collection.find_one({"day": date_to_remove_from})
        if result is not None:
            if item in result:
                del result[item]

            self.days_collection.replace_one(
                {"day": date_to_remove_from}, result)

        return Day.from_dict(result)
