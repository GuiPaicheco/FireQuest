from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.db.base import Base
from sqlalchemy import DateTime
from datetime import datetime

class Mission(Base):
    __tablename__ = "missions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    difficulty = Column(Integer)
    urgency = Column(Integer)
    xp = Column(Integer)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    due_date = Column(DateTime, nullable=True)
    approved_percentage = Column(Integer, default=100)