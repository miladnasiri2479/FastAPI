from core.database import Base
from sqlalchemy import Boolean, Column, Integer, String,Text


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text,default="")
    is_done = Column(Boolean,default=False)

    
    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, title={self.title!r}, is_done={self.is_done!r})"