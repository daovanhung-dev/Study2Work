"""Read-only PostgreSQL catalog queries."""

from __future__ import annotations

from typing import Any

from sqlalchemy import Connection, text

from app.services.identifiers import qualified_name, validate_identifier

SCHEMAS_SQL = """
SELECT n.nspname AS name, pg_get_userbyid(n.nspowner) AS owner
FROM pg_namespace AS n
WHERE n.nspname NOT LIKE 'pg_%' AND n.nspname <> 'information_schema'
ORDER BY n.nspname
"""

TABLES_SQL = """
SELECT n.nspname AS schema_name, c.relname AS name,
       CASE c.relkind WHEN 'r' THEN 'table' WHEN 'p' THEN 'partitioned_table' END AS kind,
       c.reltuples::bigint AS estimated_rows,
       obj_description(c.oid, 'pg_class') AS comment
FROM pg_class AS c
JOIN pg_namespace AS n ON n.oid = c.relnamespace
WHERE c.relkind IN ('r', 'p')
  AND n.nspname NOT LIKE 'pg_%' AND n.nspname <> 'information_schema'
ORDER BY n.nspname, c.relname
"""

VIEWS_SQL = """
SELECT n.nspname AS schema_name, c.relname AS name,
       CASE c.relkind WHEN 'v' THEN 'view' WHEN 'm' THEN 'materialized_view' END AS kind,
       obj_description(c.oid, 'pg_class') AS comment
FROM pg_class AS c
JOIN pg_namespace AS n ON n.oid = c.relnamespace
WHERE c.relkind IN ('v', 'm')
  AND n.nspname NOT LIKE 'pg_%' AND n.nspname <> 'information_schema'
ORDER BY n.nspname, c.relname
"""

ROUTINES_SQL = """
SELECT n.nspname AS schema_name, p.proname AS name,
       CASE WHEN p.prokind = 'p' THEN 'procedure' ELSE 'function' END AS kind,
       pg_get_function_identity_arguments(p.oid) AS arguments,
       pg_get_function_result(p.oid) AS result,
       pg_get_functiondef(p.oid) AS definition
FROM pg_proc AS p
JOIN pg_namespace AS n ON n.oid = p.pronamespace
WHERE p.prokind IN ('f', 'p')
  AND n.nspname NOT LIKE 'pg_%' AND n.nspname <> 'information_schema'
ORDER BY n.nspname, p.proname, arguments
"""

TRIGGERS_SQL = """
SELECT ns.nspname AS schema_name, cls.relname AS table_name,
       tg.tgname AS name, pg_get_triggerdef(tg.oid) AS definition
FROM pg_trigger AS tg
JOIN pg_class AS cls ON cls.oid = tg.tgrelid
JOIN pg_namespace AS ns ON ns.oid = cls.relnamespace
WHERE NOT tg.tgisinternal
  AND ns.nspname NOT LIKE 'pg_%'
ORDER BY ns.nspname, cls.relname, tg.tgname
"""

TYPES_SQL = """
SELECT ns.nspname AS schema_name, typ.typname AS name,
       CASE WHEN typ.typtype = 'e' THEN 'enum' ELSE 'type' END AS kind,
       COALESCE(
         (SELECT json_agg(enumlabel ORDER BY enumsortorder)
          FROM pg_enum WHERE enumtypid = typ.oid), '[]'::json
       ) AS labels
FROM pg_type AS typ
JOIN pg_namespace AS ns ON ns.oid = typ.typnamespace
WHERE typ.typtype IN ('e', 'd', 'c')
  AND ns.nspname NOT LIKE 'pg_%' AND ns.nspname <> 'information_schema'
  AND typ.typname NOT LIKE '\\_%'
ORDER BY ns.nspname, typ.typname
"""

SEQUENCES_SQL = """
SELECT schemaname AS schema_name, sequencename AS name,
       data_type, start_value, min_value, max_value, increment_by, cycle
FROM pg_sequences
WHERE schemaname NOT LIKE 'pg_%' AND schemaname <> 'information_schema'
ORDER BY schemaname, sequencename
"""

