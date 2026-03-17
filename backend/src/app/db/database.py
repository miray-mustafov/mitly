from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import Session
from typing import Generator, Annotated
from fastapi import Depends
from ..config import settings as s # relative import to reach the config package from the database module

# When your python classes in models.py inherit from Base, they are translated to the database language
Base = declarative_base()


def get_engine_and_session() -> tuple:
    # defining a destination where sqlalchemy should go and how to log in, which driver to use, etc.
    SQLALCHEMY_DATABASE_URL = f"{s.DB_DIALECT}+{s.DB_DRIVER}://{s.DB_USER}:{s.DB_PASS}@{s.DB_HOST}/{s.DB_NAME}"

    # the engine is like a power strip (разклонител) plugged into a wall outlet (контакт) (PostgresSQL)
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    # the session is when you plug in a toaster (a database query)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal


def create_db_if_missing():
    engine, _ = get_engine_and_session()
    if not database_exists(engine.url):
        create_database(engine.url)


def create_tables_if_missing():
    """
    By importing Base from models, the python interpreter initializes the classes inside (which inherit from Base)
    and this registers models/tables characteristics in Base.metadata.
    If we used local Base, it would be empty
    """
    from .models import Base  # local import to avoid circular imports
    # print(f"Registered tables: {Base.metadata.tables.keys()}")  # to check what tables are registered
    engine, _ = get_engine_and_session()
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator:
    """Dependency for FastAPI endpoints to get a DB session"""
    _, SessionLocal = get_engine_and_session()

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
Annotated type for cleaner dependency injection in FastAPI
get_db Generator helps us to SETUP > USAGE > CLEANUP a db session elegantly

without that generator technique our code we would have to initialize db session in every router
like this:
            @app.post("/urls")
            def create_url(new_data: URLSchema): 
                # 1. You have to manually create the session
                db = SessionLocal() 
                
                try:

                    # 2. Your actual logic
                    
                    db.add(new_data)
                    db.commit()
                except Exception as e:
                    # 3. You must handle rollbacks manually
                    db.rollback()
                    raise e
                finally:
                    # 4. You MUST remember to close it manually
                    db.close() 
                    
                return {"message": "Created!"}
"""
dbDep = Annotated[Session, Depends(get_db)]
