from __future__ import annotations

from fastapi import Request


def get_trace_id(request: Request) -> str:
    trace_id = getattr(request.state, "trace_id", None)
    return str(trace_id) if trace_id else ""
