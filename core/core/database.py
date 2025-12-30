from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , DeclarativeBase
from core.config import settings
from core.models import Task


engine = create_engine(
   settings.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()