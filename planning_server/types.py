from __future__ import annotations

from datetime import datetime
import strawberry


@strawberry.type
class Item:
    name: str
    hours: int

    def __init__(self, name: str, hours: int):
        self.name = name
        self.hours = hours


@strawberry.type
class Day:
    day: datetime
    items: list[Item]

    def __init__(self, day: datetime, items: list[Item]):
        self.day = day
        self.items = items

    @staticmethod
    def from_dict(dictionary: dict[str, datetime | int]) -> Day:
        date = dictionary.get('day')
        assert isinstance(date, datetime)
        items: list[Item] = []
        for key in dictionary.keys():
            if key == 'day' or key == '_id':
                continue
            value = dictionary[key]
            assert isinstance(value, int)
            items.append(Item(key, value))

        return Day(date, items)


@strawberry.input
class ItemInput:
    name: str
    hours: int
