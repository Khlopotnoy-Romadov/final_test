from pydantic import BaseModel
from datetime import datetime

class URLCreate(BaseModel):
    url: str

class URLResponse(BaseModel):
    short_id: str
    short_url: str
    
class URLStats(BaseModel):
    short_id: str
    original_url: str
    created_at: datetime
    access_count: int