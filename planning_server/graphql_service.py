from planning_server.db import Database
import strawberry
from planning_server.graphql import Query, Mutation, Subscription
from planning_server.plan_context import PlanContext
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from datetime import datetime
import asyncio
from typing import AsyncGenerator
from asyncio import Queue
import uvicorn

fast_api: FastAPI = FastAPI()

class GraphqlService:
    http_host: str
    http_port: int

    def __init__(
        self,
        http_host: str,
        http_port: int,
        database: Database,
    ):
        self.http_host = http_host
        self.http_port = http_port

        self.schema = strawberry.Schema(Query, Mutation, Subscription)
        self.context = PlanContext(database=database)
        self.graphql_app: GraphQLRouter = GraphQLRouter(
            self.schema,
            context_getter=self.context.get_context
        )

        fast_api.include_router(self.graphql_app, prefix="/graphql")

    def run_service(self, reload: bool = False) -> None:
        uvicorn.run(
            app="planning_server.graphql_service:fast_api",
            host=self.http_host,
            port=self.http_port,
            loop="asyncio",
            lifespan="on",
            reload=reload,
        )
