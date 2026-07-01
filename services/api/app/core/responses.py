from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class ErrorDetail(BaseModel):
    field: str | None
    code: str
    message: str


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int


class SuccessEnvelope[DataT](BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    business_code: str
    message: str
    timestamp: str
    trace_id: str
    data: DataT
    pagination: PaginationMeta | None = None


class ErrorEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    business_code: str
    message: str
    timestamp: str
    trace_id: str
    errors: list[ErrorDetail]


def success_payload[DataT](
    *,
    business_code: str,
    message: str,
    trace_id: str,
    data: DataT,
    pagination: PaginationMeta | None = None,
) -> dict[str, object]:
    payload = SuccessEnvelope[DataT](
        business_code=business_code,
        message=message,
        timestamp=utc_now_iso(),
        trace_id=trace_id,
        data=data,
        pagination=pagination,
    ).model_dump(exclude_none=True)
    return _to_camel_payload(payload)


def error_payload(
    *,
    business_code: str,
    message: str,
    trace_id: str,
    errors: list[ErrorDetail],
) -> dict[str, object]:
    payload = ErrorEnvelope(
        business_code=business_code,
        message=message,
        timestamp=utc_now_iso(),
        trace_id=trace_id,
        errors=errors,
    ).model_dump()
    return _to_camel_payload(payload)


def _to_camel_payload(payload: dict[str, object]) -> dict[str, object]:
    key_map = {
        "business_code": "businessCode",
        "trace_id": "traceId",
        "page_size": "pageSize",
        "total_items": "totalItems",
        "total_pages": "totalPages",
    }
    converted: dict[str, object] = {}
    for key, value in payload.items():
        converted_key = key_map.get(key, key)
        if isinstance(value, dict):
            converted[converted_key] = _to_camel_payload(value)
        elif isinstance(value, list):
            converted[converted_key] = [
                _to_camel_payload(item) if isinstance(item, dict) else item for item in value
            ]
        else:
            converted[converted_key] = value
    return converted
