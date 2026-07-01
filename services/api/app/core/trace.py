from __future__ import annotations

from fastapi import Request


def get_trace_id(request: Request) -> str:
    trace_id = getattr(request.state, "trace_id", None)
    if isinstance(trace_id, str) and trace_id:
        return trace_id
    return "00000000-0000-0000-0000-000000000000"
