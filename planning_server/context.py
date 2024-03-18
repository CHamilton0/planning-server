import asyncio
from typing import Set

from strawberry.fastapi import BaseContext

from planning_server.db import Database
from planning_server.types import Day

class Context (BaseContext):
    database: Database
    day_subscriptions: Set['asyncio.Queue[Day]']

    def __init__(
        self,
        database: Database,
        day_subscriptions: Set['asyncio.Queue[Day]'],
    ) -> None:
        self.database = database
        self.day_subscriptions = day_subscriptions
