"""Application resources shared by request dependencies."""

from __future__ import annotations

from dataclasses import dataclass

from fastapi import Request
from sqlalchemy import Engine

from app.core.config import Settings, get_settings
from app.core.database import build_engine
from app.core.responses import ApiError
from app.services.access import AccessService
from app.services.audit import AuditStore
from app.services.ddl import ConfirmationStore
from app.services.sql_executor import SqlExecutor


@dataclass
class AdminResources:
    settings: Settings
    engines: dict[str, Engine]
    legacy_engine: Engine
    audit: AuditStore
    confirmations: ConfirmationStore
    sql_executor: SqlExecutor
    access: AccessService

    @property
    def engine(self) -> Engine:
        """Compatibility engine for legacy single-target admin routes."""

        return self.legacy_engine

    @property
    def target_ids(self) -> tuple[str, ...]:
        return tuple(self.engines)

    def engine_for(self, target: str, trace_id: str) -> Engine:
        engine = self.engines.get(target)
        if engine is None:
            raise ApiError(
                status_code=422,
                business_code="DB_ADMIN_DATABASE_NOT_FOUND",
                message="The selected database is not configured.",
                trace_id=trace_id,
            )
        return engine


def build_resources(settings: Settings) -> AdminResources:
    target_urls = settings.target_urls()
    engines = {
        target: build_engine(
            settings.model_copy(update={"database_url": url, "database_targets": {}})
        )
        for target, url in target_urls.items()
    }
    legacy_engine = engines.get("default")
    if legacy_engine is None:
        legacy_engine = build_engine(settings)
    confirmations = ConfirmationStore()
    audit = AuditStore(
        settings.audit_capacity, engines=engines, control_schema=settings.control_schema
    )
    access = AccessService(engines, settings, audit)
    return AdminResources(
        settings=settings,
        engines=engines,
        legacy_engine=legacy_engine,
        audit=audit,
        confirmations=confirmations,
        sql_executor=SqlExecutor(engines, settings, confirmations),
        access=access,
    )


def get_resources(request: Request) -> AdminResources:
    resources = getattr(request.app.state, "resources", None)
    if resources is None:
        resources = build_resources(get_settings())
        request.app.state.resources = resources
    return resources
