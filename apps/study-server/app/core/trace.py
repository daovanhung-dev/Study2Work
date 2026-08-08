from uuid import uuid4

from fastapi import Request


TRACE_HEADER = "X-Trace-ID"


def create_trace_id() -> str:
    return str(uuid4())


def get_trace_id(request: Request) -> str:
    return getattr(request.state, "trace_id", create_trace_id())
