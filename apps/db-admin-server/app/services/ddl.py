"""DDL preview and execution preparation for common PostgreSQL objects."""

from __future__ import annotations

import secrets
import time
from dataclasses import dataclass, field
from typing import Any

from app.core.contracts import DdlRequest
from app.core.responses import ApiError
from app.services.identifiers import qualified_name, quote_identifier


@dataclass(frozen=True)
class PreparedDdl:
    sql: str
    target: str
    warnings: list[str]
    impact: list[dict[str, Any]] = field(default_factory=list)


def _definition_required(request: DdlRequest, trace_id: str) -> str:
    if not request.definition_sql or not request.definition_sql.strip():
        raise ApiError(
            status_code=422,
            business_code="DB_ADMIN_DEFINITION_REQUIRED",
            message="A SQL definition is required for this object kind.",
            trace_id=trace_id,
        )
    definition = request.definition_sql.strip()
    if "\x00" in definition:
        raise ApiError(
            status_code=422,
            business_code="DB_ADMIN_INVALID_DEFINITION",
            message="The SQL definition contains an invalid character.",
            trace_id=trace_id,
        )
    # Import locally to keep the DDL/SQL executor modules acyclic.
    from app.services.sql_executor import analyze_sql

    analysis = analyze_sql(definition)
    if analysis.classification == "blocked":
        raise ApiError(
            status_code=422,
            business_code="DB_ADMIN_SQL_BLOCKED",
            message=analysis.warnings[0],
            trace_id=trace_id,
        )
    return definition.rstrip(";") + ";"


def prepare_ddl(request: DdlRequest, trace_id: str) -> PreparedDdl:
    schema = request.schema_name or "public"
    target = f"{request.kind}:{schema}.{request.object_name}"
    qualified = qualified_name(schema, request.object_name, trace_id)
    warnings: list[str] = []
    if request.cascade:
        warnings.append("CASCADE may remove dependent objects and cannot be undone by this API.")

    if request.kind == "schema":
        if request.operation == "create":
            return PreparedDdl(
                f"CREATE SCHEMA {quote_identifier(request.object_name, 'name', trace_id)};",
                target,
                warnings,
            )
        if request.operation == "drop":
            suffix = " CASCADE" if request.cascade else " RESTRICT"
            return PreparedDdl(
                f"DROP SCHEMA {quote_identifier(request.object_name, 'name', trace_id)}{suffix};",
                target,
                warnings,
            )
        if request.operation == "alter" and request.new_name:
            return PreparedDdl(
                f"ALTER SCHEMA {quote_identifier(request.object_name, 'name', trace_id)} RENAME TO "
                f"{quote_identifier(request.new_name, 'new_name', trace_id)};",
                target,
                warnings,
            )

    if request.kind == "table":
        if request.operation == "create":
            if not request.columns:
                raise ApiError(
                    status_code=422,
                    business_code="DB_ADMIN_COLUMNS_REQUIRED",
                    message="At least one table column is required.",
                    trace_id=trace_id,
                )
            column_names = {column.name for column in request.columns}
            missing_keys = [key for key in request.primary_key if key not in column_names]
            if missing_keys:
                raise ApiError(
                    status_code=422,
                    business_code="DB_ADMIN_PRIMARY_KEY_COLUMN_NOT_FOUND",
                    message="Primary key columns must be present in the table definition.",
                    trace_id=trace_id,
                )
            definitions = []
            for column in request.columns:
                item = f"{quote_identifier(column.name, 'column', trace_id)} {column.data_type}"
                if not column.nullable:
                    item += " NOT NULL"
                if column.default_sql:
                    item += f" DEFAULT {column.default_sql.strip()}"
                definitions.append(item)
            if request.primary_key:
                keys = ", ".join(
                    quote_identifier(key, "primary_key", trace_id) for key in request.primary_key
                )
                definitions.append(f"PRIMARY KEY ({keys})")
            return PreparedDdl(
                f"CREATE TABLE {qualified} ({', '.join(definitions)});", target, warnings
            )
        if request.operation == "drop":
            suffix = " CASCADE" if request.cascade else " RESTRICT"
            return PreparedDdl(f"DROP TABLE {qualified}{suffix};", target, warnings)
        if request.operation == "alter" and request.new_name:
            new_name = quote_identifier(request.new_name, "new_name", trace_id)
            return PreparedDdl(
                f"ALTER TABLE {qualified} RENAME TO {new_name};",
                target,
                warnings,
            )

    definition_kinds = {
        "view",
        "materialized_view",
        "function",
        "procedure",
        "trigger",
        "type",
        "sequence",
        "index",
        "constraint",
        "grant",
    }
    if request.kind in definition_kinds and request.definition_sql:
        return PreparedDdl(_definition_required(request, trace_id), target, warnings)

    if request.operation == "drop":
        suffix = " CASCADE" if request.cascade else " RESTRICT"
        if request.kind == "trigger" and request.parent_name:
            table = qualified_name(schema, request.parent_name, trace_id)
            trigger = quote_identifier(request.object_name, "name", trace_id)
            return PreparedDdl(f"DROP TRIGGER {trigger} ON {table}{suffix};", target, warnings)
        if request.kind == "constraint" and request.parent_name:
            table = qualified_name(schema, request.parent_name, trace_id)
            constraint = quote_identifier(request.object_name, "name", trace_id)
            return PreparedDdl(
                f"ALTER TABLE {table} DROP CONSTRAINT {constraint}{suffix};",
                target,
                warnings,
            )
        keyword = {
            "view": "VIEW",
            "materialized_view": "MATERIALIZED VIEW",
            "function": "FUNCTION",
            "procedure": "PROCEDURE",
            "type": "TYPE",
            "sequence": "SEQUENCE",
            "index": "INDEX",
            "constraint": "CONSTRAINT",
        }.get(request.kind)
        if keyword:
            signature = ""
            if request.kind in {"function", "procedure"}:
                signature = f"({request.arguments or ''})"
            return PreparedDdl(f"DROP {keyword} {qualified}{signature}{suffix};", target, warnings)

    if request.kind in {
        "view",
        "materialized_view",
        "function",
        "procedure",
        "trigger",
        "type",
        "sequence",
        "index",
        "constraint",
        "grant",
    }:
        return PreparedDdl(_definition_required(request, trace_id), target, warnings)

    raise ApiError(
        status_code=422,
        business_code="DB_ADMIN_UNSUPPORTED_DDL",
        message="This DDL operation is not supported.",
        trace_id=trace_id,
    )


class ConfirmationStore:
    def __init__(self) -> None:
        self._values: dict[str, tuple[float, str, str, str]] = {}

    def issue(self, subject: str, sql: str, target: str) -> str:
        token = secrets.token_urlsafe(24)
        self._values[token] = (time.monotonic() + 300, subject, sql, target)
        return token

    def consume(self, token: str, subject: str, sql: str, target: str) -> bool:
        expected = self._values.pop(token, None)
        return (
            expected is not None
            and expected[0] > time.monotonic()
            and expected[1:]
            == (
                subject,
                sql,
                target,
            )
        )
