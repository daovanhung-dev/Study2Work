"""Typed request/response contracts for the DB Admin API."""

from __future__ import annotations

import re
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.services.identifiers import IDENTIFIER_PATTERN

ObjectKind = Literal[
    "schema",
    "table",
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
]
ObjectOperation = Literal["create", "alter", "drop"]
RowOperation = Literal["insert", "update", "delete"]
_CUSTOM_TYPE = r"[A-Za-z_][A-Za-z0-9_$]{0,62}(?:\s*\.\s*[A-Za-z_][A-Za-z0-9_$]{0,62})?"
_BUILTIN_TYPE = (
    r"(?:smallint|integer|bigint|decimal|numeric|real|double\s+precision|"
    r"smallserial|serial|bigserial|boolean|bool|character(?:\s+varying)?|"
    r"varchar|char|text|date|time(?:\s+(?:with|without)\s+time\s+zone)?|"
    r"timetz|timestamp(?:\s+(?:with|without)\s+time\s+zone)?|timestamptz|"
    r"interval|uuid|json|jsonb|bytea|xml|inet|cidr|macaddr|tsvector|tsquery|money)"
)
DATA_TYPE_PATTERN = re.compile(
    rf"^(?:{_BUILTIN_TYPE}|{_CUSTOM_TYPE})(?:\s*\(\s*\d+(?:\s*,\s*\d+)?\s*\))?(?:\s*\[\s*\])?$",
    re.IGNORECASE,
)
USERNAME_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_.-]{0,63}$")


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ColumnDefinition(StrictModel):
    name: str = Field(min_length=1, max_length=63)
    data_type: str = Field(min_length=1, max_length=128)
    nullable: bool = True
    default_sql: str | None = Field(default=None, max_length=2_000)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not IDENTIFIER_PATTERN.fullmatch(value):
            raise ValueError("Invalid column identifier")
        return value

    @field_validator("data_type")
    @classmethod
    def validate_data_type(cls, value: str) -> str:
        normalized = " ".join(value.strip().split())
        if not DATA_TYPE_PATTERN.fullmatch(normalized):
            raise ValueError("Invalid PostgreSQL data type")
        return normalized


class DdlRequest(StrictModel):
    kind: ObjectKind
    operation: ObjectOperation
    schema_name: str | None = Field(default=None, max_length=63)
    object_name: str = Field(min_length=1, max_length=63)
    parent_name: str | None = Field(default=None, max_length=63)
    new_name: str | None = Field(default=None, max_length=63)
    arguments: str | None = Field(default=None, max_length=2_000)
    definition_sql: str | None = Field(default=None, max_length=200_000)
    columns: list[ColumnDefinition] = Field(default_factory=list, max_length=500)
    primary_key: list[str] = Field(default_factory=list, max_length=64)
    cascade: bool = False

    @field_validator("schema_name", "object_name", "parent_name", "new_name", "primary_key")
    @classmethod
    def validate_identifiers(cls, value: Any) -> Any:
        values = value if isinstance(value, list) else [value]
        for item in values:
            if item is not None and not IDENTIFIER_PATTERN.fullmatch(str(item)):
                raise ValueError("Invalid PostgreSQL identifier")
        return value

    @field_validator("arguments")
    @classmethod
    def validate_arguments(cls, value: str | None) -> str | None:
        if value is not None and (";" in value or "--" in value or "/*" in value or "*/" in value):
            raise ValueError("Invalid function signature")
        return value


class DdlPreviewResponse(StrictModel):
    sql: str
    warnings: list[str]
    requires_confirmation: bool = True
    confirmation_token: str
    target: str
    impact: list[dict[str, Any]] = Field(default_factory=list)


class DdlApplyRequest(DdlRequest):
    confirmation_token: str = Field(min_length=16, max_length=256)


class SqlTargetRequest(StrictModel):
    database: str = Field(min_length=1, max_length=64)
    schema_name: str = Field(min_length=1, max_length=63)

    @field_validator("schema_name")
    @classmethod
    def validate_schema_name(cls, value: str) -> str:
        if not IDENTIFIER_PATTERN.fullmatch(value):
            raise ValueError("Invalid PostgreSQL schema identifier")
        return value


