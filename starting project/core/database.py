from sqlalchemy import create_engine , Column , Integer , String , Boolean , ForeignKey 
from sqlalchemy.orm import sessionmaker , DeclarativeBase  , Relationship
from config import settings



engine = create_engine(
   settings.database_url, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
class Base(DeclarativeBase):
    pass

class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    
    expenses = Relationship("Expense", back_populates="owner")

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_name = Column(String)
    amount = Column(Integer)
    
    owner_id = Column(Integer, ForeignKey("persons.id"))
    
    owner = Relationship("Person", back_populates="expenses")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()