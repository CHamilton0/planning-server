from datetime import datetime, timezone

from pymongo import MongoClient
from pymongo.collection import Collection

from planning_server.types import Day, Item, Goal


class Database:

    days_collection: Collection
    goals_collection: Collection

    def __init__(
        self,
        connection_string: str,
    ):
        client: MongoClient = MongoClient(connection_string)
        self.days_collection = client.database.days
        self.goals_collection = client.database.goals

    def set_goal_times(self, data: list[dict[str, str | float]]) -> list[Goal]:
        self.goals_collection.update_one({}, {'$set': {"goals": data}}, upsert=True)

        goals: list[Goal] = []
        for item_dict in data:
            name = item_dict.get("name")
            min_hours = item_dict.get("min_hours")
            max_hours = item_dict.get("max_hours", None)
            
            goals.append(Goal(name, min_hours, max_hours))

        return goals

    def get_goal_times(self) -> list[Goal]:
        goals_dict: dict | None = self.goals_collection.find_one({})
        if goals_dict is None:
            return []
        assert isinstance(goals_dict, dict)
        goals_list: list[dict[str, str | float]] = goals_dict.get("goals", [])
        assert isinstance(goals_list, list)

        goals: list[Goal] = []
        for item_dict in goals_list:
            name = item_dict.get("name")
            min_hours = item_dict.get("min_hours")
            max_hours = item_dict.get("max_hours", None)
            
            goals.append(Goal(name, min_hours, max_hours))

        return goals

    def get_day(self, date: datetime | None) -> Day:
        date_to_get = date if date else datetime.now(tz=timezone.utc)
        date_to_get = date_to_get.replace(
            hour=0, minute=0, second=0, microsecond=0)

        day_dict: dict[str, datetime | float] = {"day": date_to_get}
        result = self.days_collection.find_one(day_dict)
        if result is None:
            self.days_collection.insert_one(day_dict)
            return Day.from_dict(day_dict)
        return Day.from_dict(result)

    def set_items_in_day(self, date: datetime | None, data: dict[str, float]) -> Day:
        date_to_add = date if date else datetime.now(tz=timezone.utc)
        date_to_add = date_to_add.replace(
            hour=0, minute=0, second=0, microsecond=0)

        result = {"day": date_to_add}
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
