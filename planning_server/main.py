
import typer
from planning_server.db import Database
from planning_server.graphql_service import GraphqlService

app = typer.Typer(add_completion=False)


@app.command(context_settings={'terminal_width': 120})
def run(
    http_host: str = typer.Option(
        'localhost',
        envvar='HTTP_HOST',
        help="""HTTP host for the server"""
    ),
    http_port: int = typer.Option(
        8000,
        envvar='HTTP_PORT',
        help="""HTTP port for the server"""
    ),
    mongo_host: str = typer.Option(
        'localhost',
        envvar='MONGO_HOST',
        help="""HTTP host for MongoDB"""
    ),
    mongo_port: int = typer.Option(
        27017,
        envvar='MONGO_PORT',
        help="""HTTP port for MongoDB"""
    ),
    mongo_user: str = typer.Option(
        'user',
        envvar='MONGO_USER',
        help="""User for MongoDB"""
    ),
    mongo_password: str = typer.Option(
        'password',
        envvar='MONGO_PASSWORD',
        help="""Password for MongoDB"""
    ),
    development: bool = typer.Option(
        False,
        envvar='DEVELOPMENT',
        help="""Whether to run the development server"""
    ),
    connection_string: str = typer.Option(
        '',
        envvar='CONNECTION_STRING',
        help="""Connection string for MongoDB"""
    ),
):
    db_connection_string = connection_string if len(connection_string) > 0 else f'mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}'
    database: Database = Database(db_connection_string)

    graphql_service = GraphqlService(http_host, http_port, database, development)
    graphql_service.run_service()
