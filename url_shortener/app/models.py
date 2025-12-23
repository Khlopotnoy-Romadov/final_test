from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class ShortURL(Base):
    __tablename__ = "short_urls"
    
    id = Column(Integer, primary_key=True, index=True)
    short_id = Column(String, unique=True, index=True, nullable=False)
    original_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    access_count = Column(Integer, default=0)