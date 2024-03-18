from datetime import datetime
import strawberry
from asyncio import Queue
from typing import AsyncGenerator

from strawberry.types import Info
from planning_server.context import Context

@strawberry.type
class Day:
    day: datetime

    def __init__(self, day: datetime):
        self.day = day

@strawberry.input
class Item:
    name: str
    hours: int

@strawberry.type
class Query:
    @strawberry.field
    def day(
        self,
        info: Info[Context, None],
        day: datetime | None,
    ) -> Day:
        result = info.context.database.get_day(day)

        day_result = Day(result.get("day"))

        return day_result
    
@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_day(
        self,
        info: Info[Context, None],
        day: datetime,
        items: list[Item],
    ) -> str:
        data: dict[str, int] = {}

        for item in items:
            data[item.name] = item.hours

        return info.context.database.insert_day(day, data)
    
@strawberry.type
class Subscription:
    @strawberry.subscription
    async def subscribe_day(self, day: datetime) -> AsyncGenerator[Day, None]:
        queue: Queue = Queue()
        # add susbscription to context
        try:
            while True:
                result: Day = await queue.get()
                yield result
        finally:
            # remove susbscription from context
            pass
