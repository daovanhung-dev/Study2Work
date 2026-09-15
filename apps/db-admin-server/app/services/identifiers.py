"""PostgreSQL identifier validation and quoting."""

from __future__ import annotations

import re

from app.core.responses import ApiError

IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_$]{0,62}$")


def validate_identifier(value: str, field: str, trace_id: str) -> str:
    if not IDENTIFIER_PATTERN.fullmatch(value):
        raise ApiError(
            status_code=422,
            business_code="DB_ADMIN_INVALID_IDENTIFIER",
            message=f"Invalid PostgreSQL identifier for {field}.",
            trace_id=trace_id,
        )
    return value


def quote_identifier(value: str, field: str, trace_id: str) -> str:
    validated = validate_identifier(value, field, trace_id)
    return '"' + validated.replace('"', '""') + '"'


def qualified_name(schema: str, name: str, trace_id: str) -> str:
    return (
        f"{quote_identifier(schema, 'schema', trace_id)}.{quote_identifier(name, 'name', trace_id)}"
    )
