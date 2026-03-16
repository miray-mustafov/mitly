from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.config import settings
from app.crud.utils import ShortUrlIdGenerator
from app.db.models import Url
from app.schemas.url import URLCreate, URLRead


def create_url_obj(db: Session, url_input: URLCreate):
    expiry_days = url_input.expiry_days or settings.DEFAULT_URL_EXPIRY_DAYS
    expires_at = datetime.now(timezone.utc) + timedelta(days=expiry_days)

    url_obj = Url(
        original_url=str(url_input.original_url),
        expires_at=expires_at,
    )

    try:
        db.add(url_obj)
        db.flush()  # sends INSERT, so url_obj.url_id gets populated without committing yet, so we can get the url_id

        short_url_id = ShortUrlIdGenerator.generate_short_url_id(url_obj.url_id)
        url_obj.short_url_id = short_url_id

        db.commit()
        db.refresh(url_obj)
        return url_obj
    except Exception:
        db.rollback()  # in case of any error along the path, rollback transaction
        raise


def get_url_obj(db: Session, short_url_id: str):
    url_obj = db.query(Url).filter_by(short_url_id=short_url_id).first()

    return URLRead.model_validate(url_obj) if url_obj else None


def get_all_urls(db: Session):
    urls = db.query(Url).all()
    return urls
