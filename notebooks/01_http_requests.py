# https://github.com/codingwithroby/FastAPI-The-Complete-Course
# import: fastapi
from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "math"},
]

# to run the FastAPI app, use `uvicorn notebooks.01_http_requests:app --reload`.
# it will automatically create a swagger UI in the endpoint `docs`.
@app.get("/")
async def first_api():  # removing `async` does not make any change.
    return {"message": "Hello World!"}


@app.get("/books")
async def read_all_books():
    return BOOKS


# order matters in `FastAPLI`.
# if `mybook` is passed in the URL, it will direct to this static endpoint.
# if a value other than `mybook` is passed, it will direct to the endpoint with a path parameter.
@app.get("/books/mybook")
async def read_all_books():
    return {"book_title": "My favorite book."}


# @app.get("/books/{dynamic_param}")
# # type hint in the input defines data type in the request.
# async def read_all_books(dynamic_param: str):
#     return {"dynamic_param": dynamic_param}

# http://127.0.0.1:8000/books/title%20four
# space in URL is represented as `%20`.
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book


# http://127.0.0.1:8000/books?category=science
@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


# http://127.0.0.1:8000/books/author%20two/?category=math
@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if (
            book.get("author").casefold() == book_author.casefold()
            and book.get("category").casefold() == category.casefold()
        ):
            books_to_return.append(book)

    return books_to_return


# import: fastapi
# POST request method
from fastapi import Body


# {"title": "Title Seven", "author": "Author two", "category": "math"}
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


# PUT request method
# {"title": "Title Six", "author": "Author Two", "category": "history"}
@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i, book in enumerate(BOOKS):
        if book.get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book


# DELETE request method
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break


# # with path parameter
# # # http://127.0.0.1:8000/books_assignment/author%20two
# @app.get("/books_assignment/{book_author}")
# async def read_all_books_by_author(book_author: str):
#     books_to_return = []
#     for book in BOOKS:
#         if book.get('author').casefold() == book_author.casefold():
#             books_to_return.append(book)
#     return books_to_return

# with query parameter
# http://127.0.0.1:8000/books_assignment?book_author=author%20two
@app.get("/books_assignment")
async def read_all_books_by_author(book_author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == book_author.casefold():
            books_to_return.append(book)
    return books_to_return
