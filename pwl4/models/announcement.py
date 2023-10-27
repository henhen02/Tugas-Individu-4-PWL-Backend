from sqlalchemy import Column, Integer, Text, DATETIME
from datetime import datetime

from .meta import Base


class Announcement(Base):
    __tablename__ = "announcement"
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DATETIME, default=datetime.now)
