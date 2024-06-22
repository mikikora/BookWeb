from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash, verify_password
from typing import List

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user_password(db: Session, user_id: int, change_pass: schemas.ChangePassword):
    user = get_user(db, user_id)
    if not user or not verify_password(change_pass.old_password, user.hashed_password):
        return None
    user.hashed_password = get_password_hash(change_pass.new_password)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        for book in user.books:
            db.delete(book)

        tags = db.query(models.Tag).filter(models.Tag.owner_id == user_id).all()
        for tag in tags:
            db.delete(tag)

        db.delete(user)
        db.commit()
    return user

def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def create_user_book(db: Session, book: schemas.BookCreate, user_id: int, tags: List[schemas.Tag]):
    db_book = models.Book(**book.dict(), owner_id=user_id, tags=tags)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book: schemas.BookUpdate, user_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        return None
    
    if book.title is not None:
        db_book.title = book.title
    if book.author is not None:
        db_book.author = book.author
    if book.rating is not None:
        db_book.rating = book.rating
    if book.comment is not None:
        db_book.comment = book.comment

    if book.tags is not None:
        for tag_data in book.tags:
            tag = get_tag_by_name(db, tag_data.name)
            if not tag:
                tag = create_tag(db, tag_data, user_id)
            if tag in db_book.tags:
                continue
            db_book.tags.append(tag)
    
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
    return book

def get_tags(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Tag).offset(skip).limit(limit).all()

def create_tag(db: Session, tag: schemas.TagCreate, user_id: int):
    db_tag = models.Tag(**tag.dict(), owner_id=user_id)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def get_tag_by_name(db: Session, name: str):
    return db.query(models.Tag).filter(models.Tag.name == name).first()

def get_tag(db: Session, tag_id: int):
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()

def delete_tag(db: Session, tag_id: int, user_id: int):
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id, models.Tag.owner_id == user_id).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag

