from datetime import datetime
import strawberry
from asyncio import Queue
from typing import AsyncGenerator

from strawberry.types import Info
from planning_server.context import Context
from planning_server.types import Day, ItemInput, Item


@strawberry.type
class Query:
    @strawberry.field
    def day(
        self,
        info: Info[Context, None],
        day: datetime | None,
    ) -> Day:
        result: Day = info.context.database.get_day(day)

        return result
    
    @strawberry.field
    def goals(
        self,
        info: Info[Context, None],
    ) -> list[Item]:
        result: list[Item] = info.context.database.get_goal_times()

        return result


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def set_day_items(
        self,
        info: Info[Context, None],
        day: datetime | None,
        items: list[ItemInput],
    ) -> Day:
        data: dict[str, int] = {}

        for item in items:
            data[item.name] = item.hours

        day_with_items: Day = info.context.database.set_items_in_day(day, data)

        for day_subscription in info.context.day_subscriptions:
            await day_subscription.put(day_with_items)

        return day_with_items

    @strawberry.mutation
    async def remove_item_from_day(
        self,
        info: Info[Context, None],
        day: datetime | None,
        item: str,
    ) -> Day:
        day_with_removed_item: Day = info.context.database.remove_item_from_day(
            day, item)

        for day_subscription in info.context.day_subscriptions:
            await day_subscription.put(day_with_removed_item)

        return day_with_removed_item

    @strawberry.mutation
    async def set_goals(
        self,
        info: Info[Context, None],
        items: list[ItemInput],
    ) -> list[Item]:
        items_dict = {}
        for item in items:
            items_dict[item.name] = item.hours

        return_items = info.context.database.set_goal_times(items_dict)

        for goal_subscription in info.context.goal_subscriptions:
            await goal_subscription.put(return_items)

        return return_items


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def subscribe_day(
        self,
        info: Info[Context, None],
        day: datetime | None,
    ) -> AsyncGenerator[Day, None]:
        queue: Queue = Queue()
        info.context.day_subscriptions.add(queue)

        if day is None:
            day = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

        try:
            while True:
                result: Day = await queue.get()

                if (result.day.replace(hour=0, minute=0, second=0, microsecond=0).timestamp() ==
                        day.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()):
                    yield result
        finally:
            info.context.day_subscriptions.remove(queue)
            pass

    @strawberry.subscription
    async def subscribe_goals(
        self,
        info: Info[Context, None],
    ) -> AsyncGenerator[list[Item], None]:
        queue: Queue = Queue()
        info.context.goal_subscriptions.add(queue)

        try:
            while True:
                result: list[Item] = await queue.get()
                yield result
        finally:
            info.context.goal_subscriptions.remove(queue)
            pass
