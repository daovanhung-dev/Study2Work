from typing import Any

# Nhập các thành phần cần thiết từ FastAPI.
from fastapi import APIRouter, Depends, Header, Query, Request, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

# Nhập các thành phần từ core.
from app.core.database import get_db, get_engine
from app.core.trace import get_trace_id

# Nhập các thành phần từ những package nghiệp vụ của ứng dụng.
from app.modules.guest.api_01_auth_register.models import RegisterRequest
from app.modules.guest.api_01_auth_register.view import create_user
from app.modules.guest.api_02_auth_verify_email_send.models import VerifyEmailSendRequest
from app.modules.guest.api_02_auth_verify_email_send.view import (
    send_verification_email as dispatch_verification_email,
)
from app.modules.guest.api_03_auth_login.models import LoginRequest, RefreshRequest
from app.modules.guest.api_03_auth_login.view import login, refresh
from app.modules.guest.api_04_users_me.view import get_current_user
from app.modules.guest.api_05_categories.models import CategoryQuery
from app.modules.guest.api_05_categories.view import get_categories
from app.modules.guest.api_06_courses.models import CourseQuery
from app.modules.guest.api_06_courses.view import get_courses
from app.modules.guest.api_07_courses_search.models import CourseSearchQuery
from app.modules.guest.api_07_courses_search.view import search_courses as search_courses_view
from app.service.email.provider import (
    VerificationEmailProvider,
    get_verification_email_provider,
)

router = APIRouter(
    prefix="/api/v1",
    tags=["api v1"],
)
db_dependency = Depends(get_db)
category_query_dependency = Depends()
verification_provider_dependency = Depends(get_verification_email_provider)


def parse_course_query(
    category: int | None = Query(default=None),
    page: int = Query(default=1, json_schema_extra={"minimum": 1}),
    size: int = Query(
        default=20,
        json_schema_extra={"minimum": 1, "maximum": 100},
    ),
    sort: str | None = Query(default=None),
) -> CourseQuery:
    """Chuyển query đã parse thành model dữ liệu.

    Rule runtime được áp dụng trong validator của API.
    """
    return CourseQuery(category=category, page=page, size=size, sort=sort)


course_query_dependency = Depends(parse_course_query)


def parse_course_search_query(
    q: str | None = Query(default=None),
    category: int | None = Query(default=None),
    page: int = Query(default=1, json_schema_extra={"minimum": 1}),
    sort: str | None = Query(default=None),
) -> CourseSearchQuery:
    """Chuyển query đã parse thành model dữ liệu.

    Rule runtime được áp dụng trong validator của API.
    """
    return CourseSearchQuery(q=q, category=category, page=page, sort=sort)


course_search_query_dependency = Depends(parse_course_search_query)


@router.get("/hello")
def hello_world() -> dict[str, str]:
    """Xử lý GET /hello và trả thông điệp chào cố định để kiểm tra route API v1. Hàm không truy cập
    database hay tạo tác dụng phụ."""
    return {"message": "hello world!"}


@router.get("/test/db")
def test_db() -> dict[str, list[Any]]:
    """Mở kết nối engine, chạy câu SQL chỉ đọc SELECT NOW() và trả các giá trị thời gian trong
    trường result. Kết nối được đóng khi rời khối with; lỗi kết nối hoặc truy vấn được chuyển
    cho lớp xử lý exception của FastAPI."""
    with get_engine().connect() as connection:
        result = connection.execute(text("SELECT NOW()"))
        return {"result": [row[0] for row in result]}


