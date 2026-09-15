"""Bounded local audit store plus structured server logging."""

from __future__ import annotations

import hashlib
import logging
from collections import deque
from datetime import UTC, datetime
from threading import Lock
from typing import Any

logger = logging.getLogger("db_admin.audit")


class AuditStore:
    def __init__(self, capacity: int) -> None:
        self._entries: deque[dict[str, Any]] = deque(maxlen=capacity)
        self._lock = Lock()

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
        return entry

    def list(self, limit: int = 100) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._entries)[:limit]
