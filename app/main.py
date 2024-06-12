from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, auth
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/books/", response_model=schemas.Book)
def create_book_for_user(
    book: schemas.BookCreate, db: Session = Depends(auth.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    return crud.create_user_book(db=db, book=book, user_id=current_user.id)

@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(auth.get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books