class SqlValidateRequest(SqlTargetRequest):
    sql: str = Field(min_length=1, max_length=262_144)


class SqlValidateResponse(StrictModel):
    classification: Literal["read_only", "mutation", "blocked", "unknown"]
    statement_count: int
    requires_confirmation: bool
    warnings: list[str]
    confirmation_token: str | None = None


class SqlExecuteRequest(SqlTargetRequest):
    sql: str = Field(min_length=1, max_length=262_144)
    confirmation_token: str | None = Field(default=None, max_length=256)
    max_rows: int | None = Field(default=None, ge=1, le=100_000)


class RowFilter(StrictModel):
    column: str = Field(min_length=1, max_length=63)
    operator: Literal["eq", "contains", "is_null"] = "eq"
    value: Any = None


class RowQuery(StrictModel):
    limit: int = Field(default=100, ge=1, le=10_000)
    offset: int = Field(default=0, ge=0)
    sort_column: str | None = Field(default=None, max_length=63)
    sort_direction: Literal["asc", "desc"] = "asc"
    filters: list[RowFilter] = Field(default_factory=list, max_length=50)


class RowMutation(StrictModel):
    values: dict[str, Any] = Field(max_length=500)
    primary_key: dict[str, Any] | None = None
    confirmation_token: str | None = Field(default=None, min_length=16, max_length=256)


class RowDelete(StrictModel):
    primary_key: dict[str, Any]
    confirmation_token: str | None = Field(default=None, min_length=16, max_length=256)


class RowPreviewRequest(StrictModel):
    operation: RowOperation
    values: dict[str, Any] = Field(default_factory=dict, max_length=500)
    primary_key: dict[str, Any] | None = None


class RowPreviewResponse(StrictModel):
    operation: RowOperation
    target: str
    warnings: list[str]
    confirmation_token: str


class AuditQuery(StrictModel):
    limit: int = Field(default=100, ge=1, le=500)


class LoginRequest(StrictModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=12, max_length=256)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not USERNAME_PATTERN.fullmatch(normalized):
            raise ValueError("Invalid username")
        return normalized


class ChangePasswordRequest(StrictModel):
    current_password: str = Field(min_length=1, max_length=256)
    new_password: str = Field(min_length=12, max_length=256)


class CreateAccessAccountRequest(StrictModel):
    database: str = Field(min_length=1, max_length=64)
    username: str = Field(min_length=1, max_length=64)
    display_name: str = Field(min_length=1, max_length=150)
    schema_name: str = Field(min_length=1, max_length=63)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not USERNAME_PATTERN.fullmatch(normalized):
            raise ValueError("Invalid username")
        return normalized

    @field_validator("display_name")
    @classmethod
    def validate_display_name(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Display name cannot be blank")
        return normalized

    @field_validator("schema_name")
    @classmethod
    def validate_schema_name(cls, value: str) -> str:
        normalized = value.strip()
        if not IDENTIFIER_PATTERN.fullmatch(normalized):
            raise ValueError("Invalid PostgreSQL schema identifier")
        return normalized


class UpdateAccessAccountRequest(StrictModel):
    display_name: str | None = Field(default=None, min_length=1, max_length=150)
    status: Literal["active", "disabled"] | None = None

    @field_validator("display_name")
    @classmethod
    def validate_display_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        if not normalized:
            raise ValueError("Display name cannot be blank")
        return normalized


class ChangeSchemaRequest(StrictModel):
    database: str = Field(min_length=1, max_length=64)
    schema_name: str = Field(min_length=1, max_length=63)

    @field_validator("schema_name")
    @classmethod
    def validate_schema_name(cls, value: str) -> str:
        normalized = value.strip()
        if not IDENTIFIER_PATTERN.fullmatch(normalized):
            raise ValueError("Invalid PostgreSQL schema identifier")
        return normalized


class AccessAuditQuery(StrictModel):
    database: str | None = Field(default=None, max_length=64)
    actor: str | None = Field(default=None, max_length=64)
    action: str | None = Field(default=None, max_length=100)
    limit: int = Field(default=100, ge=1, le=500)
