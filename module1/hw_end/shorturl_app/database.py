from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

os.makedirs('/app/data', exist_ok=True)

SQLALCHEMY_DATABASE_URL = "sqlite:////app/data/shorturl.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class ShortURL(Base):
    __tablename__ = "short_urls"
    
    id = Column(Integer, primary_key=True, index=True)
    short_id = Column(String, unique=True, nullable=False)
    full_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    clicks = Column(Integer, default=0, nullable=False)
    user_tier = Column(String, default='free', nullable=False)

# Создаем индекс для быстрого поиска по short_id
Index('idx_short_id', ShortURL.short_id, unique=True)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()