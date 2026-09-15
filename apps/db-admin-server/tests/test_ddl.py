from __future__ import annotations

import pytest
from app.core.contracts import ColumnDefinition, DdlRequest
from app.core.responses import ApiError
from app.services.ddl import ConfirmationStore, prepare_ddl


def test_schema_ddl_quotes_identifiers_and_defaults_to_restrict() -> None:
    request = DdlRequest(kind="schema", operation="drop", object_name="reporting")

    prepared = prepare_ddl(request, "trace-id")

    assert prepared.sql == 'DROP SCHEMA "reporting" RESTRICT;'


def test_table_ddl_rejects_primary_key_column_not_in_definition() -> None:
    request = DdlRequest(
        kind="table",
        operation="create",
        schema_name="public",
        object_name="events",
        columns=[ColumnDefinition(name="event_id", data_type="bigint", nullable=False)],
        primary_key=["missing_id"],
    )

    with pytest.raises(ApiError) as error:
        prepare_ddl(request, "trace-id")

    assert error.value.business_code == "DB_ADMIN_PRIMARY_KEY_COLUMN_NOT_FOUND"


def test_column_data_type_rejects_sql_fragments() -> None:
    with pytest.raises(ValueError):
        ColumnDefinition(name="event_id", data_type="integer, secret text")


def test_complex_drop_uses_definition_when_signature_is_required() -> None:
    request = DdlRequest(
        kind="function",
        operation="drop",
        schema_name="public",
        object_name="search_users",
        definition_sql="DROP FUNCTION public.search_users(text)",
    )

    prepared = prepare_ddl(request, "trace-id")

    assert prepared.sql == "DROP FUNCTION public.search_users(text);"


def test_function_drop_builder_emits_an_explicit_signature() -> None:
    request = DdlRequest(
        kind="function",
        operation="drop",
        schema_name="public",
        object_name="refresh_users",
    )

    prepared = prepare_ddl(request, "trace-id")

    assert prepared.sql == 'DROP FUNCTION "public"."refresh_users"() RESTRICT;'


def test_definition_cannot_escape_request_transaction() -> None:
    request = DdlRequest(
        kind="view",
        operation="create",
        schema_name="public",
        object_name="active_users",
        definition_sql="BEGIN",
    )

    with pytest.raises(ApiError) as error:
        prepare_ddl(request, "trace-id")

    assert error.value.business_code == "DB_ADMIN_SQL_BLOCKED"


def test_plpgsql_definition_can_contain_body_semicolons() -> None:
    request = DdlRequest(
        kind="function",
        operation="create",
        schema_name="public",
        object_name="touch_users",
        definition_sql="""CREATE FUNCTION public.touch_users() RETURNS void
LANGUAGE plpgsql AS $$
DECLARE
  marker integer;
BEGIN
  marker := 1;
END;
$$""",
    )

    prepared = prepare_ddl(request, "trace-id")

    assert prepared.sql.endswith("$$;")


def test_confirmation_token_is_single_use() -> None:
    store = ConfirmationStore()
    token = store.issue("admin", 'DROP TABLE "public"."events";', "table:public.events")

    sql = 'DROP TABLE "public"."events";'
    assert store.consume(token, "admin", sql, "table:public.events")
    assert not store.consume(token, "admin", sql, "table:public.events")
