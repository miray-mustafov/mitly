from fastapi import APIRouter, HTTPException
from app.db.database import dbDep
from app.schemas.url import URLCreate, URLRead
from app.crud import crud_url

router = APIRouter(prefix="/urls", tags=["URLs"])


@router.get("")
def get_all_urls(db: dbDep):
    """
    That is currently for testing purposes
    """
    urls = crud_url.get_all_urls(db)
    return urls


@router.post("/shorten", response_model=URLRead)
def shorten_url(url_input: URLCreate, db: dbDep):
    return crud_url.create_url_obj(db, url_input)


@router.get("/{short_url_id}")
def get_url_obj_by_short_url_id(short_url_id: str, db: dbDep):
    url_read = crud_url.get_url_obj(db, short_url_id)

    if not url_read:
        raise HTTPException(status_code=404, detail="URL not found")

    if url_read.is_expired:
        raise HTTPException(status_code=410, detail="URL has expired")

    return url_read
