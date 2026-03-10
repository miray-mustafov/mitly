from src.app.db import database as actual_database
from src.app.config.test import Settings
import pytest


def test_get_engine_and_session(monkeypatch):
    """
    The common AAA tests structure pattern.
    We are not testing if SQLAlchemy can parse a URL.
    We are testing if the code correctly retrieves variables from the environment
    and plugs them into the right slots in the url connection string.
    """

    # arrange
    monkeypatch.setenv("DB_DIALECT", "postgresql")
    monkeypatch.setenv("DB_DRIVER", "psycopg")
    monkeypatch.setenv("DB_USER", "test_user")
    monkeypatch.setenv("DB_PASS", "test_pass")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_NAME", "test_db")

    # Since 'settings' is already initialized and cached in actual_database, 
    # we test by creating a new Settings object which should pick up the monkeypatched env vars.
    test_settings = Settings()
    
    # Verify Settings picks up monkeypatch
    assert test_settings.DB_USER == "test_user"
    assert test_settings.DB_NAME == "test_db"

    # To test actual_database.get_engine_and_session, we would need to override the cached settings.
    # Instead, we verify the logic of engine creation by mocking the settings used inside it.
    import src.app.db.database as database_mock
    monkeypatch.setattr(database_mock, "s", test_settings)

    engine, SessionLocal = database_mock.get_engine_and_session()

    # assert
    expected_url = "postgresql+psycopg://test_user:test_pass@localhost/test_db"
    assert engine.url.render_as_string(hide_password=False) == expected_url


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
