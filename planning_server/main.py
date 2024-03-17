from datetime import datetime

import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from planning_server.db import Database

database = Database()

@strawberry.type
class Day:
    day: datetime

    def __init__(self, day: datetime):
        self.day = day

@strawberry.type
class Query:
    @strawberry.field
    def day(self, day: datetime | None) -> Day:
        result = database.get_day(day)

        day_result = Day(result.get("day"))

        return day_result
    
@strawberry.input
class Item:
    name: str
    hours: int
    
@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_day(
        self,
        day: datetime,
        items: list[Item],
    ) -> str:
        data: dict[str, int] = {}

        for item in items:
            data[item.name] = item.hours

        return database.insert_day(day, data)

schema = strawberry.Schema(Query, Mutation)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
