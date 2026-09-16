"""HTTP routes for catalog inspection, DDL, SQL, data browsing and audit."""

from __future__ import annotations

import json
from typing import Any, Literal, cast

from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from sqlalchemy import Connection, text
from sqlalchemy.exc import SQLAlchemyError

from app.core.contracts import (
    AccessAuditQuery,
    AuditQuery,
    ChangePasswordRequest,
    ChangeSchemaRequest,
    CreateAccessAccountRequest,
    DdlApplyRequest,
    DdlRequest,
    LoginRequest,
    RowDelete,
    RowFilter,
    RowMutation,
    RowPreviewRequest,
    RowQuery,
    SqlExecuteRequest,
    SqlValidateRequest,
    UpdateAccessAccountRequest,
)
from app.core.database import configure_transaction_limits, ensure_schema_exists, get_connection
from app.core.responses import ApiError, success_response
from app.core.runtime import AdminResources, get_resources
from app.core.security import Principal, PrincipalDependency, require_permission, require_root
from app.core.trace import get_trace_id
from app.services.catalog import get_catalog, get_ddl_impact, get_object_detail
from app.services.ddl import prepare_ddl
from app.services.rows import delete_row, insert_row, query_rows, update_row

router = APIRouter(prefix="/api/v1/admin", tags=["database admin"])
DbRead = Depends(require_permission("db_admin:read"))
DbWrite = Depends(require_permission("db_admin:write"))
DbSql = Depends(require_permission("db_admin:sql"))
DbManage = Depends(require_root)
DbConnection = Depends(get_connection)
Resources = Depends(get_resources)


def _sql_confirmation_target(database: str, schema_name: str) -> str:
    return f"sql:{database}:{schema_name}"


def _legacy_scope(
    resources: AdminResources, principal: Principal, schema: str, trace_id: str
) -> Any:
    """Keep old routes on their compatibility target while applying bindings."""

    if principal.is_root:
        return resources.engine
    return resources.access.require_schema(principal, "default", schema, trace_id)


def _filter_catalog_for_principal(
    data: dict[str, list[dict[str, Any]]],
    principal: Principal,
    database: str,
    resources: AdminResources,
) -> dict[str, list[dict[str, Any]]]:
    allowed = resources.access.allowed_schema_names(principal, database)
    if allowed is None:
        return data
    filtered: dict[str, list[dict[str, Any]]] = {}
    for key, items in data.items():
        filtered[key] = [
            item
            for item in items
            if (
                str(item.get("name", "")) in allowed
                if key == "schemas"
                else str(item.get("schema_name", item.get("schema", ""))) in allowed
            )
        ]
    return filtered


