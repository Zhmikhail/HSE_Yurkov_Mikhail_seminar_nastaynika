import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from database import SessionLocal, ShortURL
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def cleanup_expired_urls():
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        
        expired_urls = db.query(ShortURL).filter(
            (ShortURL.expires_at != None) & (ShortURL.expires_at < now)
        ).all()
        
        for url in expired_urls:
            db.delete(url)
        
        db.commit()
        
        logger.info(f"Cleaned up {len(expired_urls)} expired URLs at {now}")
        
        return len(expired_urls)
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")
        db.rollback()
        return 0
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_expired_urls()