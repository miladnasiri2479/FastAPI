from core.database import Base
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime , ForeignKey 
from sqlalchemy.orm import Relationship

class TaskModel(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    user_id =Column(Integer,ForeignKey("users.id"))
    title = Column(String)
    description = Column(Text,default="")
    is_completed = Column(Boolean,default=False)

    created_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user= Relationship("UserModel", back_populates="tasks", uselist=False)
    
    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, title={self.title!r}, is_done={self.is_done!r})"