import uvicorn
from fastapi import FastAPI
from .db import database
from .api.v1.api import api_router
from .config import settings as s

app = FastAPI(title="Mitly URL Shortener")
app.include_router(api_router)


def main():  # because console scripts from pyproject.toml must point to a callable function
    if s.ENV != "test":
        database.create_db_if_missing()
        database.create_tables_if_missing()
    uvicorn.run("app.main:app", host="127.0.0.1", port=s.LOCAL_PORT)

if __name__ == '__main__':
    main()