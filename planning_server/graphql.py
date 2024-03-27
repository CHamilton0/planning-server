from datetime import datetime, timedelta, timezone
import strawberry
from asyncio import Queue
from typing import AsyncGenerator

from strawberry.types import Info
from planning_server.context import Context
from planning_server.types import Day, ItemInput, Item, GoalInput, Goal, Summary


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
    ) -> list[Goal]:
        result: list[Goal] = info.context.database.get_goal_times()

        return result
    
    @strawberry.field
    def weekly_summary(
        self,
        info: Info[Context, None],
        day: datetime | None,
    ) -> list[Summary]:
        goals: list[Goal] = info.context.database.get_goal_times()
        
        date_to_get = day if day else datetime.now(timezone=timezone.utc)
        date_to_get = date_to_get.replace(
            hour=0, minute=0, second=0, microsecond=0)
        
        week = [date_to_get + timedelta(days=x) for x in range(0, -7, -1)]

        days: list[Day] = [info.context.database.get_day(weekday) for weekday in week]
        
        summaries: list[Summary] = []
        for goal in goals:
            name = goal.name
            min_hours = goal.min_hours
            max_hours = goal.max_hours
            
            hours_done = 0
            for day_data in days:
                hours_this_day = next((item for item in day_data.items if item.name == name), None)           
                if hours_this_day is None:
                    continue
                
                hours_done += hours_this_day.hours

            summaries.append(Summary(name, hours_done, min_hours, max_hours))
        
        return summaries


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def set_day_items(
        self,
        info: Info[Context, None],
        day: datetime | None,
        items: list[ItemInput],
    ) -> Day:
        data: dict[str, float] = {}

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
        items: list[GoalInput],
    ) -> list[Goal]:
        items_list: list[dict[str, str | float]] = []
        for item in items:
            items_dict = {}
            items_dict["name"] = item.name
            items_dict["min_hours"] = item.min_hours
            items_dict["max_hours"] = item.max_hours
            
            items_list.append(items_dict)
        
        return_items = info.context.database.set_goal_times(items_list)

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
