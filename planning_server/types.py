from __future__ import annotations

from datetime import datetime
import strawberry


@strawberry.type
class Item:
    name: str
    hours: float

    def __init__(self, name: str, hours: float):
        self.name = name
        self.hours = hours

@strawberry.type
class Goal:
    name: str
    min_hours: float
    max_hours: float | None

    def __init__(self, name: str, min_hours: float, max_hours: float | None = None):
        self.name = name
        self.min_hours = min_hours
        self.max_hours = max_hours
        
@strawberry.type
class Summary:
    name: str
    hours_done: float
    min_hours: float
    max_hours: float | None
    
    def __init__(self, name: str, hours_done: float, min_hours: float, max_hours: float | None = None):
        self.name = name
        self.hours_done = hours_done
        self.min_hours = min_hours
        self.max_hours = max_hours

@strawberry.type
class Day:
    day: datetime
    items: list[Item]

    def __init__(self, day: datetime, items: list[Item]):
        self.day = day
        self.items = items

    @staticmethod
    def from_dict(dictionary: dict[str, datetime | float]) -> Day:
        date = dictionary.get('day')
        assert isinstance(date, datetime)
        items: list[Item] = []
        for key in dictionary.keys():
            if key == 'day' or key == '_id':
                continue
            value = dictionary[key]
            assert isinstance(value, float)
            items.append(Item(key, value))

        return Day(date, items)


@strawberry.input
class ItemInput:
    name: str
    hours: float
    
@strawberry.input
class GoalInput:
    name: str
    min_hours: float
    max_hours: float | None
