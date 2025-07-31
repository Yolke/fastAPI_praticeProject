from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()

class Livre(BaseModel):
    title: str
    author: str
    read: bool = False

class User(BaseModel):
    name: str
    email:  str

items = []

users: dict[int,User] = {}
books_by_user: dict[int,list[Livre]] = {}

@app.post("/users")
def add_user(user: User): 
    user_id =  len(users)
    users[user_id] = user
    books_by_user[user_id] = []
    return {"user_id": len(users) - 1, "user": user}

@app.post("/users/{user_id}/books")
def add_book_to_user(user_id: int, book: Livre):
    if user_id not in users:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    books_by_user[user_id].append(book)
    return {"message": f"Book '{book.title}' added to user {user_id}"}


@app.get("/users/{user_id}/books")
def list_books_of_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    return books_by_user[user_id]

@app.put("/users/{user_id}/books/{book_id}")
def mark_book_as_read(user_id: int, book_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    user_books = books_by_user[user_id]
    if book_id >= len(user_books):
        raise HTTPException(status_code=404, detail=f"Book {book_id} not found")

    user_books[book_id].read = True
    return {"message": f"Book {book_id} marked as read for user {user_id}"}

@app.delete("/users/{user_id}/books/{book_id}")
def delete_book_of_user(user_id: int, book_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    user_books = books_by_user[user_id]
    if book_id >= len(user_books):
        raise HTTPException(status_code=404, detail=f"Book {book_id} not found")

    deleted = user_books.pop(book_id)
    return {"message": f"Deleted book '{deleted.title}' for user {user_id}"}


@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/books", response_model=list[Livre])
def listLivre(limit: int = 10):
    return items[0:limit]

@app.get("/books/{book_id}",response_model=Livre)
def get_item(book_id: int) -> Livre:
    if book_id < len(items):
        return items[book_id]
    else:
        raise HTTPException(status_code=404, detail=f"Book {book_id} not found")
    
@app.post("/books")
def add_item(books : Livre):
    items.append(books)
    return items

@app.delete("/books/{book_id}")
def delete_item(book_id: int):
    if book_id < len(items):
        del items[book_id] #Synthaxe fausse ? items.pop(book_id)?
        return {"message": "Book deleted", "book":items[book_id]}
    raise HTTPException(status_code=404, detail=f"Book {book_id} not found")

@app.put("/books/{book_id}/read", response_model=Livre)
def mark_as_read(book_id: int):
    if book_id < len(items):
        items[book_id].read = True
        return items[book_id]
    raise HTTPException(status_code=404, detail=f"Book {book_id} not found")





