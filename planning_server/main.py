from datetime import datetime
import asyncio
from typing import AsyncGenerator
from asyncio import Queue

import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from planning_server.db import Database
from planning_server.graphql import Query, Mutation, Subscription
from planning_server.plan_context import PlanContext

database = Database()

schema = strawberry.Schema(Query, Mutation, Subscription)

context = PlanContext(database=database)

graphql_app = GraphQLRouter(
    schema,
    context_getter=context.get_context
)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
