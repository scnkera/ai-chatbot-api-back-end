from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from ..db import db
from typing import Optional
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(25))
    email: Mapped[str] = mapped_column(String(50), default=None, nullable=True)
    password: Mapped[str] = mapped_column(String(50), default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def to_dict(self):

        user_dict = dict(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password,
            created_at=self.created_at.isoformat()
        )

        return user_dict

    @classmethod
    def from_dict(cls, user_data):
        created_at = user_data.get("created_at", datetime.utcnow()) 
        user_dict = cls(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
            created_at=created_at
        )

        return user_dict