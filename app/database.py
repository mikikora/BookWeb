from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Użyj odpowiednich danych do logowania się do swojej bazy danych PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://mikolaj:AlaMaKota@localhost/BookWeb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
