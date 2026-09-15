"""Safe, primary-key-aware table data access."""

from __future__ import annotations

from typing import Any

from psycopg.types.json import Json, Jsonb
from sqlalchemy import Connection, text

from app.core.contracts import RowFilter, RowMutation, RowQuery
from app.core.responses import ApiError
from app.services.catalog import get_table_metadata
from app.services.identifiers import qualified_name, quote_identifier, validate_identifier

TABLE_KIND_SQL = """
SELECT c.relkind
FROM pg_class AS c
JOIN pg_namespace AS n ON n.oid = c.relnamespace
WHERE n.nspname = :schema_name AND c.relname = :table_name
"""


def _table_info(
    connection: Connection, schema_name: str, table_name: str, trace_id: str
) -> dict[str, Any]:
    validate_identifier(schema_name, "schema", trace_id)
    validate_identifier(table_name, "table", trace_id)
    row = (
        connection.execute(
            text(TABLE_KIND_SQL), {"schema_name": schema_name, "table_name": table_name}
        )
        .mappings()
        .first()
    )
    if row is None:
        raise ApiError(
            status_code=404,
            business_code="DB_ADMIN_OBJECT_NOT_FOUND",
            message="The table was not found.",
            trace_id=trace_id,
        )
    if row["relkind"] not in {"r", "p"}:
        raise ApiError(
            status_code=422,
            business_code="DB_ADMIN_TABLE_REQUIRED",
            message="The selected object is not a base table.",
            trace_id=trace_id,
        )
    metadata = get_table_metadata(connection, schema_name, table_name)
    return {
        "columns": [str(item["name"]) for item in metadata["columns"]],
        "primaryKey": [str(item["name"]) for item in metadata["primaryKey"]],
        "columnTypes": {str(item["name"]): str(item["data_type"]) for item in metadata["columns"]},
        "metadata": metadata,
    }


def _parameter(value: Any, data_type: str | None) -> Any:
    if data_type == "jsonb":
        return Jsonb(value)
    if data_type == "json":
        return Json(value)
    return value


def _where_clause(
    filters: list[RowFilter],
    columns: set[str],
    column_types: dict[str, str],
    trace_id: str,
) -> tuple[str, dict[str, Any]]:
    clauses: list[str] = []
    params: dict[str, Any] = {}
    for index, item in enumerate(filters):
        if item.column not in columns:
            raise ApiError(
                status_code=422,
                business_code="DB_ADMIN_INVALID_COLUMN",
                message="The filter column does not exist.",
                trace_id=trace_id,
            )
        identifier = quote_identifier(item.column, "filter.column", trace_id)
        if item.operator == "is_null":
            clauses.append(f"{identifier} IS NULL")
        elif item.operator == "contains":
            key = f"filter_{index}"
            clauses.append(f"CAST({identifier} AS TEXT) ILIKE :{key}")
            params[key] = f"%{item.value or ''}%"
        else:
            key = f"filter_{index}"
            clauses.append(f"{identifier} = :{key}")
            params[key] = _parameter(item.value, column_types.get(item.column))
    return (f" WHERE {' AND '.join(clauses)}" if clauses else ""), params


def query_rows(
    connection: Connection, schema_name: str, table_name: str, query: RowQuery, trace_id: str
) -> dict[str, Any]:
    info = _table_info(connection, schema_name, table_name, trace_id)
    columns = set(info["columns"])
    where, params = _where_clause(query.filters, columns, info["columnTypes"], trace_id)
    order = ""
    if query.sort_column:
        if query.sort_column not in columns:
            raise ApiError(
                status_code=422,
                business_code="DB_ADMIN_INVALID_COLUMN",
                message="The sort column does not exist.",
                trace_id=trace_id,
            )
        direction = "DESC" if query.sort_direction == "desc" else "ASC"
        order = (
            f" ORDER BY {quote_identifier(query.sort_column, 'sort_column', trace_id)} {direction}"
        )
    statement = (
        f"SELECT * FROM {qualified_name(schema_name, table_name, trace_id)}"
        f"{where}{order} LIMIT :limit OFFSET :offset"
    )
    params.update({"limit": query.limit, "offset": query.offset})
    result = connection.execute(text(statement), params)
    rows = [dict(row) for row in result.mappings().all()]
    return {
        "columns": info["metadata"]["columns"],
        "primaryKey": info["metadata"]["primaryKey"],
        "rows": rows,
        "limit": query.limit,
        "offset": query.offset,
    }


def _validate_values(values: dict[str, Any], columns: set[str], trace_id: str) -> None:
    unknown = set(values) - columns
    if unknown:
        raise ApiError(
            status_code=422,
            business_code="DB_ADMIN_INVALID_COLUMN",
            message="A submitted column does not exist.",
            trace_id=trace_id,
        )


