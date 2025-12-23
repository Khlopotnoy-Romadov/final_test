from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from . import models, schemas
from .database import engine, get_db

# Создаем таблицы
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo Service", version="1.0.0")

@app.post("/items/", response_model=schemas.TodoItemResponse)
def create_item(item: schemas.TodoItemCreate, db: Session = Depends(get_db)):
    db_item = models.TodoItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/", response_model=List[schemas.TodoItemResponse])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.TodoItem).offset(skip).limit(limit).all()
    return items

@app.get("/items/{item_id}", response_model=schemas.TodoItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.TodoItem).filter(models.TodoItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=schemas.TodoItemResponse)
def update_item(item_id: int, item_update: schemas.TodoItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(models.TodoItem).filter(models.TodoItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    update_data = item_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.TodoItem).filter(models.TodoItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)