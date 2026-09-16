"""Bounded local audit store plus structured server logging."""

from __future__ import annotations

import hashlib
import logging
from collections import deque
from datetime import UTC, datetime
from threading import Lock
from typing import Any

from sqlalchemy import Engine, text
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger("db_admin.audit")


class AuditStore:
    def __init__(
        self,
        capacity: int,
        engines: dict[str, Engine] | None = None,
        control_schema: str = "db_admin",
    ) -> None:
        self._entries: deque[dict[str, Any]] = deque(maxlen=capacity)
        self._lock = Lock()
        self._engines = engines or {}
        self._control_schema = '"' + control_schema.replace('"', '""') + '"'

    def record(
        self,
        *,
        actor: str,
        action: str,
        target: str,
        outcome: str,
        trace_id: str,
        sql: str | None = None,
        details: dict[str, Any] | None = None,
        database_target: str | None = None,
        actor_user_id: str | None = None,
        actor_username: str | None = None,
    ) -> dict[str, Any]:
        entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "actor": actor,
            "action": action,
            "target": target,
            "outcome": outcome,
            "traceId": trace_id,
            "sqlHash": hashlib.sha256(sql.encode()).hexdigest() if sql else None,
            "details": details or {},
        }
        with self._lock:
            self._entries.appendleft(entry)
        logger.info(
            "db_admin_action actor=%s action=%s target=%s outcome=%s trace_id=%s sql_hash=%s",
            actor,
            action,
            target,
            outcome,
            trace_id,
            entry["sqlHash"],
        )
        if database_target is not None:
            self._persist(
                entry,
                database_target=database_target,
                actor_user_id=actor_user_id,
                actor_username=actor_username,
            )
        return entry

    def _persist(
        self,
        entry: dict[str, Any],
        *,
        database_target: str,
        actor_user_id: str | None,
        actor_username: str | None,
    ) -> None:
        engine = self._engines.get(database_target)
        if engine is None:
            return
        target = str(entry["target"])
        resource_type, _, resource_name = target.partition(":")
        try:
            with engine.begin() as connection:
                connection.execute(
                    text(f"""
                        INSERT INTO {self._control_schema}.admin_audit_events
                            (event_id, actor_user_id, actor_username, database_target,
                             action, resource_type, resource_name, outcome, trace_id,
                             sql_hash, metadata, created_at)
                        VALUES
                            (:event_id, :actor_user_id, :actor_username, :database_target,
                             :action, :resource_type, :resource_name, :outcome, :trace_id,
                             :sql_hash, CAST(:metadata AS JSONB), :created_at)
                    """),
                    {
                        "event_id": secrets_uuid(),
                        "actor_user_id": actor_user_id,
                        "actor_username": actor_username,
                        "database_target": database_target,
                        "action": entry["action"],
                        "resource_type": resource_type or None,
                        "resource_name": resource_name or None,
                        "outcome": entry["outcome"],
                        "trace_id": entry["traceId"],
                        "sql_hash": entry["sqlHash"],
                        "metadata": json_metadata(entry["details"]),
                        "created_at": entry["timestamp"],
                    },
                )
        except SQLAlchemyError as exc:
            # Audit persistence must not turn a successful database operation
            # into a failed request when an older target has not been bootstrapped.
            logger.warning(
                "DB Admin durable audit unavailable target=%s error=%s",
                database_target,
                type(exc).__name__,
            )

    def list_persistent(
        self,
        *,
        database: str | None,
        actor: str | None,
        action: str | None,
        limit: int,
        trace_id: str,
    ) -> list[dict[str, Any]]:
        targets = [database] if database else list(self._engines)
        entries: list[dict[str, Any]] = []
        statement = text(f"""
            SELECT created_at, actor_username, actor_user_id, database_target,
                   action, resource_type, resource_name, outcome, trace_id,
                   sql_hash, metadata
            FROM {self._control_schema}.admin_audit_events
            WHERE (:actor IS NULL OR actor_username = :actor OR actor_user_id::text = :actor)
              AND (:action IS NULL OR action = :action)
            ORDER BY created_at DESC
            LIMIT :limit
        """)
        for target in targets:
            engine = self._engines.get(target)
            if engine is None:
                continue
            try:
                with engine.connect() as connection:
                    for row in connection.execute(
                        statement, {"actor": actor, "action": action, "limit": limit}
                    ).mappings():
                        entries.append(
                            {
                                "timestamp": row["created_at"].isoformat(),
                                "actor": row["actor_username"]
                                or str(row["actor_user_id"] or "unknown"),
                                "action": row["action"],
                                "target": f"{row['resource_type']}:{row['resource_name']}",
                                "outcome": row["outcome"],
                                "traceId": row["trace_id"],
                                "sqlHash": row["sql_hash"],
                                "details": row["metadata"] or {},
                                "database": row["database_target"],
                            }
                        )
            except SQLAlchemyError as exc:
                logger.warning(
                    "DB Admin durable audit read unavailable target=%s trace_id=%s error=%s",
                    target,
                    trace_id,
                    type(exc).__name__,
                )
        entries.sort(key=lambda item: str(item["timestamp"]), reverse=True)
        return entries[:limit]

    def list(self, limit: int = 100) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._entries)[:limit]


def secrets_uuid() -> str:
    from uuid import uuid4

    return str(uuid4())


def json_metadata(value: dict[str, Any]) -> str:
    import json

    return json.dumps(value, default=str, separators=(",", ":"))
