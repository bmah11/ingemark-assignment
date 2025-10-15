from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class MessageBase(BaseModel):
    chat_id: UUID
    content: str
    sent_at: datetime
    rating: bool
    role: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    message_id: UUID

    model_config = {"from_attributes": True}
