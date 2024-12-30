from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from ..db import db
from typing import Optional
from datetime import datetime


class Training_Message(db.Model):
    __tablename__ = 'training_messages'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id", ondelete="CASCADE"))
    character: Mapped["Character"] = relationship("Character", back_populates="training_messages")
    message: Mapped[str] = mapped_column(String(50), default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def to_dict(self):

        training_message_dict = dict(
            id=self.id,
            character_id=self.character_id,
            character=self.character,
            message=self.message,
            created_at=self.created_at
        )

        return training_message_dict

    @classmethod
    def from_dict(cls, training_message_data):
        
        training_message_dict = cls(
            character_id=training_message_data["character_id"],
            character=training_message_data["character"],
            message=training_message_data["message"],
            created_at=training_message_data["completed_at"]
        )

        return training_message_dict