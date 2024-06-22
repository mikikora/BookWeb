from pydantic import BaseModel
from typing import Optional, List

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class BookBase(BaseModel):
    title: str
    author: str
    rating: int
    comment: Optional[str] = None

class BookCreate(BookBase):
    tags: List[TagCreate] = []

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    rating: Optional[int] = None
    comment: Optional[str] = None
    tags: Optional[List[TagCreate]] = []

class Book(BookBase):
    id: int
    owner_id: int
    tags: List[Tag] = []   # Use as Set

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    books: List[Book] = []

    class Config:
        orm_mode = True

class ChangePassword(BaseModel):
    old_password: str
    new_password: str
