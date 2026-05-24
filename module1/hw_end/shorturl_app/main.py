from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime, timedelta
from database import get_db, ShortURL
import string
import secrets
import uvicorn
from fastapi.responses import RedirectResponse

app = FastAPI(title="URL Shortener Service")

USER_TIERS = {
    'tsar': 1,      # 66¹ = 66 комбинаций
    'premium': 2,   # 66² = 4,356 комбинаций
    'standard': 3,  # 66³ = 287,496 комбинаций  
    'free': 4       # 66⁴ = 18,974,736 комбинаций
}

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_.~"

class URLCreate(BaseModel):
    url: HttpUrl
    ttl_minutes: Optional[float] = 1440.0
    user_tier: Optional[str] = 'free'

class URLResponse(BaseModel):
    short_id: str
    short_url: str
    full_url: str
    created_at: str
    expires_at: Optional[str]
    clicks: int
    user_tier: str
    
    class Config:
        from_attributes = True

def generate_short_id(length):
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))

def is_short_id_unique(short_id, db):
    return db.query(ShortURL).filter(ShortURL.short_id == short_id).first() is None

def get_unique_short_id(db, user_tier='free'):
    length = USER_TIERS.get(user_tier, 4)
    max_attempts = 50
    
    for _ in range(max_attempts):
        short_id = generate_short_id(length)
        if is_short_id_unique(short_id, db):
            return short_id
    
    return generate_short_id(length + 1)

def calculate_expires_at(ttl_minutes):
    if ttl_minutes is None:
        return None
    return datetime.utcnow() + timedelta(minutes=ttl_minutes)

def cleanup_expired_urls(db):
    now = datetime.utcnow()
    expired_urls = db.query(ShortURL).filter(
        (ShortURL.expires_at != None) & (ShortURL.expires_at < now)
    ).all()
    
    for url in expired_urls:
        db.delete(url)
    
    if expired_urls:
        db.commit()
    return len(expired_urls)

@app.post("/shorten", response_model=URLResponse)
def shorten_url(url_data: URLCreate, db: Session = Depends(get_db)):
    cleanup_expired_urls(db)
    
    short_id = get_unique_short_id(db, url_data.user_tier)
    expires_at = calculate_expires_at(url_data.ttl_minutes)
    
    db_url = ShortURL(
        short_id=short_id,
        full_url=str(url_data.url),
        expires_at=expires_at,
        user_tier=url_data.user_tier
    )
    
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    
    return URLResponse(
        short_id=db_url.short_id,
        short_url=f"http://localhost:8001/{db_url.short_id}",
        full_url=db_url.full_url,
        created_at=db_url.created_at.isoformat(),
        expires_at=db_url.expires_at.isoformat() if db_url.expires_at else None,
        clicks=db_url.clicks,
        user_tier=db_url.user_tier
    )

@app.get("/{short_id}")
def redirect_to_url(short_id: str, db: Session = Depends(get_db)):
    url_item = db.query(ShortURL).filter(ShortURL.short_id == short_id).first()
    
    if not url_item:
        raise HTTPException(status_code=404, detail="URL not found")
    
    if url_item.expires_at and url_item.expires_at < datetime.utcnow():
        db.delete(url_item)
        db.commit()
        raise HTTPException(status_code=410, detail="URL has expired")
    
    url_item.clicks += 1
    db.commit()
    
    return RedirectResponse(url=url_item.full_url, status_code=status.HTTP_302_FOUND)

@app.get("/stats/{short_id}", response_model=URLResponse)
def get_url_stats(short_id: str, db: Session = Depends(get_db)):
    url_item = db.query(ShortURL).filter(ShortURL.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="URL not found")
    
    is_expired = url_item.expires_at and url_item.expires_at < datetime.utcnow()
    
    return URLResponse(
        short_id=url_item.short_id,
        short_url=f"http://localhost:8001/{url_item.short_id}",
        full_url=url_item.full_url,
        created_at=url_item.created_at.isoformat(),
        expires_at=url_item.expires_at.isoformat() if url_item.expires_at else None,
        clicks=url_item.clicks,
        user_tier=url_item.user_tier
    )

# Добавь после других эндпоинтов

@app.get("/admin/urls")
def get_all_urls(db: Session = Depends(get_db)):
    urls = db.query(ShortURL).order_by(ShortURL.created_at.desc()).all()
    return [
        {
            "short_id": url.short_id,
            "full_url": url.full_url,
            "created_at": url.created_at.isoformat(),
            "expires_at": url.expires_at.isoformat() if url.expires_at else None,
            "clicks": url.clicks,
            "user_tier": url.user_tier
        }
        for url in urls
    ]

@app.get("/admin/urls/count")
def get_urls_count(db: Session = Depends(get_db)):
    count = db.query(ShortURL).count()
    return {"total_urls": count}

@app.get("/admin/urls/stats")
def get_urls_stats(db: Session = Depends(get_db)):
    # Статистика по типам пользователей
    stats = db.query(
        ShortURL.user_tier,
        db.func.count(ShortURL.id).label('count'),
        db.func.sum(ShortURL.clicks).label('total_clicks'),
        db.func.avg(ShortURL.clicks).label('avg_clicks')
    ).group_by(ShortURL.user_tier).all()
    
    return [
        {
            "user_tier": stat.user_tier,
            "count": stat.count,
            "total_clicks": stat.total_clicks,
            "avg_clicks": float(stat.avg_clicks) if stat.avg_clicks else 0
        }
        for stat in stats
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)