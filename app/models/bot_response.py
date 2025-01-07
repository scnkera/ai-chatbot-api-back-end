from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from ..db import db
from typing import Optional
from datetime import datetime
from typing import List

class BotResponses(db.Model):
    pass