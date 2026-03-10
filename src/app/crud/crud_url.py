from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from ..db.models import Url
from ..schemas.url import URLCreate, URLRead
from ..config import settings
from .utils import ShortUrlIdGenerator


def create_url_obj(db: Session, url_input: URLCreate):
    expiry_days = url_input.expiry_days or settings.DEFAULT_URL_EXPIRY_DAYS
    expires_at = datetime.now(timezone.utc) + timedelta(days=expiry_days)
    short_url_id = ShortUrlIdGenerator.generate_short_url_id()

    url_obj = Url(
        original_url=str(url_input.original_url),
        expires_at=expires_at,
        short_url_id=short_url_id,
    )

    db.add(url_obj)
    db.commit()
    db.refresh(url_obj)

    return url_obj


def get_url_obj(db: Session, short_url: str):
    cur_short_url_id = short_url.split("/")[-1]
    url_obj = db.query(Url).filter_by(short_url_id=cur_short_url_id).first()

    return URLRead.model_validate(url_obj) if url_obj else None
