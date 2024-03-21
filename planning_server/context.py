import asyncio
from typing import Set

from strawberry.fastapi import BaseContext

from planning_server.db import Database
from planning_server.types import Day, Item

class Context (BaseContext):
    database: Database
    day_subscriptions: Set['asyncio.Queue[Day]']
    goal_subscriptions: Set['asyncio.Queue[list[Item]]']

    def __init__(
        self,
        database: Database,
        day_subscriptions: Set['asyncio.Queue[Day]'],
        goal_subscriptions: Set['asyncio.Queue[list[Item]]'],
    ) -> None:
        self.database = database
        self.day_subscriptions = day_subscriptions
        self.goal_subscriptions = goal_subscriptions
