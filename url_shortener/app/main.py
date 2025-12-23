from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import shortuuid
from urllib.parse import urlparse
import uvicorn

from . import models, schemas
from .database import engine, get_db

# Создаем таблицы
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener Service", version="1.0.0")

def validate_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

@app.post("/shorten", response_model=schemas.URLResponse)
def shorten_url(url_data: schemas.URLCreate, db: Session = Depends(get_db)):
    # Валидация URL
    if not validate_url(url_data.url):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid URL format"
        )
    
    # Генерируем короткий ID
    short_id = shortuuid.uuid()[:8]
    
    # Проверяем уникальность (хотя очень маловероятно совпадение)
    existing = db.query(models.ShortURL).filter(
        models.ShortURL.short_id == short_id
    ).first()
    
    # Если ID уже существует, генерируем новый
    while existing:
        short_id = shortuuid.uuid()[:8]
        existing = db.query(models.ShortURL).filter(
            models.ShortURL.short_id == short_id
        ).first()
    
    # Сохраняем в базу
    db_url = models.ShortURL(
        short_id=short_id,
        original_url=url_data.url
    )
    
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    
    return {
        "short_id": short_id,
        "short_url": f"/{short_id}"
    }

@app.get("/{short_id}")
def redirect_to_url(short_id: str, db: Session = Depends(get_db)):
    url_entry = db.query(models.ShortURL).filter(
        models.ShortURL.short_id == short_id
    ).first()
    
    if not url_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found"
        )
    
    # Увеличиваем счетчик переходов
    url_entry.access_count += 1
    db.commit()
    
    return RedirectResponse(url=url_entry.original_url)

@app.get("/stats/{short_id}", response_model=schemas.URLStats)
def get_url_stats(short_id: str, db: Session = Depends(get_db)):
    url_entry = db.query(models.ShortURL).filter(
        models.ShortURL.short_id == short_id
    ).first()
    
    if not url_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found"
        )
    
    return url_entry

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)