@router.post("/auth/login")
def auth_login(
    payload: LoginRequest,
    request: Request,
    resources: AdminResources = Resources,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    return success_response(
        business_code="DB_ADMIN_LOGIN_SUCCESS",
        message="Signed in to DB Admin.",
        trace_id=trace_id,
        data=resources.access.login(payload.username, payload.password, trace_id),
    )


@router.post("/auth/change-password")
def auth_change_password(
    payload: ChangePasswordRequest,
    request: Request,
    resources: AdminResources = Resources,
    principal: Principal = PrincipalDependency,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    return success_response(
        business_code="DB_ADMIN_PASSWORD_CHANGED",
        message="Password changed. Sign-in session renewed.",
        trace_id=trace_id,
        data=resources.access.change_password(
            principal, payload.current_password, payload.new_password, trace_id
        ),
    )


@router.get("/auth/me")
def auth_me(
    request: Request,
    resources: AdminResources = Resources,
    principal: Principal = PrincipalDependency,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    return success_response(
        business_code="DB_ADMIN_SESSION_LOADED",
        message="Current DB Admin session loaded.",
        trace_id=trace_id,
        data=resources.access.me(principal, trace_id),
    )


def _handle_database_error(
    exc: SQLAlchemyError,
    trace_id: str,
    message: str = "Database operation failed.",
) -> ApiError:
    return ApiError(
        status_code=400,
        business_code="DB_ADMIN_DATABASE_ERROR",
        message=message,
        trace_id=trace_id,
    )


def _row_confirmation_material(
    *,
    operation: str,
    schema_name: str,
    table_name: str,
    values: dict[str, Any],
    primary_key: dict[str, Any] | None,
) -> tuple[str, str]:
    target = f"row.{operation}:{schema_name}.{table_name}"
    material = json.dumps(
        {
            "operation": operation,
            "schema": schema_name,
            "table": table_name,
            "values": values,
            "primaryKey": primary_key,
        },
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )
    return material, target


def _ensure_row_confirmation(
    *,
    resources: AdminResources,
    principal: Principal,
    token: str | None,
    material: str,
    target: str,
    operation: str,
    trace_id: str,
) -> None:
    if token and resources.confirmations.consume(token, principal.subject, material, target):
        return
    resources.audit.record(
        actor=principal.subject,
        action=f"row.{operation}",
        target=target,
        outcome="failed",
        trace_id=trace_id,
        details={"businessCode": "DB_ADMIN_CONFIRMATION_INVALID"},
    )
    raise ApiError(
        status_code=409,
        business_code="DB_ADMIN_CONFIRMATION_INVALID",
        message="Preview and confirm the row mutation before execution.",
        trace_id=trace_id,
    )


@router.get("/databases")
def databases(
    request: Request,
    resources: AdminResources = Resources,
    principal: Principal = DbRead,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    data = {
        "databases": [
            {
                "id": target,
                "label": target.replace("_", " ").title(),
            }
            for target in resources.target_ids
            if target in resources.access.allowed_targets(principal)
        ]
    }
    return success_response(
        business_code="DB_ADMIN_DATABASES_LOADED",
        message="Configured databases loaded.",
        trace_id=trace_id,
        data=data,
    )


@router.get("/connection")
def connection_info(
    request: Request,
    connection: Connection = DbConnection,
    _principal: Principal = DbRead,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    try:
        row = (
            connection.execute(
                text(
                    "SELECT current_database() AS database, current_user AS user_name, "
                    "current_schema() AS schema_name, version() AS server_version"
                )
            )
            .mappings()
            .one()
        )
    except SQLAlchemyError as exc:
        raise _handle_database_error(
            exc, trace_id, "Unable to connect to the configured Neon database."
        ) from exc
    data = {
        "database": row["database"],
        "user": row["user_name"],
        "schema": row["schema_name"],
        "serverVersion": row["server_version"],
    }
    return success_response(
        business_code="DB_ADMIN_CONNECTION_READY",
        message="Database connection is ready.",
        trace_id=trace_id,
        data=jsonable_encoder(data),
    )


@router.get("/catalog")
def catalog(
    request: Request,
    database: str,
    resources: AdminResources = Resources,
    principal: Principal = DbRead,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    try:
        engine = resources.access.require_target(principal, database, trace_id)
        with engine.connect() as connection:
            data = get_catalog(connection)
        allowed = resources.access.current_schema_names(principal, database, trace_id)
        if allowed is not None:
            data = {
                key: [
                    item
                    for item in items
                    if (
                        str(item.get("name", "")) in allowed
                        if key == "schemas"
                        else str(item.get("schema_name", item.get("schema", ""))) in allowed
                    )
                ]
                for key, items in data.items()
            }
    except SQLAlchemyError as exc:
        raise _handle_database_error(exc, trace_id) from exc
    resources.audit.record(
        actor=principal.subject,
        actor_user_id=principal.user_id,
        actor_username=principal.username,
        action="catalog.read",
        target=database,
        database_target=database,
        outcome="success",
        trace_id=trace_id,
    )
    return success_response(
        business_code="DB_ADMIN_CATALOG_LOADED",
        message="Database catalog loaded.",
        trace_id=trace_id,
        data=jsonable_encoder(data),
    )


@router.get("/objects/{kind}/{schema_name}/{object_name}")
def object_detail(
    kind: str,
    schema_name: str,
    object_name: str,
    request: Request,
    resources: AdminResources = Resources,
    principal: Principal = DbRead,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    try:
        connection = _legacy_scope(resources, principal, schema_name, trace_id).connect()
        data = get_object_detail(
            connection,
            kind=kind,
            schema_name=schema_name,
            object_name=object_name,
        )
    except ApiError:
        raise
    except SQLAlchemyError as exc:
        raise _handle_database_error(exc, trace_id) from exc
    finally:
        if "connection" in locals() and connection is not None:
            connection.close()
    if data is None:
        raise ApiError(
            status_code=404,
            business_code="DB_ADMIN_OBJECT_NOT_FOUND",
            message="The database object was not found.",
            trace_id=trace_id,
        )
    return success_response(
        business_code="DB_ADMIN_OBJECT_LOADED",
        message="Database object loaded.",
        trace_id=trace_id,
        data=jsonable_encoder(data),
    )


@router.post("/ddl/preview")
def ddl_preview(
    payload: DdlRequest,
    request: Request,
    resources: AdminResources = Resources,
    principal: Principal = DbWrite,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    _legacy_scope(resources, principal, payload.schema_name or "public", trace_id)
    prepared = prepare_ddl(payload, trace_id)
    if payload.operation == "drop":
        try:
            with resources.engine.connect() as connection:
                impact = get_ddl_impact(
                    connection,
                    kind=payload.kind,
                    schema_name=payload.schema_name,
                    object_name=payload.object_name,
                )
        except SQLAlchemyError as exc:
            raise _handle_database_error(
                exc, trace_id, "Unable to inspect DDL dependencies."
            ) from exc
        warnings = list(prepared.warnings)
        if impact:
            warnings.insert(0, f"Preview found {len(impact)} dependent or impacted object(s).")
        prepared = prepared.__class__(
            sql=prepared.sql,
            target=prepared.target,
            warnings=warnings,
            impact=impact,
        )
    token = resources.confirmations.issue(principal.subject, prepared.sql, prepared.target)
    data = {
        "sql": prepared.sql,
        "warnings": prepared.warnings,
        "requiresConfirmation": True,
        "confirmationToken": token,
        "target": prepared.target,
        "impact": prepared.impact,
    }
    return success_response(
        business_code="DB_ADMIN_DDL_PREPARED",
        message="DDL preview is ready for confirmation.",
        trace_id=trace_id,
        data=data,
    )


@router.post("/ddl/apply")
def ddl_apply(
    payload: DdlApplyRequest,
    request: Request,
    resources: AdminResources = Resources,
    principal: Principal = DbWrite,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    _legacy_scope(resources, principal, payload.schema_name or "public", trace_id)
    prepared = prepare_ddl(payload, trace_id)
    if not resources.confirmations.consume(
        payload.confirmation_token, principal.subject, prepared.sql, prepared.target
    ):
        resources.audit.record(
            actor=principal.subject,
            action=f"ddl.{payload.operation}",
            target=prepared.target,
            outcome="failed",
            trace_id=trace_id,
            details={"kind": payload.kind, "businessCode": "DB_ADMIN_CONFIRMATION_INVALID"},
        )
        raise ApiError(
            status_code=409,
            business_code="DB_ADMIN_CONFIRMATION_INVALID",
            message="The DDL confirmation is invalid or expired.",
            trace_id=trace_id,
        )
    try:
        with resources.engine.begin() as connection:
            configure_transaction_limits(connection, resources.settings)
            connection.exec_driver_sql(prepared.sql)
    except SQLAlchemyError as exc:
        resources.audit.record(
            actor=principal.subject,
            action=f"ddl.{payload.operation}",
            target=prepared.target,
            outcome="failed",
            trace_id=trace_id,
            details={"kind": payload.kind},
        )
        raise _handle_database_error(
            exc, trace_id, "PostgreSQL rejected the DDL operation."
        ) from exc
    resources.audit.record(
        actor=principal.subject,
        action=f"ddl.{payload.operation}",
        target=prepared.target,
        outcome="success",
        trace_id=trace_id,
        details={"kind": payload.kind, "cascade": payload.cascade},
    )
    return success_response(
        business_code="DB_ADMIN_DDL_APPLIED",
        message="DDL operation applied.",
        trace_id=trace_id,
        data={"target": prepared.target, "sql": prepared.sql},
    )


@router.post("/sql/validate")
def sql_validate(
    payload: SqlValidateRequest,
    request: Request,
    resources: AdminResources = Resources,
    principal: Principal = DbSql,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    engine = resources.access.require_schema(
        principal, payload.database, payload.schema_name, trace_id
    )
    # ``DEV_AUTH`` is a test-only bypass and existing unit tests intentionally
    # validate SQL without opening a Neon connection. Real local/prod auth
    # always performs the schema existence check here.
    if not resources.settings.dev_auth:
        with engine.connect() as connection:
            ensure_schema_exists(connection, payload.schema_name, trace_id)
    confirmation_target = _sql_confirmation_target(payload.database, payload.schema_name)
    analysis, token = resources.sql_executor.validate(
        payload.sql,
        principal.subject,
        trace_id,
        confirmation_target=confirmation_target,
    )
    data = {
        "database": payload.database,
        "schemaName": payload.schema_name,
        "classification": analysis.classification,
        "statementCount": analysis.statement_count,
        "requiresConfirmation": analysis.requires_confirmation,
        "warnings": analysis.warnings,
        "confirmationToken": token,
    }
    return success_response(
        business_code="DB_ADMIN_SQL_VALIDATED",
        message="SQL validation completed.",
        trace_id=trace_id,
        data=data,
    )


@router.post("/sql/execute")
def sql_execute(
    payload: SqlExecuteRequest,
    request: Request,
    resources: AdminResources = Resources,
    principal: Principal = DbSql,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    resources.access.require_schema(principal, payload.database, payload.schema_name, trace_id)
    confirmation_target = _sql_confirmation_target(payload.database, payload.schema_name)
    try:
        data = resources.sql_executor.execute(
            sql=payload.sql,
            subject=principal.subject,
            confirmation_token=payload.confirmation_token,
            max_rows=payload.max_rows,
            trace_id=trace_id,
            database=payload.database,
            schema_name=payload.schema_name,
            confirmation_target=confirmation_target,
        )
    except ApiError as exc:
        resources.audit.record(
            actor=principal.subject,
            action="sql.execute",
            target=confirmation_target,
            outcome="failed",
            trace_id=trace_id,
            sql=payload.sql,
            database_target=payload.database,
            actor_user_id=principal.user_id,
            actor_username=principal.username,
            details={"businessCode": exc.business_code},
        )
        raise
    except SQLAlchemyError as exc:
        raise _handle_database_error(
            exc, trace_id, "PostgreSQL rejected the SQL statement."
        ) from exc
    resources.audit.record(
        actor=principal.subject,
        action="sql.execute",
        target=confirmation_target,
        outcome="success",
        trace_id=trace_id,
        sql=payload.sql,
        database_target=payload.database,
        actor_user_id=principal.user_id,
        actor_username=principal.username,
        details={
            "database": payload.database,
            "schemaName": payload.schema_name,
            "classification": data["classification"],
            "rowCount": data["rowCount"],
        },
    )
    return success_response(
        business_code="DB_ADMIN_SQL_EXECUTED",
        message="SQL execution completed.",
        trace_id=trace_id,
        data=jsonable_encoder(data),
    )


def _parse_filters(value: str | None, trace_id: str) -> list[dict[str, Any]]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ApiError(
            status_code=422,
            business_code="DB_ADMIN_INVALID_FILTERS",
            message="Filters must be valid JSON.",
            trace_id=trace_id,
        ) from exc
    if not isinstance(parsed, list):
        raise ApiError(
            status_code=422,
            business_code="DB_ADMIN_INVALID_FILTERS",
            message="Filters must be a JSON array.",
            trace_id=trace_id,
        )
    try:
        return [RowFilter.model_validate(item).model_dump() for item in parsed]
    except ValidationError as exc:
        raise ApiError(
            status_code=422,
            business_code="DB_ADMIN_INVALID_FILTERS",
            message="Each filter must contain a valid column, operator and value.",
            trace_id=trace_id,
        ) from exc


@router.get("/tables/{schema_name}/{table_name}/rows")
def table_rows(
    schema_name: str,
    table_name: str,
    request: Request,
    limit: int = 100,
    offset: int = 0,
    sort_column: str | None = None,
    sort_direction: str = "asc",
    filters: str | None = None,
    resources: AdminResources = Resources,
    principal: Principal = DbRead,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    try:
        connection = _legacy_scope(resources, principal, schema_name, trace_id).connect()
        normalized_direction = sort_direction.lower()
        if normalized_direction not in {"asc", "desc"}:
            raise ApiError(
                status_code=422,
                business_code="DB_ADMIN_INVALID_SORT",
                message="Sort direction must be asc or desc.",
                trace_id=trace_id,
            )
        direction = cast(Literal["asc", "desc"], normalized_direction)
        query = RowQuery(
            limit=limit,
            offset=offset,
            sort_column=sort_column,
            sort_direction=direction,
            filters=[RowFilter(**item) for item in _parse_filters(filters, trace_id)],
        )
        data = query_rows(connection, schema_name, table_name, query, trace_id)
    except ApiError:
        raise
    except ValidationError as exc:
        raise ApiError(
            status_code=422,
            business_code="DB_ADMIN_INVALID_QUERY",
            message="The row query parameters are invalid.",
            trace_id=trace_id,
        ) from exc
    except SQLAlchemyError as exc:
        raise _handle_database_error(exc, trace_id) from exc
    finally:
        if "connection" in locals() and connection is not None:
            connection.close()
    return success_response(
        business_code="DB_ADMIN_ROWS_LOADED",
        message="Table rows loaded.",
        trace_id=trace_id,
        data=jsonable_encoder(data),
    )


@router.post("/tables/{schema_name}/{table_name}/rows/preview")
def table_row_preview(
    schema_name: str,
    table_name: str,
    payload: RowPreviewRequest,
    request: Request,
    resources: AdminResources = Resources,
    principal: Principal = DbWrite,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    _legacy_scope(resources, principal, schema_name, trace_id)
    material, target = _row_confirmation_material(
        operation=payload.operation,
        schema_name=schema_name,
        table_name=table_name,
        values=payload.values,
        primary_key=payload.primary_key,
    )
    token = resources.confirmations.issue(principal.subject, material, target)
    warning = {
        "insert": "One row will be inserted and committed.",
        "update": "One matching primary-key row will be updated and committed.",
        "delete": "The matching primary-key row will be deleted and cannot be recovered here.",
    }[payload.operation]
    return success_response(
        business_code="DB_ADMIN_ROW_PREPARED",
        message="Row mutation preview is ready for confirmation.",
        trace_id=trace_id,
        data={
            "operation": payload.operation,
            "target": target,
            "warnings": [warning],
            "confirmationToken": token,
        },
    )


@router.post("/tables/{schema_name}/{table_name}/rows")
def table_row_insert(
    schema_name: str,
    table_name: str,
    payload: RowMutation,
    request: Request,
    resources: AdminResources = Resources,
    principal: Principal = DbWrite,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    _legacy_scope(resources, principal, schema_name, trace_id)
    material, target = _row_confirmation_material(
        operation="insert",
        schema_name=schema_name,
        table_name=table_name,
        values=payload.values,
        primary_key=payload.primary_key,
    )
    _ensure_row_confirmation(
        resources=resources,
        principal=principal,
        token=payload.confirmation_token,
        material=material,
        target=target,
        operation="insert",
        trace_id=trace_id,
    )
    try:
        with resources.engine.begin() as connection:
            configure_transaction_limits(connection, resources.settings)
            row = insert_row(connection, schema_name, table_name, payload, trace_id)
    except ApiError as exc:
        resources.audit.record(
            actor=principal.subject,
            action="row.insert",
            target=f"{schema_name}.{table_name}",
            outcome="failed",
            trace_id=trace_id,
            details={"businessCode": exc.business_code},
        )
        raise
    except SQLAlchemyError as exc:
        raise _handle_database_error(exc, trace_id, "PostgreSQL rejected the row insert.") from exc
    resources.audit.record(
        actor=principal.subject,
        action="row.insert",
        target=f"{schema_name}.{table_name}",
        outcome="success",
        trace_id=trace_id,
    )
    return success_response(
        business_code="DB_ADMIN_ROW_CREATED",
        message="Row created.",
        trace_id=trace_id,
        data=jsonable_encoder(row),
    )


@router.patch("/tables/{schema_name}/{table_name}/rows")
def table_row_update(
    schema_name: str,
    table_name: str,
    payload: RowMutation,
    request: Request,
    resources: AdminResources = Resources,
    principal: Principal = DbWrite,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    _legacy_scope(resources, principal, schema_name, trace_id)
    material, target = _row_confirmation_material(
        operation="update",
        schema_name=schema_name,
        table_name=table_name,
        values=payload.values,
        primary_key=payload.primary_key,
    )
    _ensure_row_confirmation(
        resources=resources,
        principal=principal,
        token=payload.confirmation_token,
        material=material,
        target=target,
        operation="update",
        trace_id=trace_id,
    )
    try:
        with resources.engine.begin() as connection:
            configure_transaction_limits(connection, resources.settings)
            row = update_row(connection, schema_name, table_name, payload, trace_id)
    except ApiError as exc:
        resources.audit.record(
            actor=principal.subject,
            action="row.update",
            target=f"{schema_name}.{table_name}",
            outcome="failed",
            trace_id=trace_id,
            details={"businessCode": exc.business_code},
        )
        raise
    except SQLAlchemyError as exc:
        raise _handle_database_error(exc, trace_id, "PostgreSQL rejected the row update.") from exc
    resources.audit.record(
        actor=principal.subject,
        action="row.update",
        target=f"{schema_name}.{table_name}",
        outcome="success",
        trace_id=trace_id,
    )
    return success_response(
        business_code="DB_ADMIN_ROW_UPDATED",
        message="Row updated.",
        trace_id=trace_id,
        data=jsonable_encoder(row),
    )


@router.delete("/tables/{schema_name}/{table_name}/rows")
def table_row_delete(
    schema_name: str,
    table_name: str,
    payload: RowDelete,
    request: Request,
    resources: AdminResources = Resources,
    principal: Principal = DbWrite,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    _legacy_scope(resources, principal, schema_name, trace_id)
    material, target = _row_confirmation_material(
        operation="delete",
        schema_name=schema_name,
        table_name=table_name,
        values={},
        primary_key=payload.primary_key,
    )
    _ensure_row_confirmation(
        resources=resources,
        principal=principal,
        token=payload.confirmation_token,
        material=material,
        target=target,
        operation="delete",
        trace_id=trace_id,
    )
    try:
        with resources.engine.begin() as connection:
            configure_transaction_limits(connection, resources.settings)
            delete_row(connection, schema_name, table_name, payload.primary_key, trace_id)
    except ApiError as exc:
        resources.audit.record(
            actor=principal.subject,
            action="row.delete",
            target=f"{schema_name}.{table_name}",
            outcome="failed",
            trace_id=trace_id,
            details={"businessCode": exc.business_code},
        )
        raise
    except SQLAlchemyError as exc:
        raise _handle_database_error(exc, trace_id, "PostgreSQL rejected the row delete.") from exc
    resources.audit.record(
        actor=principal.subject,
        action="row.delete",
        target=f"{schema_name}.{table_name}",
        outcome="success",
        trace_id=trace_id,
    )
    return success_response(
        business_code="DB_ADMIN_ROW_DELETED", message="Row deleted.", trace_id=trace_id, data=None
    )


@router.get("/audit")
def audit(
    request: Request,
    limit: int = 100,
    resources: AdminResources = Resources,
    _principal: Principal = DbRead,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    query = AuditQuery(limit=limit)
    return success_response(
        business_code="DB_ADMIN_AUDIT_LOADED",
        message="Audit history loaded.",
        trace_id=trace_id,
        data={"entries": resources.audit.list(query.limit)},
    )


@router.get("/access/accounts")
def access_accounts(
    request: Request,
    database: str | None = None,
    resources: AdminResources = Resources,
    _principal: Principal = DbManage,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    return success_response(
        business_code="DB_ADMIN_ACCESS_ACCOUNTS_LOADED",
        message="Access accounts loaded.",
        trace_id=trace_id,
        data={"accounts": resources.access.list_accounts(database, trace_id)},
    )


@router.post("/access/accounts")
def access_create_account(
    payload: CreateAccessAccountRequest,
    request: Request,
    resources: AdminResources = Resources,
    principal: Principal = DbManage,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    data = resources.access.create_account(payload, trace_id)
    resources.audit.record(
        actor=principal.subject,
        actor_user_id=principal.user_id,
        actor_username=principal.username,
        action="access.account.create",
        target=f"{payload.database}:{payload.schema_name}",
        database_target=payload.database,
        outcome="success",
        trace_id=trace_id,
        details={"username": payload.username},
    )
    return success_response(
        business_code="DB_ADMIN_ACCESS_ACCOUNT_CREATED",
        message="Account created. Save the generated secret now; it will not be shown again.",
        trace_id=trace_id,
        data=data,
    )


@router.patch("/access/accounts/{user_id}")
def access_update_account(
    user_id: str,
    payload: UpdateAccessAccountRequest,
    request: Request,
    resources: AdminResources = Resources,
    principal: Principal = DbManage,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    return success_response(
        business_code="DB_ADMIN_ACCESS_ACCOUNT_UPDATED",
        message="Account updated.",
        trace_id=trace_id,
        data=resources.access.update_account(user_id, payload, principal, trace_id),
    )


@router.put("/access/accounts/{user_id}/schema")
def access_change_schema(
    user_id: str,
    payload: ChangeSchemaRequest,
    request: Request,
    resources: AdminResources = Resources,
    principal: Principal = DbManage,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    return success_response(
        business_code="DB_ADMIN_ACCESS_SCHEMA_CHANGED",
        message="Account schema binding updated. The previous schema was preserved.",
        trace_id=trace_id,
        data=resources.access.change_schema(user_id, payload, principal, trace_id),
    )


@router.post("/access/accounts/{user_id}/rotate-password")
def access_rotate_password(
    user_id: str,
    request: Request,
    resources: AdminResources = Resources,
    principal: Principal = DbManage,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    return success_response(
        business_code="DB_ADMIN_ACCESS_PASSWORD_ROTATED",
        message="Password rotated. Save the generated secret now; it will not be shown again.",
        trace_id=trace_id,
        data=resources.access.rotate_password(user_id, principal, trace_id),
    )


@router.get("/access/audit")
def access_audit(
    request: Request,
    database: str | None = None,
    actor: str | None = None,
    action: str | None = None,
    limit: int = 100,
    resources: AdminResources = Resources,
    _principal: Principal = DbManage,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    query = AccessAuditQuery(database=database, actor=actor, action=action, limit=limit)
    return success_response(
        business_code="DB_ADMIN_ACCESS_AUDIT_LOADED",
        message="Access audit loaded.",
        trace_id=trace_id,
        data={
            "entries": resources.access.list_audit(
                query.database, query.actor, query.action, query.limit, trace_id
            )
        },
    )
