from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    rating: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    books: list[Book] = []

    class Config:
        orm_mode = True
