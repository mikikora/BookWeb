from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

book_tag_association = Table(
    'book_tag_association', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    books = relationship("Book", back_populates="owner")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    rating = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))
    comment = Column(String)

    owner = relationship("User", back_populates="books")
    tags = relationship("Tag", secondary=book_tag_association, back_populates="books")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User")
    books = relationship("Book", secondary=book_tag_association, back_populates="tags")
