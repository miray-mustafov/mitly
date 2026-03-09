from src.app.db import database as actual_database
import pytest


def test_get_engine_and_session(monkeypatch):  # monkeypatch is a built-in pytest fixture
    """
    The common AAA tests structure pattern.
    We are not testing if SQLAlchemy can parse a URL.
    We are testing if the code correctly retrieves variables from the environment
    and plugs them into the right slots in the connection string.
    """

    # arrange(setup): Fake the environment variables
    # this ensures os.getenv returns these values during the test
    monkeypatch.setenv("DB_DIALECT", "postgresql")
    monkeypatch.setenv("DB_DRIVER", "psycopg")
    monkeypatch.setenv("DB_USER", "test_user")
    monkeypatch.setenv("DB_PASS", "test_pass")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_NAME", "test_db")

    # act: Call the actual function
    engine, SessionLocal = actual_database.get_engine_and_session()

    # assert: Verify the engine URL is constructed correctly
    expected_url = "postgresql+psycopg://test_user:test_pass@localhost/test_db"
    assert engine.url.render_as_string(hide_password=False) == expected_url
    assert SessionLocal is not None  # not-so-relevant check but just in case
    assert engine is not None


def test_get_db_lifecycle(mocker):  # all AI here
    # Mock the session object and the sessionmaker
    mock_session = mocker.Mock()
    # Mock get_engine_and_session to return our mock sessionmaker
    mock_session_local = mocker.Mock(return_value=mock_session)
    mocker.patch("src.app.db.database.get_engine_and_session", return_value=(None, mock_session_local))

    # Run the generator
    gen = actual_database.get_db()
    db = next(gen)

    # Assert 1: We got our session
    assert db == mock_session

    # Assert 2: Close hasn't been called yet
    mock_session.close.assert_not_called()

    # Trigger the 'finally' block
    try:
        next(gen)
    except StopIteration:
        pass

    # Assert 3: Close was called
    mock_session.close.assert_called_once()


"""
Skipped tests:

def test_create_db_if_missing():
    pass


def test_create_tables_if_missing():
    pass
"""
