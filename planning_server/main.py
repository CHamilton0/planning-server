from datetime import datetime
import asyncio
from typing import AsyncGenerator
from asyncio import Queue

import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from planning_server.db import Database
from planning_server.graphql import Query, Mutation, Subscription

database = Database()

schema = strawberry.Schema(Query, Mutation, Subscription)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
