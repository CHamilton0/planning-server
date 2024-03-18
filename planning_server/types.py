from datetime import datetime
import strawberry

from strawberry.types import Info

@strawberry.type
class Day:
    day: datetime

    def __init__(self, day: datetime):
        self.day = day

@strawberry.input
class Item:
    name: str
    hours: int
