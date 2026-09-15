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
    AuditQuery,
    DdlApplyRequest,
    DdlRequest,
    RowDelete,
    RowFilter,
    RowMutation,
    RowPreviewRequest,
    RowQuery,
    SqlExecuteRequest,
    SqlValidateRequest,
)
from app.core.database import configure_transaction_limits, get_connection
from app.core.responses import ApiError, success_response
from app.core.runtime import AdminResources, get_resources
from app.core.security import Principal, require_permission
from app.core.trace import get_trace_id
from app.services.catalog import get_catalog, get_ddl_impact, get_object_detail
from app.services.ddl import prepare_ddl
from app.services.rows import delete_row, insert_row, query_rows, update_row

router = APIRouter(prefix="/api/v1/admin", tags=["database admin"])
DbRead = Depends(require_permission("db_admin:read"))
DbWrite = Depends(require_permission("db_admin:write"))
DbSql = Depends(require_permission("db_admin:sql"))
DbConnection = Depends(get_connection)
Resources = Depends(get_resources)


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
    connection: Connection = DbConnection,
    _principal: Principal = DbRead,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    try:
        data = get_catalog(connection)
    except SQLAlchemyError as exc:
        raise _handle_database_error(exc, trace_id) from exc
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
    connection: Connection = DbConnection,
    _principal: Principal = DbRead,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    try:
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
    analysis, token = resources.sql_executor.validate(payload.sql, principal.subject, trace_id)
    data = {
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
    try:
        data = resources.sql_executor.execute(
            sql=payload.sql,
            subject=principal.subject,
            confirmation_token=payload.confirmation_token,
            max_rows=payload.max_rows,
            trace_id=trace_id,
        )
    except ApiError as exc:
        resources.audit.record(
            actor=principal.subject,
            action="sql.execute",
            target="sql",
            outcome="failed",
            trace_id=trace_id,
            sql=payload.sql,
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
        target="sql",
        outcome="success",
        trace_id=trace_id,
        sql=payload.sql,
        details={"classification": data["classification"], "rowCount": data["rowCount"]},
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
    connection: Connection = DbConnection,
    _principal: Principal = DbRead,
) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    try:
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
