from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
import uuid

class Message(Base):
    __tablename__ = "messages"

    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), nullable=False)
    content = Column(String, nullable=False)
    sent_at = Column(DateTime, nullable=False)
    rating = Column(Boolean, nullable=False)
    role = Column(String, nullable=False)
