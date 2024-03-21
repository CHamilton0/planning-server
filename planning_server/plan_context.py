import asyncio
from typing import Set

from planning_server.db import Database
from planning_server.context import Context
from planning_server.types import Day, Item


class PlanContext:
    _database: Database
    _day_subscriptions: Set['asyncio.Queue[Day]']
    _goal_subscriptions: Set['asyncio.Queue[list[Item]]']

    def __init__(self, database: Database) -> None:
        self._database = database
        self._day_subscriptions = set()
        self._goal_subscriptions = set()

    def get_context(self) -> Context:
        return Context(
            database=self._database,
            day_subscriptions=self._day_subscriptions,
            goal_subscriptions=self._goal_subscriptions,
        )
