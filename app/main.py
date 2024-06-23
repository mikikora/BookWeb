from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from . import crud, models, schemas, auth
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(auth.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(auth.get_db)):
    books = crud.get_users(db, skip=skip, limit=limit)
    return books

@app.put("/users/change-password", response_model=schemas.User)
def change_password(password_data: schemas.ChangePassword, db: Session = Depends(auth.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return crud.update_user_password(db, user_id=current_user.id, change_pass=password_data)

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(auth.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    return crud.delete_user(db, user_id=user_id)

@app.post("/books/", response_model=schemas.Book)
def create_book_for_user(
    book: schemas.BookCreate, db: Session = Depends(auth.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    tags = []
    for tag_data in book.tags:
        tag = crud.get_tag_by_name(db, tag_data.name)
        if not tag:
            tag = crud.create_tag(db, tag_data, current_user.id)
        tags.append(tag)
    return crud.create_user_book(db=db, book=book, user_id=current_user.id, tags=tags)

@app.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(auth.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    book = crud.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    return crud.delete_book(db, book_id=book_id)

@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(auth.get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book_for_user(
    book_id: int, book: schemas.BookUpdate, db: Session = Depends(auth.get_db), current_user: schemas.User = Depends(auth.get_current_user)
):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    return crud.update_book(db, book_id=book_id, book=book, user_id=current_user.id)

@app.post("/tags/", response_model=schemas.Tag)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(auth.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    db_tag = crud.get_tag_by_name(db, tag.name)
    if db_tag:
        raise HTTPException(status_code=400, detail="Tag already exists")
    return crud.create_tag(db, tag, current_user.id)

@app.get("/tags/", response_model=list[schemas.Tag])
def read_tags(skip: int = 0, limit: int = 10, db: Session = Depends(auth.get_db)):
    tags = crud.get_tags(db, skip=skip, limit=limit)
    return tags

@app.delete("/tags/{tag_id}", response_model=schemas.Tag)
def delete_tag(tag_id: int, db: Session = Depends(auth.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    tag = crud.get_tag(db, tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag Not found")
    if tag.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    return crud.delete_tag(db, tag_id, current_user.id)