INDEXES_SQL = """
SELECT schemaname AS schema_name, tablename AS table_name,
       indexname AS name, indexdef AS definition
FROM pg_indexes
WHERE schemaname NOT LIKE 'pg_%' AND schemaname <> 'information_schema'
ORDER BY schemaname, tablename, indexname
"""

CONSTRAINTS_SQL = """
SELECT ns.nspname AS schema_name, cls.relname AS table_name,
       con.conname AS name,
       CASE con.contype WHEN 'p' THEN 'primary_key' WHEN 'f' THEN 'foreign_key'
         WHEN 'u' THEN 'unique' WHEN 'c' THEN 'check' WHEN 'x' THEN 'exclusion'
         ELSE con.contype::text END AS kind,
       pg_get_constraintdef(con.oid) AS definition
FROM pg_constraint AS con
JOIN pg_class AS cls ON cls.oid = con.conrelid
JOIN pg_namespace AS ns ON ns.oid = cls.relnamespace
WHERE ns.nspname NOT LIKE 'pg_%' AND ns.nspname <> 'information_schema'
ORDER BY ns.nspname, cls.relname, con.conname
"""

GRANTS_SQL = """
SELECT table_schema AS schema_name, table_name AS name, table_name, grantee, privilege_type,
       is_grantable
FROM information_schema.role_table_grants
WHERE table_schema NOT LIKE 'pg_%' AND table_schema <> 'information_schema'
ORDER BY table_schema, table_name, grantee, privilege_type
"""

COLUMNS_SQL = """
SELECT c.column_name AS name, c.ordinal_position AS position,
       c.data_type, c.udt_name, c.is_nullable,
       c.column_default, c.is_identity, c.identity_generation,
       c.is_generated, c.generation_expression
FROM information_schema.columns AS c
WHERE c.table_schema = :schema_name AND c.table_name = :table_name
ORDER BY c.ordinal_position
"""

PRIMARY_KEY_SQL = """
SELECT a.attname AS name, array_position(i.indkey, a.attnum) AS position
FROM pg_index AS i
JOIN pg_attribute AS a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
JOIN pg_class AS c ON c.oid = i.indrelid
JOIN pg_namespace AS n ON n.oid = c.relnamespace
WHERE i.indisprimary AND n.nspname = :schema_name AND c.relname = :table_name
ORDER BY position
"""

DEPENDENTS_SQL = """
SELECT DISTINCT dependent_ns.nspname AS schema_name,
       dependent.relname AS name,
       CASE dependent.relkind
         WHEN 'r' THEN 'table' WHEN 'p' THEN 'partitioned_table'
         WHEN 'v' THEN 'view' WHEN 'm' THEN 'materialized_view'
         WHEN 'i' THEN 'index' WHEN 'S' THEN 'sequence'
         ELSE dependent.relkind::text
       END AS kind
FROM pg_depend AS dependency
JOIN pg_class AS dependent ON dependent.oid = dependency.objid
JOIN pg_namespace AS dependent_ns ON dependent_ns.oid = dependent.relnamespace
WHERE dependency.refobjid = to_regclass(:qualified_name)
  AND dependency.deptype IN ('n', 'a')
  AND dependent.oid <> to_regclass(:qualified_name)
ORDER BY dependent_ns.nspname, dependent.relname
LIMIT 100
"""

