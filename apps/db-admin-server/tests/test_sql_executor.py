from __future__ import annotations

import pytest
from app.core.config import Settings
from app.core.responses import ApiError
from app.services.ddl import ConfirmationStore
from app.services.sql_executor import SqlExecutor, analyze_sql


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
