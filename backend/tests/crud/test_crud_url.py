from app.crud.crud_url import create_url_obj, get_url_obj
from app.schemas.url import URLCreate
from app.db.models import Url
from pydantic import HttpUrl


def test_create_url_obj_creates_correct_obj_and_saves_it_to_db(db_session):
    url_input = URLCreate(original_url=HttpUrl("https://example.com"), expiry_days=10)

    db_obj = create_url_obj(db_session, url_input)

    assert str(db_obj.original_url) == "https://example.com/"
    assert db_obj.short_url_id is not None
    assert len(db_obj.short_url_id) > 0

    queried = db_session.query(Url).filter_by(short_url_id=db_obj.short_url_id).first()
    assert queried is not None
    assert str(queried.original_url) == "https://example.com/"


def test_get_url_obj_exists(db_session):
    test_short_id = "test_id"
    test_original_id = "test_original_id"
    from datetime import datetime, timezone, timedelta
    new_url = Url(
        original_url=test_original_id,
        short_url_id=test_short_id,
        created_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(days=1)
    )
    db_session.add(new_url)
    db_session.commit()

    res = get_url_obj(db_session, f"{test_short_id}")

    assert res is not None
    assert res.short_url_id == test_short_id
    assert res.original_url == test_original_id


def test_get_url_obj_not_found(db_session):
    res = get_url_obj(db_session, "https://mit.ly/nonexistent")
    assert res is None
