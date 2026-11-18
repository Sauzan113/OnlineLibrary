
import azure.functions as func
import json

from azure.cosmos.exceptions import CosmosResourceNotFoundError
from services.cosmos_service import (
    get_all_books,
    get_book,
    add_book,
    delete_book
)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


# GET: Retrieve all books
@app.route(route="books", methods=["GET"])
def get_books(req: func.HttpRequest) -> func.HttpResponse:
    try:
        books = get_all_books()

        return func.HttpResponse(
            json.dumps(books),
            status_code=200,
            mimetype="application/json"
        )
    except Exception:
        return func.HttpResponse(
            "Unable to retrieve books.",
            status_code=500
        )


# GET: Retrieve one book
@app.route(route="books/{book_id}", methods=["GET"])
def get_book_by_id(req: func.HttpRequest) -> func.HttpResponse:
    book_id = req.route_params.get("book_id")

    try:
        book = get_book(book_id)

        return func.HttpResponse(
            json.dumps(book),
            status_code=200,
            mimetype="application/json"
        )
    except CosmosResourceNotFoundError:
        return func.HttpResponse(
            "Book not found.",
            status_code=404
        )
    except Exception:
        return func.HttpResponse(
            "Unable to retrieve the book.",
            status_code=500
        )


# POST: Add a new book
@app.route(route="books", methods=["POST"])
def create_book(req: func.HttpRequest) -> func.HttpResponse:
    try:
        book = req.get_json()

        required_fields = ["id", "title", "author", "category"]

        if not all(book.get(field) for field in required_fields):
            return func.HttpResponse(
                "Please provide id, title, author and category.",
                status_code=400
            )

        saved_book = add_book(book)

        return func.HttpResponse(
            json.dumps(saved_book),
            status_code=201,
            mimetype="application/json"
        )
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON request body.",
            status_code=400
        )
    except Exception:
        return func.HttpResponse(
            "Unable to add the book.",
            status_code=500
        )


# DELETE: Delete a book
@app.route(route="books/{book_id}", methods=["DELETE"])
def remove_book(req: func.HttpRequest) -> func.HttpResponse:
    book_id = req.route_params.get("book_id")

    try:
        delete_book(book_id)

        return func.HttpResponse(
            "Book deleted successfully.",
            status_code=200
        )
    except CosmosResourceNotFoundError:
        return func.HttpResponse(
            "Book not found.",
            status_code=404
        )
    except Exception:
        return func.HttpResponse(
            "Unable to delete the book.",
            status_code=500
        )
