import pytest
from app.core.config import Settings
from app.core.database import (
    build_database_url,
    get_db_from_factory,
    query_many,
    query_one,
)
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session


def make_settings() -> Settings:
    return Settings(
        database_url="postgresql://user:p%40ss%3Aword@localhost:5432/study",
        db_schema="study_dev0",
        jwt_algorithm="HS256",
        jwt_secret_key="test-secret-key-that-is-at-least-32-characters",
    )


def test_database_url_escapes_credentials() -> None:
    url = build_database_url(make_settings())

    assert url.render_as_string(hide_password=False) == (
        "postgresql+psycopg://user:p%40ss%3Aword@localhost:5432/study"
    )


def test_database_url_preserves_neon_connection_options() -> None:
    url = build_database_url(
        Settings(
            db_host="localhost",
            db_name="local_database",
            db_user="local_user",
            db_password="local_password",
        )
    )

    assert url.drivername == "postgresql+psycopg"
    assert url.host == "ep-red-frog-b3yp4d4v-pooler.c-4.ap-southeast-1.aws.neon.tech"
    assert url.database == "neondb"
    assert url.query == {
        "sslmode": "require",
        "channel_binding": "require",
    }


def test_query_helpers_return_plain_dictionaries() -> None:
    engine = create_engine("sqlite://")
    with Session(engine) as db:
        db.execute(text("CREATE TABLE users (id INTEGER, name TEXT)"))
        db.execute(text("INSERT INTO users VALUES (1, 'Ada'), (2, 'Linus')"))
        db.commit()

        assert query_one(db, "SELECT id, name FROM users WHERE id = :id", {"id": 1}) == {
            "id": 1,
            "name": "Ada",
        }
        assert query_many(db, "SELECT id, name FROM users ORDER BY id") == [
            {"id": 1, "name": "Ada"},
            {"id": 2, "name": "Linus"},
        ]


def test_get_db_closes_the_request_session() -> None:
    class FakeSession:
        closed = False

        def close(self) -> None:
            self.closed = True

    session = FakeSession()
    sessions = get_db_from_factory(lambda: session)
    assert next(sessions) is session
    with pytest.raises(StopIteration):
        next(sessions)
    assert session.closed is True
