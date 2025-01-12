from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from ..db import db
from typing import Optional
from datetime import datetime
from typing import List

class BotResponses(db.Model):
    __tablename__ = 'bot_responses'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    char_id: Mapped[str] = mapped_column(String(25))
    training_message_id: Mapped[str] = mapped_column(String(50), default=None, nullable=True)
    question: Mapped[str] = mapped_column(String(50), default=None, nullable=True)
    response: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def to_dict(self):

        bot_response_dict = dict(
            char_id=self.char_id,
            training_message_id=self.training_message_id,
            question=self.question,
            response=self.response,
            created_at=self.created_at.isoformat()
        )

        return bot_response_dict

    @classmethod
    def from_dict(cls, bot_response_dict_data):
        created_at = bot_response_data.get("created_at", datetime.utcnow()) 
        bot_response_dict = cls(
            char_id=bot_response_data["char_id"],
            training_message_id=bot_response_data["training_message_id"],
            question=bot_response_data["question"],
            response=bot_response_data["response"],
            created_at=created_at
        )

        return bot_response_dict
