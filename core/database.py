from sqlalchemy import create_engine , Column , Integer , String , Boolean , ForeignKey 
from sqlalchemy.orm import sessionmaker , DeclarativeBase 

# ۱. اصلاح آدرس: نام فایل معمولاً .db یا .sqlite است
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# ۲. ایجاد موتور (نکته: check_same_thread فقط برای SQLite نیاز است)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String())
    amount = Column(Integer)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()