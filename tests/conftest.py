import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")  # flags the function that it will prepare stuff for tests
def db_session():
    """
    Setup: Everything before the yield keyword (creating the engine, creating tables).
    The Object: The session object itself, which is "handed over" to the test.
    Teardown: Everything after the yield keyword (closing the session, dropping tables).
        This runs automatically after the test finishes, even if the test fails!
    Scope: scope="function" means a brand-new, clean database session is created for every single test function.
    """

    engine = create_engine(
        SQLALCHEMY_TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    from src.app.db.models import Base  # ! Import from models so Base knows about the models
    Base.metadata.create_all(bind=engine)  # Create the tables in the SQLite memory

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
