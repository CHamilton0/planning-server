import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from pymongo import MongoClient

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb://user:password@localhost:27017"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['database']

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Welcome from strawberry"


schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)

# Get the database
dbname = get_database()

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

dbname.test.insert_one({'x': 1})
