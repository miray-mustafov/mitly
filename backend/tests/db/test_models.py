from src.app.db.models import Url
from datetime import datetime, timedelta, timezone
import pytest
from sqlalchemy.exc import IntegrityError


def test_url_creation(db_session):
    new_url = Url(
        short_url_id="goog1234",
        original_url="https://google.com",
        expires_at=datetime.now(timezone.utc) + timedelta(days=30)
    )

    db_session.add(new_url)
    db_session.commit()

    retrieved = db_session.query(Url).filter_by(short_url_id="goog1234").first()
    assert retrieved is not None
    assert retrieved.original_url == "https://google.com"
    assert retrieved.url_id is not None


def test_url_is_expired_logic(db_session):
    past_date = datetime.now(timezone.utc) - timedelta(days=1)
    expired_url = Url(
        short_url_id="old12345",
        original_url="https://old.com",
        expires_at=past_date
    )

    future_date = datetime.now(timezone.utc) + timedelta(days=1)
    active_url = Url(
        short_url_id="new12345",
        original_url="https://new.com",
        expires_at=future_date
    )

    assert expired_url.is_expired is True
    assert active_url.is_expired is False


def test_short_url_id_uniqueness(db_session):
    url1 = Url(short_url_id="same1234", original_url="https://a.com", expires_at=datetime.now(timezone.utc))
    url2 = Url(short_url_id="same1234", original_url="https://b.com", expires_at=datetime.now(timezone.utc))

    db_session.add(url1)
    db_session.commit()

    db_session.add(url2)
    with pytest.raises(IntegrityError):
        db_session.commit()