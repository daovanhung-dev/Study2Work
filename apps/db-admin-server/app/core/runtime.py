"""Application resources shared by request dependencies."""

from __future__ import annotations

from dataclasses import dataclass

from fastapi import Request
from sqlalchemy import Engine

from app.core.config import Settings, get_settings
from app.core.database import build_engine
from app.services.audit import AuditStore
from app.services.ddl import ConfirmationStore
from app.services.sql_executor import SqlExecutor


@dataclass
class AdminResources:
    settings: Settings
    engine: Engine
    audit: AuditStore
    confirmations: ConfirmationStore
    sql_executor: SqlExecutor


def build_resources(settings: Settings) -> AdminResources:
    engine = build_engine(settings)
    confirmations = ConfirmationStore()
    return AdminResources(
        settings=settings,
        engine=engine,
        audit=AuditStore(settings.audit_capacity),
        confirmations=confirmations,
        sql_executor=SqlExecutor(engine, settings, confirmations),
    )


def get_resources(request: Request) -> AdminResources:
    resources = getattr(request.app.state, "resources", None)
    if resources is None:
        resources = build_resources(get_settings())
        request.app.state.resources = resources
    return resources
