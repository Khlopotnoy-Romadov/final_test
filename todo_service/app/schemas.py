from pydantic import BaseModel
from typing import Optional

class TodoItemCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoItemResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    
    class Config:
        from_attributes = True