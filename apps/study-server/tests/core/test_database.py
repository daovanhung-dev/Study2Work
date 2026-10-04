from collections.abc import Callable
from types import SimpleNamespace
from unittest.mock import Mock

import app.core.database as database_module
import pytest
from app.core.config import Settings
from app.core.database import (
    build_database_url,
    get_db_from_factory,
    query_many,
    query_one,
)
from sqlalchemy import URL, create_engine, text
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session


def make_settings() -> Settings:
    """Tạo Settings cô lập cho kiểm thử database với URL PostgreSQL local, schema test và khóa
    HS256 dành riêng cho test."""
    return Settings(
        database_url="postgresql://user:p%40ss%3Aword@localhost:5432/study",
        db_schema="study_dev0",
        jwt_algorithm="HS256",
        jwt_secret_key="test-secret-key-that-is-at-least-32-characters",
    )


def test_database_url_escapes_credentials() -> None:
    """Kiểm tra parser URL mã hóa ký tự đặc biệt trong thông tin xác thực và đổi driver sang
    postgresql+psycopg."""
    url = build_database_url(make_settings())

    assert url.render_as_string(hide_password=False) == (
        "postgresql+psycopg://user:p%40ss%3Aword@localhost:5432/study"
    )


def test_database_url_preserves_neon_connection_options() -> None:
    """Kiểm tra khi chuẩn hóa driver, URL vẫn giữ các tùy chọn SSL và channel
    binding cần cho Neon."""
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


def test_build_engine_registers_transaction_schema_hook_without_startup_option(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra engine PostgreSQL gắn schema cho mỗi transaction, giữ URL Neon và pool options,
    không gửi schema trong startup options."""
    config = Settings(
        db_host="localhost",
        db_name="local_database",
        db_user="local_user",
        db_password="local_password",
        db_schema="study_dev0",
    )
    database_engine = SimpleNamespace(dialect=SimpleNamespace(name="postgresql"))
    captured_args: list[object] = []
    captured_kwargs: dict[str, object] = {}
    captured_listeners: list[Callable[[Connection], None]] = []

    def fake_create_engine(*args: object, **kwargs: object) -> object:
        """Thay create_engine trong kiểm thử, ghi lại keyword arguments để xác nhận cấu hình
        build_engine mà không mở kết nối thật."""
        captured_args.extend(args)
        captured_kwargs.update(kwargs)
        return database_engine

    def fake_listen(
        target: object,
        identifier: str,
        listener: Callable[[Connection], None],
    ) -> None:
        """Ghi listener đăng ký để kiểm tra callback begin mà không tạo kết nối PostgreSQL."""
        assert target is database_engine
        assert identifier == "begin"
        captured_listeners.append(listener)

    monkeypatch.setattr(database_module, "create_engine", fake_create_engine)
    monkeypatch.setattr(database_module.event, "listen", fake_listen)

    result = database_module.build_engine(config)

    assert result is database_engine
    assert isinstance(captured_args[0], URL)
    assert captured_args[0].drivername == "postgresql+psycopg"
    assert captured_args[0].query == {"sslmode": "require", "channel_binding": "require"}
    assert captured_kwargs == {
        "pool_pre_ping": True,
        "pool_size": config.database_pool_size,
        "max_overflow": config.database_max_overflow,
    }
    assert len(captured_listeners) == 1

    listener = captured_listeners[0]
    connection = Mock()
    listener(connection)
    listener(connection)

    assert connection.execute.call_count == 2
    for call in connection.execute.call_args_list:
        statement, params = call.args
        assert str(statement) == "SELECT set_config('search_path', quote_ident(:schema), true)"
        assert params == {"schema": config.db_schema}


def test_build_engine_does_not_register_schema_hook_for_non_postgres(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra engine không phải PostgreSQL không nhận listener search_path."""
    database_engine = SimpleNamespace(dialect=SimpleNamespace(name="sqlite"))
    listen = Mock()
    monkeypatch.setattr(database_module, "create_engine", lambda *args, **kwargs: database_engine)
    monkeypatch.setattr(database_module.event, "listen", listen)

    assert database_module.build_engine(make_settings()) is database_engine
    listen.assert_not_called()


def test_transaction_schema_setup_failure_propagates() -> None:
    """Kiểm tra lỗi đặt search_path không bị nuốt để transaction dừng trước truy vấn nghiệp vụ."""
    connection = Mock()
    connection.execute.side_effect = RuntimeError("search_path setup failed")

    with pytest.raises(RuntimeError, match="search_path setup failed"):
        database_module._set_transaction_search_path("study_dev0", connection)


def test_query_helpers_return_plain_dictionaries() -> None:
    """Kiểm tra query_one và query_many chuyển mapping row thành dict thường, trả None khi không có
    row và bind tham số truy vấn."""
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
    """Kiểm tra dependency get_db đóng Session sau khi caller hoàn tất, kể cả khi generator được
    đóng."""
    class FakeSession:
        closed = False

        def close(self) -> None:
            """Đánh dấu FakeSession đã đóng để kiểm thử dependency giải phóng Session
            sau request."""
            self.closed = True

    session = FakeSession()
    sessions = get_db_from_factory(lambda: session)
    assert next(sessions) is session
    with pytest.raises(StopIteration):
        next(sessions)
    assert session.closed is True