def insert_row(
    connection: Connection, schema_name: str, table_name: str, mutation: RowMutation, trace_id: str
) -> dict[str, Any]:
    info = _table_info(connection, schema_name, table_name, trace_id)
    if not info["primaryKey"]:
        raise ApiError(
            status_code=409,
            business_code="DB_ADMIN_PRIMARY_KEY_REQUIRED",
            message="Tables without a primary key are read-only.",
            trace_id=trace_id,
        )
    columns = set(info["columns"])
    _validate_values(mutation.values, columns, trace_id)
    if not mutation.values:
        raise ApiError(
            status_code=422,
            business_code="DB_ADMIN_VALUES_REQUIRED",
            message="At least one row value is required.",
            trace_id=trace_id,
        )
    names = list(mutation.values)
    quoted = ", ".join(quote_identifier(name, "values", trace_id) for name in names)
    placeholders = ", ".join(f":value_{index}" for index in range(len(names)))
    values = {
        f"value_{index}": _parameter(mutation.values[name], info["columnTypes"].get(name))
        for index, name in enumerate(names)
    }
    statement = (
        f"INSERT INTO {qualified_name(schema_name, table_name, trace_id)} ({quoted}) "
        f"VALUES ({placeholders}) RETURNING *"
    )
    result = connection.execute(text(statement), values)
    row = result.mappings().first()
    if row is None:
        raise ApiError(
            status_code=500,
            business_code="DB_ADMIN_MUTATION_FAILED",
            message="The row was not created.",
            trace_id=trace_id,
        )
    return dict(row)


def update_row(
    connection: Connection, schema_name: str, table_name: str, mutation: RowMutation, trace_id: str
) -> dict[str, Any]:
    info = _table_info(connection, schema_name, table_name, trace_id)
    primary_key = info["primaryKey"]
    if not primary_key:
        raise ApiError(
            status_code=409,
            business_code="DB_ADMIN_PRIMARY_KEY_REQUIRED",
            message="Rows without a primary key are read-only.",
            trace_id=trace_id,
        )
    if not mutation.primary_key or set(mutation.primary_key) != set(primary_key):
        raise ApiError(
            status_code=422,
            business_code="DB_ADMIN_PRIMARY_KEY_REQUIRED",
            message="All primary-key values are required.",
            trace_id=trace_id,
        )
    _validate_values(mutation.values, set(info["columns"]), trace_id)
    values = {key: value for key, value in mutation.values.items() if key not in primary_key}
    if not values:
        raise ApiError(
            status_code=422,
            business_code="DB_ADMIN_VALUES_REQUIRED",
            message="At least one non-key value is required.",
            trace_id=trace_id,
        )
    set_parts = []
    params: dict[str, Any] = {}
    for index, (name, value) in enumerate(values.items()):
        key = f"value_{index}"
        set_parts.append(f"{quote_identifier(name, 'values', trace_id)} = :{key}")
        params[key] = _parameter(value, info["columnTypes"].get(name))
    where_parts = []
    for index, name in enumerate(primary_key):
        key = f"pk_{index}"
        where_parts.append(f"{quote_identifier(name, 'primary_key', trace_id)} = :{key}")
        params[key] = _parameter(mutation.primary_key[name], info["columnTypes"].get(name))
    statement = (
        f"UPDATE {qualified_name(schema_name, table_name, trace_id)} "
        f"SET {', '.join(set_parts)} WHERE {' AND '.join(where_parts)} RETURNING *"
    )
    result = connection.execute(text(statement), params)
    row = result.mappings().first()
    if row is None:
        raise ApiError(
            status_code=404,
            business_code="DB_ADMIN_ROW_NOT_FOUND",
            message="The row was not found.",
            trace_id=trace_id,
        )
    return dict(row)


def delete_row(
    connection: Connection,
    schema_name: str,
    table_name: str,
    primary_key: dict[str, Any],
    trace_id: str,
) -> None:
    info = _table_info(connection, schema_name, table_name, trace_id)
    keys = info["primaryKey"]
    if not keys:
        raise ApiError(
            status_code=409,
            business_code="DB_ADMIN_PRIMARY_KEY_REQUIRED",
            message="Rows without a primary key are read-only.",
            trace_id=trace_id,
        )
    if set(primary_key) != set(keys):
        raise ApiError(
            status_code=422,
            business_code="DB_ADMIN_PRIMARY_KEY_REQUIRED",
            message="All primary-key values are required.",
            trace_id=trace_id,
        )
    params = {
        f"pk_{index}": _parameter(primary_key[name], info["columnTypes"].get(name))
        for index, name in enumerate(keys)
    }
    where = " AND ".join(
        f"{quote_identifier(name, 'primary_key', trace_id)} = :pk_{index}"
        for index, name in enumerate(keys)
    )
    result = connection.execute(
        text(f"DELETE FROM {qualified_name(schema_name, table_name, trace_id)} WHERE {where}"),
        params,
    )
    if result.rowcount != 1:
        raise ApiError(
            status_code=404,
            business_code="DB_ADMIN_ROW_NOT_FOUND",
            message="The row was not found.",
            trace_id=trace_id,
        )
