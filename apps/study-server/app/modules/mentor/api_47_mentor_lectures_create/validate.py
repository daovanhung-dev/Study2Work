"""Kiểm tra path và JSON asset references cho API #47."""

import json

from app.core.responses import ErrorDetail, error_response
from starlette.responses import JSONResponse

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1


def _validation_error(trace_id: str, *, field: str, message: str) -> JSONResponse:
    """Dựng validation envelope chuẩn cho một trường API #47 không hợp lệ."""

    # Giữ lỗi tại ranh giới HTTP để response luôn theo envelope Study API.
    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Dữ liệu đầu vào không hợp lệ.",
        trace_id=trace_id,
        errors=[
            ErrorDetail(
                field=field,
                code="VALUE_ERROR",
                message=message,
            )
        ],
    )


def validate_lecture_course_id(course_id: int, *, trace_id: str) -> JSONResponse | None:
    """Từ chối course ID ngoài signed int64 trước khi dùng trong query."""

    if INT64_MIN <= course_id <= INT64_MAX:
        return None
    # Ánh xạ path ngoài miền int64 thành lỗi validation của catalog API #47.
    return _validation_error(
        trace_id,
        field="course_id",
        message="Input should be a signed 64-bit integer",
    )


def validate_asset_refs(asset_refs: str, *, trace_id: str) -> list[int] | JSONResponse:
    """Parse JSON array asset IDs, cho phép mảng rỗng và từ chối ID trùng/sai kiểu."""

    try:
        # Giải mã chuỗi JSON trước khi kiểm tra shape và kiểu từng ID.
        decoded = json.loads(asset_refs)
    except (json.JSONDecodeError, TypeError):
        return _validation_error(
            trace_id,
            field="asset_refs",
            message="Input should be a JSON array of unique signed 64-bit integers",
        )

    if type(decoded) is not list:
        return _validation_error(
            trace_id,
            field="asset_refs",
            message="Input should be a JSON array of unique signed 64-bit integers",
        )

    # Yêu cầu từng phần tử là integer JSON thật, nằm trong miền int64.
    if any(
        type(asset_id) is not int or not INT64_MIN <= asset_id <= INT64_MAX
        for asset_id in decoded
    ):
        return _validation_error(
            trace_id,
            field="asset_refs",
            message="Input should be a JSON array of unique signed 64-bit integers",
        )

    # Asset ID lặp bị từ chối để mỗi request ID ánh xạ tới đúng một UploadAsset.
    if len(decoded) != len(set(decoded)):
        return _validation_error(
            trace_id,
            field="asset_refs",
            message="Asset IDs must be unique",
        )

    return decoded
