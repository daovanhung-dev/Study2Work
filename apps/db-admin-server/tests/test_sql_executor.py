from __future__ import annotations

import pytest
from app.core.config import Settings
from app.core.responses import ApiError
from app.services.ddl import ConfirmationStore
from app.services.sql_executor import SqlExecutor, analyze_sql


class FakeResult:
    returns_rows = True
    rowcount = 1

    def __init__(self, schema_exists: bool = True) -> None:
        self.schema_exists = schema_exists

    def scalar_one_or_none(self) -> int | None:
        return 1 if self.schema_exists else None

    def keys(self) -> list[str]:
        return ["value"]

    def fetchmany(self, _size: int) -> list[tuple[int]]:
        return [(1,)]


class FakeTransaction:
    committed = False
    rolled_back = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True


class FakeConnection:
    def __init__(self, schema_exists: bool = True) -> None:
        self.schema_exists = schema_exists
        self.transaction = FakeTransaction()
        self.calls: list[tuple[str, dict[str, object]]] = []
        self.driver_sql: list[str] = []

    def __enter__(self) -> FakeConnection:
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def begin(self) -> FakeTransaction:
        return self.transaction

    def execute(self, statement: object, params: dict[str, object] | None = None) -> FakeResult:
        self.calls.append((str(statement), params or {}))
        return FakeResult(self.schema_exists)

    def exec_driver_sql(self, statement: str) -> FakeResult:
        self.driver_sql.append(statement)
        return FakeResult()


class FakeEngine:
    def __init__(self, schema_exists: bool = True) -> None:
        self.connection = FakeConnection(schema_exists)

    def connect(self) -> FakeConnection:
        return self.connection


def test_sql_analysis_classifies_read_only() -> None:
    result = analyze_sql("-- comment\nSELECT * FROM users")
    assert result.classification == "read_only"
    assert result.requires_confirmation is False


def test_sql_analysis_requires_confirmation_for_mutation() -> None:
    result = analyze_sql("UPDATE users SET full_name = 'Ada'")
    assert result.classification == "mutation"
    assert result.requires_confirmation is True


def test_transaction_control_is_blocked() -> None:
    result = analyze_sql("BEGIN")
    assert result.classification == "blocked"


def test_transaction_control_is_blocked_in_later_statement() -> None:
    result = analyze_sql("SELECT 1; COMMIT")
    assert result.classification == "blocked"


def test_multiple_read_statements_remain_read_only() -> None:
    result = analyze_sql("SELECT 1; SELECT 2;")
    assert result.classification == "read_only"
    assert result.statement_count == 2


def test_semicolon_in_string_does_not_create_a_statement() -> None:
    result = analyze_sql("SELECT 'COMMIT; still a string'")
    assert result.classification == "read_only"
    assert result.statement_count == 1


def test_validate_sql_returns_single_use_confirmation_token() -> None:
    settings = Settings(
        app_env="test",
        database_url="postgresql://user:password@localhost/database",
        jwt_issuer="issuer",
        jwt_audience="audience",
        dev_auth=True,
    )
    executor = SqlExecutor(object(), settings, ConfirmationStore())  # type: ignore[arg-type]
    analysis, token = executor.validate("CREATE TABLE users (id integer)", "admin", "trace")
    assert analysis.classification == "mutation"
    assert token


def test_confirmation_token_is_bound_to_database_and_schema() -> None:
    settings = Settings(
        app_env="test",
        database_url="postgresql://user:password@localhost/database",
        jwt_issuer="issuer",
        jwt_audience="audience",
        dev_auth=True,
    )
    confirmations = ConfirmationStore()
    executor = SqlExecutor(object(), settings, confirmations)  # type: ignore[arg-type]
    _, token = executor.validate(
        "CREATE TABLE users (id integer)",
        "admin",
        "trace",
        confirmation_target="sql:work_server:public",
    )

    assert token
    assert (
        confirmations.consume(
            token, "admin", "CREATE TABLE users (id integer)", "sql:study_server:public"
        )
        is False
    )


def test_validate_rejects_oversized_sql() -> None:
    settings = Settings(
        app_env="test",
        database_url="postgresql://user:password@localhost/database",
        jwt_issuer="issuer",
        jwt_audience="audience",
        dev_auth=True,
        max_sql_bytes=1024,
    )
    executor = SqlExecutor(object(), settings, ConfirmationStore())  # type: ignore[arg-type]
    with pytest.raises(ApiError) as error:
        executor.validate("x" * 2_000, "admin", "trace")
    assert error.value.status_code == 413


def test_execute_uses_selected_database_and_transaction_search_path() -> None:
    settings = Settings(
        app_env="test",
        database_url="postgresql://user:password@localhost/database",
        jwt_issuer="issuer",
        jwt_audience="audience",
        dev_auth=True,
    )
    work = FakeEngine()
    study = FakeEngine()
    executor = SqlExecutor(
        {"work_server": work, "study_server": study}, settings, ConfirmationStore()
    )  # type: ignore[arg-type]

    result = executor.execute(
        sql="SELECT 1",
        subject="admin",
        confirmation_token=None,
        max_rows=None,
        trace_id="trace",
        database="work_server",
        schema_name="public",
    )

    assert result["rows"] == [{"value": 1}]
    assert work.connection.driver_sql == ["SELECT 1"]
    assert study.connection.driver_sql == []
    assert work.connection.transaction.rolled_back is True
    assert work.connection.transaction.committed is False
    assert any(
        "set_config('search_path'" in statement and params["search_path"] == '"public"'
        for statement, params in work.connection.calls
    )


def test_execute_rejects_schema_that_is_not_present_in_selected_database() -> None:
    settings = Settings(
        app_env="test",
        database_url="postgresql://user:password@localhost/database",
        jwt_issuer="issuer",
        jwt_audience="audience",
        dev_auth=True,
    )
    engine = FakeEngine(schema_exists=False)
    executor = SqlExecutor({"work_server": engine}, settings, ConfirmationStore())  # type: ignore[arg-type]

    with pytest.raises(ApiError) as error:
        executor.execute(
            sql="SELECT 1",
            subject="admin",
            confirmation_token=None,
            max_rows=None,
            trace_id="trace",
            database="work_server",
            schema_name="missing_schema",
        )

    assert error.value.business_code == "DB_ADMIN_SCHEMA_NOT_FOUND"
    assert engine.connection.driver_sql == []
    assert engine.connection.transaction.rolled_back is True
