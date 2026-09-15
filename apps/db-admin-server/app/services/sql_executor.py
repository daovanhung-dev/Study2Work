"""Classification and isolated execution of database-scoped SQL."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from sqlalchemy import Engine, text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import Settings
from app.core.database import configure_transaction_limits
from app.core.responses import ApiError
from app.services.ddl import ConfirmationStore

READ_PREFIXES = ("select", "with", "explain", "show", "describe", "desc")
BLOCKED_STATEMENT = re.compile(
    r"^(?:begin|commit|rollback|savepoint|release|set|reset|discard|load|"
    r"alter\s+system|create\s+role|alter\s+role|drop\s+role|copy)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class SqlAnalysis:
    classification: str
    statement_count: int
    requires_confirmation: bool
    warnings: list[str]


def _dollar_tag_at(sql: str, index: int) -> str | None:
    match = re.match(r"\$(?:[A-Za-z_][A-Za-z0-9_]*)?\$", sql[index:])
    return match.group(0) if match else None


def _statements(sql: str) -> list[str]:
    """Split SQL at top-level semicolons, preserving dollar-quoted bodies."""

    statements: list[str] = []
    current: list[str] = []
    index = 0
    single_quote = False
    double_quote = False
    dollar_tag: str | None = None
    line_comment = False
    block_comment = False
    while index < len(sql):
        if line_comment:
            if sql[index] == "\n":
                line_comment = False
                current.append(" ")
            index += 1
            continue
        if block_comment:
            if sql.startswith("*/", index):
                block_comment = False
                index += 2
            else:
                index += 1
            continue
        if dollar_tag:
            if sql.startswith(dollar_tag, index):
                current.append(dollar_tag)
                index += len(dollar_tag)
                dollar_tag = None
            else:
                current.append(sql[index])
                index += 1
            continue
        if single_quote:
            current.append(sql[index])
            if sql[index] == "'":
                if index + 1 < len(sql) and sql[index + 1] == "'":
                    current.append(sql[index + 1])
                    index += 2
                    continue
                single_quote = False
            index += 1
            continue
        if double_quote:
            current.append(sql[index])
            if sql[index] == '"':
                if index + 1 < len(sql) and sql[index + 1] == '"':
                    current.append(sql[index + 1])
                    index += 2
                    continue
                double_quote = False
            index += 1
            continue
        if sql.startswith("--", index):
            line_comment = True
            index += 2
            continue
        if sql.startswith("/*", index):
            block_comment = True
            index += 2
            continue
        if sql[index] == "'":
            single_quote = True
            current.append(sql[index])
            index += 1
            continue
        if sql[index] == '"':
            double_quote = True
            current.append(sql[index])
            index += 1
            continue
        if sql[index] == "$":
            tag = _dollar_tag_at(sql, index)
            if tag:
                dollar_tag = tag
                current.append(tag)
                index += len(tag)
                continue
        if sql[index] == ";":
            statement = "".join(current).strip()
            if statement:
                statements.append(statement)
            current = []
            index += 1
            continue
        current.append(sql[index])
        index += 1
    statement = "".join(current).strip()
    if statement:
        statements.append(statement)
    return statements


def analyze_sql(sql: str) -> SqlAnalysis:
    statements = [statement.lower() for statement in _statements(sql)]
    if not statements:
        return SqlAnalysis("unknown", 0, True, ["SQL is empty."])
    if any(BLOCKED_STATEMENT.match(statement) for statement in statements):
        return SqlAnalysis(
            "blocked",
            len(statements),
            True,
            [
                "Transaction-control, role, session, and COPY commands are blocked "
                "by request isolation."
            ],
        )
    read_only = all(
        any(
            statement.startswith(prefix)
            and (len(statement) == len(prefix) or statement[len(prefix)].isspace())
            for prefix in READ_PREFIXES
        )
        for statement in statements
    )
    classification = "read_only" if read_only else "mutation"
    if classification == "read_only":
        warnings = ["Result rows are capped by the configured max_rows limit."]
    else:
        warnings = ["This SQL can change database state and requires confirmation before commit."]
    return SqlAnalysis(classification, len(statements), classification != "read_only", warnings)


def _json_value(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool, list, dict)):
        return value
    return str(value)


class SqlExecutor:
    def __init__(
        self, engine: Engine, settings: Settings, confirmations: ConfirmationStore
    ) -> None:
        self.engine = engine
        self.settings = settings
        self.confirmations = confirmations

    def validate(self, sql: str, subject: str, trace_id: str) -> tuple[SqlAnalysis, str | None]:
        if len(sql.encode()) > self.settings.max_sql_bytes:
            raise ApiError(
                status_code=413,
                business_code="DB_ADMIN_SQL_TOO_LARGE",
                message="SQL exceeds the configured size limit.",
                trace_id=trace_id,
            )
        analysis = analyze_sql(sql)
        if analysis.classification == "blocked":
            raise ApiError(
                status_code=422,
                business_code="DB_ADMIN_SQL_BLOCKED",
                message=analysis.warnings[0],
                trace_id=trace_id,
            )
        token = (
            self.confirmations.issue(subject, sql, "sql")
            if analysis.requires_confirmation
            else None
        )
        return analysis, token

    def execute(
        self,
        *,
        sql: str,
        subject: str,
        confirmation_token: str | None,
        max_rows: int | None,
        trace_id: str,
    ) -> dict[str, Any]:
        analysis = analyze_sql(sql)
        if analysis.classification == "blocked":
            raise ApiError(
                status_code=422,
                business_code="DB_ADMIN_SQL_BLOCKED",
                message=analysis.warnings[0],
                trace_id=trace_id,
            )
        if analysis.requires_confirmation and not confirmation_token:
            raise ApiError(
                status_code=409,
                business_code="DB_ADMIN_CONFIRMATION_REQUIRED",
                message="Validate and confirm this SQL before execution.",
                trace_id=trace_id,
            )
        if analysis.requires_confirmation and not self.confirmations.consume(
            confirmation_token or "", subject, sql, "sql"
        ):
            raise ApiError(
                status_code=409,
                business_code="DB_ADMIN_CONFIRMATION_INVALID",
                message="The SQL confirmation is invalid or expired.",
                trace_id=trace_id,
            )
        row_limit = max_rows or self.settings.max_rows
        try:
            with self.engine.connect() as connection:
                transaction = connection.begin()
                try:
                    configure_transaction_limits(connection, self.settings)
                    if analysis.classification == "read_only":
                        connection.execute(text("SET TRANSACTION READ ONLY"))
                    result = connection.exec_driver_sql(sql)
                    columns = list(result.keys()) if result.returns_rows else []
                    raw_rows = result.fetchmany(row_limit + 1) if result.returns_rows else []
                    truncated = len(raw_rows) > row_limit
                    rows = [
                        {
                            column: _json_value(value)
                            for column, value in zip(columns, row, strict=True)
                        }
                        for row in raw_rows[:row_limit]
                    ]
                    if analysis.classification == "read_only":
                        transaction.rollback()
                    else:
                        transaction.commit()
                    return {
                        "classification": analysis.classification,
                        "columns": columns,
                        "rows": rows,
                        "rowCount": result.rowcount,
                        "truncated": truncated,
                    }
                except Exception:
                    transaction.rollback()
                    raise
        except SQLAlchemyError as exc:
            raise ApiError(
                status_code=400,
                business_code="DB_ADMIN_SQL_FAILED",
                message="PostgreSQL rejected the SQL statement.",
                trace_id=trace_id,
            ) from exc
