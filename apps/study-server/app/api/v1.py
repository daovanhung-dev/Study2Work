from typing import Any

# import framework
from fastapi import APIRouter, Depends, Header, Query, Request, status
from fastapi.exceptions import RequestValidationError
from sqlalchemy import text
from sqlalchemy.orm import Session

# import core's file
from app.core.database import get_db, get_engine
from app.core.trace import get_trace_id

# import folder's files
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
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    sort: str | None = Query(default=None),
) -> CourseQuery:
    """Parse query primitives and preserve the API validation envelope."""

    try:
        return CourseQuery(category=category, page=page, size=size, sort=sort)
    except ValueError as exc:
        raise RequestValidationError(
            [{"type": "value_error", "loc": ("query", "sort"), "msg": str(exc)}]
        ) from exc


course_query_dependency = Depends(parse_course_query)


def parse_course_search_query(
    q: str | None = Query(default=None),
    category: int | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    sort: str | None = Query(default=None),
) -> CourseSearchQuery:
    """Parse search query primitives and preserve the API error envelope."""

    try:
        return CourseSearchQuery(q=q, category=category, page=page, sort=sort)
    except ValueError as exc:
        raise RequestValidationError(
            [{"type": "value_error", "loc": ("query", "sort"), "msg": str(exc)}]
        ) from exc


course_search_query_dependency = Depends(parse_course_search_query)


@router.get("/hello")
def hello_world() -> dict[str, str]:
    return {"message": "hello world!"}


@router.get("/test/db")
def test_db() -> dict[str, list[Any]]:
    with get_engine().connect() as connection:
        result = connection.execute(text("SELECT NOW()"))
        return {"result": [row[0] for row in result]}


@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(
    user_data: RegisterRequest,
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any]:
    return create_user(
        user_data=user_data,
        db=db,
        trace_id=get_trace_id(request),
    )


@router.post("/auth/login", status_code=status.HTTP_200_OK)
def authenticate(
    user_data: LoginRequest,
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any]:
    return login(
        user_data=user_data,
        db=db,
        trace_id=get_trace_id(request),
    )


@router.post("/auth/refresh", status_code=status.HTTP_200_OK)
def refresh_access_token(
    user_data: RefreshRequest,
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any]:
    return refresh(
        user_data=user_data,
        db=db,
        trace_id=get_trace_id(request),
    )


@router.post("/auth/verify-email/send", status_code=status.HTTP_202_ACCEPTED)
def send_verification_email(
    user_data: VerifyEmailSendRequest,
    request: Request,
    provider: VerificationEmailProvider = verification_provider_dependency,
) -> dict[str, Any]:
    return dispatch_verification_email(
        user_data=user_data,
        provider=provider,
        trace_id=get_trace_id(request),
    )


@router.get("/categories", status_code=status.HTTP_200_OK)
def categories(
    request: Request,
    category_query: CategoryQuery = category_query_dependency,
    db: Session = db_dependency,
) -> dict[str, Any]:
    return get_categories(
        locale=category_query.locale,
        db=db,
        trace_id=get_trace_id(request),
    )


@router.get("/courses", status_code=status.HTTP_200_OK)
def courses(
    request: Request,
    course_query: CourseQuery = course_query_dependency,
    db: Session = db_dependency,
) -> dict[str, Any]:
    return get_courses(
        course_query=course_query,
        db=db,
        trace_id=get_trace_id(request),
    )


@router.get("/courses/search", status_code=status.HTTP_200_OK)
def search_courses(
    request: Request,
    course_query: CourseSearchQuery = course_search_query_dependency,
    db: Session = db_dependency,
) -> dict[str, Any]:
    return search_courses_view(
        course_query=course_query,
        db=db,
        trace_id=get_trace_id(request),
    )


@router.get("/users/me", status_code=status.HTTP_200_OK)
def current_user(
    request: Request,
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any]:
    return get_current_user(
        authorization=authorization,
        db=db,
        trace_id=get_trace_id(request),
    )
