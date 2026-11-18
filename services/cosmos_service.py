
import os
from azure.cosmos import CosmosClient


def get_container_client():
    endpoint = os.environ["COSMOS_ENDPOINT"]
    key = os.environ["COSMOS_KEY"]
    database_name = os.environ["COSMOS_DATABASE"]
    container_name = os.environ["COSMOS_CONTAINER"]

    client = CosmosClient(endpoint, key)

    database = client.get_database_client(database_name)

    container = database.get_container_client(container_name)

    return container


def get_all_books():
    container = get_container_client()
    return list(container.query_items(
        query="SELECT * FROM c",
        enable_cross_partition_query=True
    ))


def get_book(book_id):
    container = get_container_client()
    return container.read_item(
        item=book_id,
        partition_key=book_id
    )


def add_book(book):
    container = get_container_client()
    return container.upsert_item(book)


def delete_book(book_id):
    container = get_container_client()
    container.delete_item(
        item=book_id,
        partition_key=book_id
    )