# API #01 auth_register
@router.post(
    "/auth/register",
    status_code=status.HTTP_201_CREATED,
    response_model=dict[str, Any],
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "required": ["email", "password", "full_name"],
                        "properties": {
                            "email": {"type": "string", "format": "email", "maxLength": 255},
                            "password": {"type": "string", "minLength": 1},
                            "full_name": {
                                "type": "string",
                                "minLength": 1,
                                "maxLength": 150,
                            },
                        },
                    }
                }
            },
        }
    },
)
def register(
    user_data: RegisterRequest,
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận RegisterRequest, Session và trace ID của request rồi chuyển việc tạo tài khoản cho
    create_user. Route giữ mã HTTP 201; kiểm tra nghiệp vụ, giao dịch và dựng response do lớp
    view đảm nhiệm."""
    return create_user(
        user_data=user_data,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #03 auth_login
@router.post(
    "/auth/login",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "required": ["email", "password"],
                        "properties": {
                            "email": {"type": "string", "format": "email", "maxLength": 255},
                            "password": {"type": "string", "minLength": 1},
                        },
                    }
                }
            },
        }
    },
)
def authenticate(
    user_data: LoginRequest,
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận LoginRequest, Session và trace ID rồi chuyển quy trình xác thực cho login. Route giữ mã
    HTTP 200; việc kiểm tra thông tin đăng nhập, phát hành token và quản lý giao dịch do lớp
    view đảm nhiệm."""
    return login(
        user_data=user_data,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #03 auth_refresh
@router.post(
    "/auth/refresh",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "required": ["refresh_token"],
                        "properties": {"refresh_token": {"type": "string", "minLength": 1}},
                    }
                }
            },
        }
    },
)
def refresh_access_token(
    user_data: RefreshRequest,
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận RefreshRequest, Session và trace ID rồi chuyển việc xác thực, xoay vòng refresh token
    cho refresh. Route trả mã HTTP 200 khi thành công; lớp view sở hữu kiểm tra token và giao
    dịch."""
    return refresh(
        user_data=user_data,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #02 auth_verify_email_send
@router.post(
    "/auth/verify-email/send",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=dict[str, Any],
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "required": ["user_id", "email"],
                        "properties": {
                            "user_id": {"type": "integer"},
                            "email": {"type": "string", "format": "email"},
                        },
                    }
                }
            },
        }
    },
)
async def send_verification_email(
    user_data: VerifyEmailSendRequest,
    request: Request,
    provider: VerificationEmailProvider = verification_provider_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận yêu cầu gửi email xác minh và provider được inject, lấy trace ID rồi giao dispatch cho
    lớp view. Route trả mã HTTP 202 khi provider chấp nhận yêu cầu và không tự mở kết nối
    database."""
    raw_payload = await request.json()
    if not isinstance(raw_payload, dict):
        raw_payload = {}
    return dispatch_verification_email(
        user_data=user_data,
        raw_payload=raw_payload,
        provider=provider,
        trace_id=get_trace_id(request),
    )


# API #05 categories
@router.get(
    "/categories",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
)
def categories(
    request: Request,
    category_query: CategoryQuery = category_query_dependency,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận locale đã được phân tích, Session và trace ID rồi chuyển việc đọc danh mục cho
    get_categories. Route trả mã HTTP 200; view áp dụng locale mặc định, truy vấn và dựng
    envelope."""
    return get_categories(
        locale=category_query.locale,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #06 courses
@router.get(
    "/courses",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
)
def courses(
    request: Request,
    course_query: CourseQuery = course_query_dependency,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận bộ lọc danh sách khóa học, Session và trace ID rồi chuyển xử lý cho get_courses. Route
    trả mã HTTP 200; phân trang, truy vấn, kiểm tra tính toàn vẹn mentor và ánh xạ dữ liệu nằm
    trong view."""
    return get_courses(
        course_query=course_query,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #07 courses_search
@router.get(
    "/courses/search",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
)
def search_courses(
    request: Request,
    course_query: CourseSearchQuery = course_search_query_dependency,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận từ khóa cùng bộ lọc tìm kiếm, Session và trace ID rồi chuyển cho search_courses_view.
    Route trả mã HTTP 200; chuẩn hóa truy vấn, tìm kiếm, phân trang và dựng response do view đảm
    nhiệm."""
    return search_courses_view(
        course_query=course_query,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #04 users_me
@router.get(
    "/users/me",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
)
def current_user(
    request: Request,
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận header Authorization, Session và trace ID rồi chuyển việc xác thực cùng đọc hồ sơ cho
    get_current_user. Route trả mã HTTP 200 khi thành công; kiểm tra JWT, quyền Student và truy
    vấn hồ sơ do view thực hiện."""
    return get_current_user(
        authorization=authorization,
        db=db,
        trace_id=get_trace_id(request),
    )
