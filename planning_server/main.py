from datetime import datetime

import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from planning_server.db import Database

database = Database()

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Welcome from strawberry"
    
@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_day(self, day: datetime) -> str:
        print(day)
        return database.insert_day(day)

schema = strawberry.Schema(Query, Mutation)

graphql_app = GraphQLRouter(schema)


app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
