"""Thiết lập SQLAlchemy đồng bộ và cung cấp dependency phiên cùng các hàm truy vấn nhỏ cho
Study API."""

from __future__ import annotations

from collections.abc import Generator, Mapping
from functools import lru_cache, partial
from typing import Any

from sqlalchemy import URL, Connection, Engine, create_engine, event, text
from sqlalchemy.engine import Result, make_url
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings, get_settings


def build_database_url(config: Settings) -> URL:
    """Đọc URL database từ Settings, phân tích thành đối tượng URL SQLAlchemy và đổi driver
    PostgreSQL mặc định sang postgresql+psycopg. Các thành phần query như SSL và channel binding
    được giữ lại; giá trị bí mật chỉ được mở tại bước phân tích URL."""

    database_url = make_url(config.database_url.get_secret_value())
    if database_url.drivername == "postgresql":
        database_url = database_url.set(drivername="postgresql+psycopg")
    return database_url


def _set_transaction_search_path(schema: str, connection: Connection) -> None:
    """Đặt search_path chỉ trong transaction hiện tại bằng tên schema được bind an toàn.

    Lỗi cấu hình schema được giữ nguyên để transaction dừng trước khi chạy truy vấn nghiệp vụ.
    """
    connection.execute(
        text("SELECT set_config('search_path', quote_ident(:schema), true)"),
        {"schema": schema},
    )


def build_engine(config: Settings) -> Engine:
    """Tạo SQLAlchemy Engine từ cấu hình đã cung cấp với kiểm tra kết nối trước khi lấy kết nối và
    giới hạn pool theo Settings. Với PostgreSQL, hàm đăng ký listener đặt search_path chỉ trong
    từng transaction; hàm không mở transaction nghiệp vụ."""

    database_engine = create_engine(
        build_database_url(config),
        pool_pre_ping=True,
        pool_size=config.database_pool_size,
        max_overflow=config.database_max_overflow,
    )
    if database_engine.dialect.name == "postgresql":
        event.listen(
            database_engine,
            "begin",
            partial(_set_transaction_search_path, config.db_schema),
        )
    return database_engine


def build_session_factory(database_engine: Engine) -> sessionmaker[Session]:
    """Tạo sessionmaker đồng bộ gắn với Engine đã cho, tắt autoflush và giữ trạng thái object sau
    commit. Factory trả về tạo một Session mới cho mỗi lần gọi."""

    return sessionmaker(
        bind=database_engine,
        autoflush=False,
        expire_on_commit=False,
        class_=Session,
    )


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    """Lấy Settings mặc định rồi tạo Engine và cache một Engine duy nhất trong tiến trình. Cấu hình
    chỉ được nạp khi hàm được gọi lần đầu."""

    return build_engine(get_settings())


@lru_cache(maxsize=1)
def get_session_factory() -> sessionmaker[Session]:
    """Lấy Engine dùng chung rồi tạo và cache factory Session cho tiến trình. Các request có thể
    dùng factory này để mở Session riêng."""

    return build_session_factory(get_engine())


def SessionLocal() -> Session:
    """Duy trì API tương thích cũ bằng cách gọi factory hiện hành để mở và trả về một Session mới.
    Caller chịu trách nhiệm đóng Session."""

    return get_session_factory()()


def get_db_from_factory(
    session_factory: sessionmaker[Session],
) -> Generator[Session, None, None]:
    """Mở một Session từ factory được truyền vào, yield cho request hoặc caller, rồi luôn đóng
    Session trong khối finally. Hàm không tự commit hoặc rollback transaction."""

    db = session_factory()
    try:
        yield db
    finally:
        db.close()


def get_db() -> Generator[Session, None, None]:
    """Cung cấp dependency FastAPI dùng session factory mặc định đã cache. Dependency yield Session
    theo request và ủy quyền việc đóng Session cho get_db_from_factory."""

    yield from get_db_from_factory(get_session_factory())

# Dùng trong quá trình phát triển API.

def execute_query(
    db: Session,
    query: str,
    params: Mapping[str, Any] | None = None,
) -> Result[Any]:
    """Thực thi câu SQL dạng text bằng các tham số có tên trên Session do caller sở hữu. Trả về
    SQLAlchemy Result; không commit hay rollback, vì transaction thuộc trách nhiệm của caller."""

    return db.execute(text(query), dict(params or {}))

def query_one(
    db: Session,
    query: str,
    params: Mapping[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Gọi execute_query, lấy hàng đầu tiên dưới dạng mapping rồi chuyển thành dict Python. Trả về
    None nếu truy vấn không có hàng; không thay đổi quyền sở hữu transaction."""

    row = execute_query(db, query, params).mappings().first()
    return dict(row) if row is not None else None


def query_many(
    db: Session,
    query: str,
    params: Mapping[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Gọi execute_query, lấy toàn bộ hàng dưới dạng mapping và chuyển mỗi hàng thành dict Python.
    Trả về danh sách rỗng nếu không có hàng; không commit transaction."""

    rows = execute_query(db, query, params).mappings().all()
    return [dict(row) for row in rows]