SCHEMA_IMPACT_SQL = """
SELECT n.nspname AS schema_name, c.relname AS name,
       CASE c.relkind
         WHEN 'r' THEN 'table' WHEN 'p' THEN 'partitioned_table'
         WHEN 'v' THEN 'view' WHEN 'm' THEN 'materialized_view'
         WHEN 'S' THEN 'sequence' ELSE c.relkind::text
       END AS kind
FROM pg_class AS c
JOIN pg_namespace AS n ON n.oid = c.relnamespace
WHERE n.nspname = :schema_name
UNION ALL
SELECT n.nspname AS schema_name, p.proname AS name,
       CASE WHEN p.prokind = 'p' THEN 'procedure' ELSE 'function' END AS kind
FROM pg_proc AS p
JOIN pg_namespace AS n ON n.oid = p.pronamespace
WHERE n.nspname = :schema_name
UNION ALL
SELECT n.nspname AS schema_name, t.typname AS name, 'type' AS kind
FROM pg_type AS t
JOIN pg_namespace AS n ON n.oid = t.typnamespace
WHERE n.nspname = :schema_name AND t.typtype IN ('e', 'd', 'c')
ORDER BY schema_name, name
LIMIT 500
"""


def _rows(
    connection: Connection, statement: str, params: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    return [dict(row) for row in connection.execute(text(statement), params or {}).mappings()]


def get_catalog(connection: Connection) -> dict[str, list[dict[str, Any]]]:
    return {
        "schemas": _rows(connection, SCHEMAS_SQL),
        "tables": _rows(connection, TABLES_SQL),
        "views": _rows(connection, VIEWS_SQL),
        "routines": _rows(connection, ROUTINES_SQL),
        "triggers": _rows(connection, TRIGGERS_SQL),
        "types": _rows(connection, TYPES_SQL),
        "sequences": _rows(connection, SEQUENCES_SQL),
        "indexes": _rows(connection, INDEXES_SQL),
        "constraints": _rows(connection, CONSTRAINTS_SQL),
        "grants": _rows(connection, GRANTS_SQL),
    }


def get_table_metadata(connection: Connection, schema_name: str, table_name: str) -> dict[str, Any]:
    return {
        "columns": _rows(
            connection, COLUMNS_SQL, {"schema_name": schema_name, "table_name": table_name}
        ),
        "primaryKey": _rows(
            connection, PRIMARY_KEY_SQL, {"schema_name": schema_name, "table_name": table_name}
        ),
    }


def get_ddl_impact(
    connection: Connection,
    *,
    kind: str,
    schema_name: str | None,
    object_name: str,
) -> list[dict[str, Any]]:
    """Return a bounded dependency/impact preview for destructive DDL."""

    schema = schema_name or "public"
    validate_identifier(schema, "schema", "ddl-preview")
    validate_identifier(object_name, "name", "ddl-preview")
    if kind == "schema":
        return _rows(connection, SCHEMA_IMPACT_SQL, {"schema_name": object_name})
    if kind not in {"table", "view", "materialized_view", "sequence", "index"}:
        return []
    return _rows(
        connection,
        DEPENDENTS_SQL,
        {"qualified_name": qualified_name(schema, object_name, "ddl-preview")},
    )


def get_object_detail(
    connection: Connection,
    *,
    kind: str,
    schema_name: str,
    object_name: str,
) -> dict[str, Any] | None:
    catalog = get_catalog(connection)
    source_key = {
        "schema": "schemas",
        "table": "tables",
        "view": "views",
        "materialized_view": "views",
        "function": "routines",
        "procedure": "routines",
        "trigger": "triggers",
        "type": "types",
        "sequence": "sequences",
        "index": "indexes",
        "constraint": "constraints",
        "grant": "grants",
    }.get(kind)
    if source_key is None:
        return None
    matches = []
    for item in catalog[source_key]:
        item_schema = item.get("schema_name", item.get("schema"))
        item_name = item.get("name")
        if kind == "trigger":
            item_name = item.get("name")
        if item_schema == schema_name and item_name == object_name:
            if kind in {"view", "materialized_view"} and item.get("kind") != kind:
                continue
            if kind in {"function", "procedure"} and item.get("kind") != kind:
                continue
            matches.append(item)
    if not matches:
        return None
    detail: dict[str, Any] = {
        "kind": kind,
        "schemaName": schema_name,
        "objectName": object_name,
        "items": matches,
    }
    if kind == "table":
        detail.update(get_table_metadata(connection, schema_name, object_name))
    return detail
