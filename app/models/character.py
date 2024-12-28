from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from ..db import db
from typing import Optional
from datetime import datetime

class Character(db.Model):
    __tablename__ = 'characters'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)  # Explicitly define the column
    description: Mapped[str] = mapped_column(String(255), nullable=False)  # Explicitly define the column
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def to_dict(self):

        user_dict = dict(
            id=self.id,
            name=self.name,
            description=self.description,
            # created_at=self.created_at.isoformat()
        )

        return user_dict

    @classmethod
    def from_dict(cls, user_data):
        created_at = user_data.get("created_at", datetime.utcnow()) 
        user_dict = cls(
            name=user_data["name"],
            description=user_data["description"],
            created_at=created_at
        )

        return user_dict