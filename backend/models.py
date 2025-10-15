from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())

# ------------- User model -----------------
class User(Base):
    __tablename__ = "users"
    user_id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    user_name = Column(String(255), nullable=False)
    user_email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    last_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = relationship("Note", back_populates="owner", cascade="all, delete-orphan")

# ----------- Notes model --------------------
class Note(Base):
    __tablename__ = "notes"

    note_id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    note_title = Column(String(255), nullable=False)
    note_content = Column(String(255), nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    last_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(String(36), ForeignKey("users.user_id"), nullable=False)
    owner = relationship("User", back_populates="notes")
