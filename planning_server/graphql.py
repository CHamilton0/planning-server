from datetime import datetime
import strawberry
from asyncio import Queue
from typing import AsyncGenerator

from strawberry.types import Info
from planning_server.context import Context
from planning_server.types import Day, Item

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
    async def add_day(
        self,
        info: Info[Context, None],
        day: datetime,
        items: list[Item],
    ) -> str:
        data: dict[str, int] = {}

        for item in items:
            data[item.name] = item.hours

        for day_subscription in info.context.day_subscriptions:
            await day_subscription.put(day)

        return info.context.database.insert_day(day, data)
    
@strawberry.type
class Subscription:
    @strawberry.subscription
    async def subscribe_day(
        self,
        info: Info[Context, None],
        day: datetime,
    ) -> AsyncGenerator[Day, None]:
        queue: Queue = Queue()
        info.context.day_subscriptions.add(queue)
        try:
            while True:
                result: Day = await queue.get()
                yield result
        finally:
            info.context.day_subscriptions.remove(queue)
            pass
