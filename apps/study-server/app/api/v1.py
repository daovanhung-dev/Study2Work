from typing import Any

# Nhập các thành phần cần thiết từ FastAPI.
from fastapi import APIRouter, Depends, File, Form, Header, Path, Query, Request, UploadFile, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool
from starlette.responses import JSONResponse

# Nhập các thành phần từ core.
from app.core.database import get_db, get_engine
from app.core.trace import get_trace_id
from app.modules.admin.api_68_admin_users_list.models import GetAdminUsersEnvelope
from app.modules.admin.api_68_admin_users_list.view import get_admin_users

# Nhập các thành phần từ những package nghiệp vụ của ứng dụng.
from app.modules.admin.api_69_admin_user_detail.models import GetAdminUserEnvelope
from app.modules.admin.api_69_admin_user_detail.view import get_admin_user
from app.modules.admin.api_70_admin_user_update.models import (
    AdminUserUpdateRequest,
    UpdateAdminUserEnvelope,
)
from app.modules.admin.api_70_admin_user_update.view import update_admin_user
from app.modules.admin.api_71_admin_user_status.models import (
    AdminUserStatusRequest,
    UpdateAdminUserStatusEnvelope,
)
from app.modules.admin.api_71_admin_user_status.view import update_admin_user_status
from app.modules.admin.api_72_admin_user_delete.models import DeleteAdminUserEnvelope
from app.modules.admin.api_72_admin_user_delete.view import delete_admin_user
from app.modules.admin.api_73_admin_courses_list.models import GetAdminCoursesEnvelope
from app.modules.admin.api_73_admin_courses_list.view import get_admin_courses
from app.modules.admin.api_74_admin_course_detail.models import GetAdminCourseDetailEnvelope
from app.modules.admin.api_74_admin_course_detail.view import get_admin_course_detail
from app.modules.admin.api_75_admin_course_update.models import (
    AdminCourseUpdateRequest,
    UpdateAdminCourseEnvelope,
)
from app.modules.admin.api_75_admin_course_update.view import update_admin_course
from app.modules.admin.api_76_admin_course_status.models import (
    AdminCourseStatusRequest,
    UpdateAdminCourseStatusEnvelope,
)
from app.modules.admin.api_76_admin_course_status.view import update_admin_course_status
from app.modules.admin.api_77_admin_course_delete.models import DeleteAdminCourseEnvelope
from app.modules.admin.api_77_admin_course_delete.view import delete_admin_course
from app.modules.admin.api_78_admin_content_pending.models import (
    GetAdminPendingContentsEnvelope,
)
from app.modules.admin.api_78_admin_content_pending.view import get_admin_pending_contents
from app.modules.admin.api_79_admin_content_detail.models import GetAdminContentEnvelope
from app.modules.admin.api_79_admin_content_detail.view import get_admin_content
from app.modules.admin.api_80_admin_content_approve.models import ApproveAdminContentEnvelope
from app.modules.admin.api_80_admin_content_approve.view import approve_admin_content
from app.modules.admin.api_81_admin_content_reject.models import (
    RejectAdminContentEnvelope,
    RejectAdminContentRequest,
)
from app.modules.admin.api_81_admin_content_reject.view import reject_admin_content
from app.modules.admin.api_82_admin_lessons_list.models import GetAdminLessonsEnvelope
from app.modules.admin.api_82_admin_lessons_list.view import get_admin_lessons
from app.modules.admin.api_83_admin_lesson_detail.models import GetAdminLessonEnvelope
from app.modules.admin.api_83_admin_lesson_detail.view import get_admin_lesson_detail
from app.modules.admin.api_84_admin_lesson_update.models import (
    AdminLessonUpdateRequest,
    UpdateAdminLessonEnvelope,
)
from app.modules.admin.api_84_admin_lesson_update.view import update_admin_lesson
from app.modules.admin.api_85_admin_lesson_status.models import (
    AdminLessonStatusRequest,
    UpdateAdminLessonStatusEnvelope,
)
from app.modules.admin.api_85_admin_lesson_status.view import update_admin_lesson_status
from app.modules.admin.api_86_admin_lesson_delete.models import DeleteAdminLessonEnvelope
from app.modules.admin.api_86_admin_lesson_delete.view import delete_admin_lesson
from app.modules.admin.api_87_admin_quizzes_list.models import GetAdminQuizzesEnvelope
from app.modules.admin.api_87_admin_quizzes_list.view import get_admin_quizzes
from app.modules.admin.api_88_admin_quizzes_create.models import CreateAdminQuizEnvelope
from app.modules.admin.api_88_admin_quizzes_create.view import create_admin_quiz
from app.modules.admin.api_89_admin_quizzes_update.models import UpdateAdminQuizEnvelope
from app.modules.admin.api_89_admin_quizzes_update.view import update_admin_quiz
from app.modules.admin.api_90_admin_quizzes_delete.models import DeleteAdminQuizEnvelope
from app.modules.admin.api_90_admin_quizzes_delete.view import delete_admin_quiz
from app.modules.admin.api_91_admin_quizzes_statistics.models import (
    GetAdminQuizStatisticsEnvelope,
)
from app.modules.admin.api_91_admin_quizzes_statistics.view import get_admin_quiz_statistics
from app.modules.admin.api_92_admin_notifications_list.models import (
    GetAdminNotificationsEnvelope,
)
from app.modules.admin.api_92_admin_notifications_list.view import get_admin_notifications
from app.modules.admin.api_93_admin_notifications_create.models import (
    CreateAdminNotificationEnvelope,
)
from app.modules.admin.api_93_admin_notifications_create.view import create_admin_notification
from app.modules.admin.api_94_admin_notifications_update.models import (
    UpdateAdminNotificationEnvelope,
)
from app.modules.admin.api_94_admin_notifications_update.view import update_admin_notification
from app.modules.admin.api_95_admin_notifications_delete.models import (
    DeleteAdminNotificationEnvelope,
)
from app.modules.admin.api_95_admin_notifications_delete.view import delete_admin_notification
from app.modules.admin.api_96_admin_notifications_status.models import (
    GetAdminNotificationStatusEnvelope,
)
from app.modules.admin.api_96_admin_notifications_status.view import (
    get_admin_notification_status,
)
from app.modules.admin.api_97_admin_discussions_reported.models import (
    GetAdminReportedDiscussionsEnvelope,
)
from app.modules.admin.api_97_admin_discussions_reported.view import (
    get_admin_reported_discussions,
)
from app.modules.admin.api_98_admin_discussions_detail.models import (
    GetAdminDiscussionDetailEnvelope,
)
from app.modules.admin.api_98_admin_discussions_detail.view import get_admin_discussion_detail
from app.modules.guest._shared.course_catalog.constants import DEFAULT_PAGE, DEFAULT_SIZE
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
from app.modules.guest.api_08_courses_detail.view import get_course_detail
from app.modules.guest.api_09_courses_curriculum.view import get_course_curriculum
from app.modules.guest.api_11_courses_resources.view import (
    get_course_resources as get_course_resources_view,
)
from app.modules.guest.api_12_resources_detail.view import get_resource_detail
from app.modules.guest.api_13_users_me_avatar.models import AvatarUploadRequest
from app.modules.guest.api_13_users_me_avatar.view import upload_avatar
from app.modules.guest.api_14_users_me_profile.models import ProfileUpdateRequest
from app.modules.guest.api_14_users_me_profile.view import update_profile
from app.modules.guest.api_15_courses_enrollment_status.view import (
    get_enrollment_status as get_enrollment_status_view,
)
from app.modules.guest.api_21_users_me_progress.view import (
    get_user_progress as get_user_progress_view,
)
from app.modules.guest.api_22_lessons_access.view import (
    check_lesson_access as check_lesson_access_view,
)
from app.modules.guest.api_23_lessons_start.view import (
    start_lesson as start_lesson_view,
)
from app.modules.guest.api_24_lessons_detail.view import (
    get_lesson_detail as get_lesson_detail_view,
)
from app.modules.guest.api_25_lessons_progress.models import (
    LessonProgressUpdateRequest,
)
from app.modules.guest.api_25_lessons_progress.view import (
    update_lesson_progress as update_lesson_progress_view,
)
from app.modules.mentor.api_46_mentor_courses.models import MentorCourseQuery
from app.modules.mentor.api_46_mentor_courses.view import get_mentor_courses
from app.modules.mentor.api_47_mentor_lectures_create.models import (
    CreateLectureEnvelope,
    CreateLectureRequest,
)
from app.modules.mentor.api_47_mentor_lectures_create.view import create_lecture
from app.modules.mentor.api_48_mentor_lecture_detail.models import GetLectureEnvelope
from app.modules.mentor.api_48_mentor_lecture_detail.view import get_lecture
from app.modules.mentor.api_49_mentor_content_list.models import GetCourseContentsEnvelope
from app.modules.mentor.api_49_mentor_content_list.view import get_course_contents
from app.modules.mentor.api_50_mentor_content_create.models import (
    CreateContentEnvelope,
    CreateContentRequest,
)
from app.modules.mentor.api_50_mentor_content_create.view import create_content
from app.modules.mentor.api_51_mentor_content_update.models import (
    UpdateContentEnvelope,
    UpdateContentRequest,
)
from app.modules.mentor.api_51_mentor_content_update.view import update_content
from app.modules.mentor.api_52_mentor_content_publish.models import (
    PublishContentEnvelope,
    PublishContentRequest,
)
from app.modules.mentor.api_52_mentor_content_publish.view import publish_content
from app.modules.mentor.api_53_mentor_content_delete.models import DeleteContentEnvelope
from app.modules.mentor.api_53_mentor_content_delete.view import delete_content
from app.modules.mentor.api_54_mentor_submissions_list.models import (
    GetMentorSubmissionsEnvelope,
    MentorSubmissionsQuery,
)
from app.modules.mentor.api_54_mentor_submissions_list.view import get_mentor_submissions
from app.modules.mentor.api_55_mentor_submissions_detail.models import (
    GetMentorSubmissionEnvelope,
)
from app.modules.mentor.api_55_mentor_submissions_detail.view import get_mentor_submission
from app.modules.mentor.api_56_mentor_submissions_grade.models import (
    GradeMentorSubmissionEnvelope,
    GradeSubmissionRequest,
)
from app.modules.mentor.api_56_mentor_submissions_grade.view import grade_mentor_submission
from app.modules.mentor.api_57_mentor_submissions_feedback.models import (
    FeedbackMentorSubmissionEnvelope,
    FeedbackSubmissionRequest,
)
from app.modules.mentor.api_57_mentor_submissions_feedback.view import (
    save_mentor_submission_feedback,
)
from app.modules.mentor.api_58_mentor_support_requests.models import (
    GetMentorSupportRequestsEnvelope,
    MentorSupportRequestsQuery,
)
from app.modules.mentor.api_58_mentor_support_requests.view import (
    get_mentor_support_requests,
)
from app.modules.mentor.api_59_mentor_support_request_detail.models import (
    GetMentorSupportRequestEnvelope,
)
from app.modules.mentor.api_59_mentor_support_request_detail.view import (
    get_mentor_support_request,
)
from app.modules.mentor.api_60_mentor_support_reply.models import (
    ReplyMentorSupportRequestEnvelope,
    ReplyToMentorSupportRequest,
)
from app.modules.mentor.api_60_mentor_support_reply.view import (
    reply_to_mentor_support_request,
)
from app.modules.mentor.api_61_mentor_support_resolve.models import (
    ResolveMentorSupportRequestEnvelope,
)
from app.modules.mentor.api_61_mentor_support_resolve.view import (
    resolve_mentor_support_request,
)
from app.modules.mentor.api_62_mentor_course_students.models import (
    GetMentorCourseStudentsEnvelope,
)
from app.modules.mentor.api_62_mentor_course_students.view import (
    get_mentor_course_students,
)
from app.modules.mentor.api_63_mentor_notifications_create.models import (
    CreateNotificationEnvelope,
    CreateNotificationRequest,
)
from app.modules.mentor.api_63_mentor_notifications_create.view import (
    create_mentor_notifications,
)
from app.modules.mentor.api_64_mentor_notification_status.models import (
    GetMentorNotificationStatusEnvelope,
)
from app.modules.mentor.api_64_mentor_notification_status.view import (
    get_mentor_notification_status,
)
from app.modules.mentor.api_65_mentor_course_progress.models import (
    GetMentorCourseProgressEnvelope,
)
from app.modules.mentor.api_65_mentor_course_progress.view import (
    get_mentor_course_progress,
)
from app.modules.mentor.api_66_mentor_course_analytics.models import (
    GetMentorCourseAnalyticsEnvelope,
)
from app.modules.mentor.api_66_mentor_course_analytics.view import (
    get_mentor_course_analytics,
)
from app.modules.mentor.api_67_mentor_student_progress.models import (
    GetMentorStudentProgressEnvelope,
)
from app.modules.mentor.api_67_mentor_student_progress.view import (
    get_mentor_student_progress,
)
from app.modules.student.api_34_uploads.models import UploadPurpose
from app.modules.student.api_34_uploads.view import create_upload
from app.service.email.provider import (
    VerificationEmailProvider,
    get_verification_email_provider,
)
from app.service.object_storage.avatar import (
    AvatarStorageProvider,
    get_avatar_storage_provider,
)
from app.service.object_storage.upload import UploadStorageProvider, get_upload_storage_provider

router = APIRouter(
    prefix="/api/v1",
    tags=["api v1"],
)
db_dependency = Depends(get_db)
category_query_dependency = Depends()
verification_provider_dependency = Depends(get_verification_email_provider)
avatar_storage_provider_dependency = Depends(get_avatar_storage_provider)
upload_storage_provider_dependency = Depends(get_upload_storage_provider)
upload_file_part_dependency = File(...)
upload_purpose_form_dependency = Form(...)
upload_course_id_form_dependency = Form(
    default=None,
    json_schema_extra={"format": "int64"},
)


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


# API #08 courses_detail
@router.get(
    "/courses/{course_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
)
def course_detail(
    course_id: str,
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận course_id, Session và trace ID rồi chuyển cho get_course_detail. Route trả mã HTTP 200;
    kiểm tra tham số, truy vấn chi tiết khóa học và dựng response do view đảm nhiệm."""
    return get_course_detail(
        course_id_raw=course_id,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #09 courses_curriculum
@router.get(
    "/courses/{course_id}/curriculum",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
)
def course_curriculum(
    course_id: str,
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận course_id, Session và trace ID rồi chuyển cho get_course_curriculum. Route trả mã
    HTTP 200; kiểm tra tham số, kiểm tra khóa học, truy vấn bài học và dựng response do view đảm
    nhiệm."""
    return get_course_curriculum(
        course_id_raw=course_id,
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


# API #11 courses_resources
@router.get(
    "/courses/{course_id}/resources",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
)
def course_resources(
    course_id: int,
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    return get_course_resources_view(
        course_id=course_id,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #12 resources_detail
@router.get(
    "/resources/{resource_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
    openapi_extra={
        "parameters": [
            {
                "name": "resource_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            }
        ]
    },
)
def resource_detail(
    request: Request,
    resource_id: str = Path(include_in_schema=False),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận raw resource ID, Session và trace ID rồi chuyển luồng đọc resource cho API #12."""

    return get_resource_detail(
        resource_id=resource_id,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #13 users_me_avatar
@router.post(
    "/users/me/avatar",
    status_code=status.HTTP_201_CREATED,
    response_model=dict[str, Any],
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "required": ["image"],
                        "additionalProperties": False,
                        "properties": {
                            "image": {
                                "type": "string",
                                "format": "data-url",
                                "description": (
                                    "Data URL image/png, image/jpeg hoặc image/webp; "
                                    "tối đa 5 MiB sau giải mã."
                                ),
                            },
                        },
                    }
                }
            },
        }
    },
)
def upload_current_user_avatar(
    user_data: AvatarUploadRequest,
    request: Request,
    authorization: str | None = Header(default=None, alias="Authorization"),
    provider: AvatarStorageProvider = avatar_storage_provider_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận Data URL, Authorization và provider rồi chuyển luồng upload cho API #13."""

    return upload_avatar(
        authorization=authorization,
        user_data=user_data,
        provider=provider,
        trace_id=get_trace_id(request),
    )


# API #34 uploads
@router.post(
    "/uploads",
    status_code=status.HTTP_201_CREATED,
    response_model=dict[str, Any],
)
def upload_file(
    request: Request,
    file: UploadFile = upload_file_part_dependency,
    purpose: UploadPurpose = upload_purpose_form_dependency,
    course_id: int | None = upload_course_id_form_dependency,
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
    provider: UploadStorageProvider = upload_storage_provider_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận multipart file và chuyển xác thực, lưu object cùng metadata cho API #34."""

    return create_upload(
        authorization=authorization,
        file=file,
        purpose=purpose,
        course_id=course_id,
        db=db,
        provider=provider,
        trace_id=get_trace_id(request),
    )


# API #14 users_me_profile
@router.put(
    "/users/me/profile",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "required": ["full_name", "phone", "avatar_url"],
                        "properties": {
                            "full_name": {
                                "type": "string",
                                "minLength": 1,
                                "maxLength": 150,
                            },
                            "phone": {
                                "anyOf": [
                                    {"type": "string", "maxLength": 20},
                                    {"type": "null"},
                                ]
                            },
                            "avatar_url": {
                                "anyOf": [
                                    {"type": "string"},
                                    {"type": "null"},
                                ]
                            },
                        },
                    }
                }
            },
        }
    },
)
def update_current_profile(
    user_data: ProfileUpdateRequest,
    request: Request,
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận profile source-backed và chuyển xác thực, update cùng transaction cho API #14."""

    return update_profile(
        authorization=authorization,
        user_data=user_data,
        db=db,
        trace_id=get_trace_id(request),
    )



# API #15 courses_enrollment_status
@router.get(
    "/courses/{course_id}/enrollment-status",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
)
def course_enrollment_status(
    course_id: int,
    request: Request,
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    return get_enrollment_status_view(
        course_id=course_id,
        authorization=authorization,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #21 users_me_progress
@router.get(
    "/users/me/progress",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
)
def user_progress(
    request: Request,
    course_id: str | None = Query(default=None),
    aggregate: str | None = Query(default=None),
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận query, Header Authorization, Session và trace ID rồi chuyển cho get_user_progress."""
    return get_user_progress_view(
        authorization=authorization,
        course_id=course_id,
        aggregate=aggregate,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #22 lessons_access
@router.get(
    "/lessons/{lesson_id}/access",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
)
def lesson_access(
    lesson_id: int,
    request: Request,
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận lesson_id, Header Authorization, Session và trace ID rồi chuyển cho check_lesson_access."""
    return check_lesson_access_view(
        lesson_id=lesson_id,
        authorization=authorization,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #23 lessons_start
@router.post(
    "/lessons/{lesson_id}/start",
    status_code=status.HTTP_201_CREATED,
    response_model=dict[str, Any],
)
def lesson_start(
    lesson_id: int,
    request: Request,
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận lesson_id, Header Authorization, Session và trace ID rồi chuyển cho start_lesson."""
    return start_lesson_view(
        lesson_id=lesson_id,
        authorization=authorization,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #24 lessons_detail
@router.get(
    "/lessons/{lesson_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
)
def lesson_detail(
    lesson_id: int,
    request: Request,
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận lesson_id, Header Authorization, Session và trace ID rồi chuyển cho get_lesson_detail."""
    return get_lesson_detail_view(
        lesson_id=lesson_id,
        authorization=authorization,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #25 lessons_progress
@router.patch(
    "/lessons/{lesson_id}/progress",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
)
def lesson_progress(
    lesson_id: int,
    progress_data: LessonProgressUpdateRequest,
    request: Request,
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận lesson_id, body tiến độ, Header Authorization, Session và trace ID rồi chuyển cho update_lesson_progress."""
    return update_lesson_progress_view(
        lesson_id=lesson_id,
        progress_data=progress_data,
        authorization=authorization,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #46 mentor_courses
@router.get(
    "/mentor/courses",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
)
def mentor_courses(
    request: Request,
    authorization: str | None = Header(default=None, alias="Authorization"),
    status_filter: str | None = Query(
        default=None,
        alias="status",
        json_schema_extra={"enum": ["DRAFT", "PUBLISHED"]},
    ),
    page: int = Query(default=DEFAULT_PAGE, json_schema_extra={"minimum": 1}),
    size: int = Query(
        default=DEFAULT_SIZE,
        json_schema_extra={"minimum": 1, "maximum": 100},
    ),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận Bearer token, query fields, Session và trace ID rồi chuyển API #46 cho view kiểm tra
    Mentor, đọc các course trực tiếp sở hữu và dựng envelope phân trang."""
    mentor_query = MentorCourseQuery(status=status_filter, page=page, size=size)
    return get_mentor_courses(
        authorization=authorization,
        mentor_query=mentor_query,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #47 mentor_lectures_create
@router.post(
    "/mentor/courses/{course_id}/lectures",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateLectureEnvelope,
)
def create_mentor_lecture(
    lecture_request: CreateLectureRequest,
    request: Request,
    course_id: int = Path(..., json_schema_extra={"format": "int64"}),
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận lecture body, Bearer token, Session và trace ID rồi chuyển API #47 cho view.

    View xác thực Mentor, khóa course/assets theo owner và tạo lecture trong transaction.
    """
    return create_lecture(
        authorization=authorization,
        course_id=course_id,
        lecture_request=lecture_request,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #48 mentor_lecture_detail
@router.get(
    "/mentor/lectures/{lecture_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetLectureEnvelope,
)
def get_mentor_lecture(
    request: Request,
    lecture_id: str = Path(
        ...,
        json_schema_extra={"type": "integer", "format": "int64"},
    ),
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận raw path ID, Bearer token và Session rồi chuyển API #48 cho view.

    View kiểm tra signed int64, quyền Mentor và đọc Lecture cùng UploadAsset links.
    """
    return get_lecture(
        authorization=authorization,
        lecture_id_value=lecture_id,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #49 mentor_course_contents
@router.get(
    "/mentor/courses/{course_id}/content",
    status_code=status.HTTP_200_OK,
    response_model=GetCourseContentsEnvelope,
    response_model_exclude_none=True,
    openapi_extra={
        "parameters": [
            {
                "name": "course_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            }
        ]
    },
)
def get_mentor_course_contents(
    request: Request,
    course_id: str = Path(
        ...,
        json_schema_extra={"type": "integer", "format": "int64"},
    ),
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận course ID, Bearer token và Session rồi chuyển API #49 cho view đọc cây Content."""

    return get_course_contents(
        authorization=authorization,
        course_id_value=course_id,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #50 mentor_content_create
@router.post(
    "/mentor/content",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateContentEnvelope,
    response_model_exclude_none=True,
)
def create_mentor_content(
    content_request: CreateContentRequest,
    request: Request,
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận JSON Content, Bearer token và Session rồi chuyển API #50 cho lớp điều phối."""

    return create_content(
        authorization=authorization,
        content_request=content_request,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #51 mentor_content_update
@router.put(
    "/mentor/content/{content_id}",
    status_code=status.HTTP_200_OK,
    response_model=UpdateContentEnvelope,
    response_model_exclude_none=True,
    openapi_extra={
        "parameters": [
            {
                "name": "content_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            }
        ]
    },
)
def update_mentor_content(
    content_request: UpdateContentRequest,
    request: Request,
    content_id: str = Path(
        ...,
        json_schema_extra={"type": "integer", "format": "int64"},
    ),
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận Content replacement, path ID, Bearer token và Session rồi chuyển API #51 cho view."""

    return update_content(
        authorization=authorization,
        content_id_value=content_id,
        content_request=content_request,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #52 mentor_content_publish
@router.patch(
    "/mentor/content/{content_id}/publish",
    status_code=status.HTTP_200_OK,
    response_model=PublishContentEnvelope,
    response_model_exclude_none=True,
    openapi_extra={
        "parameters": [
            {
                "name": "content_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            }
        ]
    },
)
def publish_mentor_content(
    content_request: PublishContentRequest,
    request: Request,
    content_id: str = Path(
        ...,
        json_schema_extra={"type": "integer", "format": "int64"},
    ),
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận target state DERIVED, path, Bearer token và Session rồi chuyển API #52 cho view."""

    return publish_content(
        authorization=authorization,
        content_id_value=content_id,
        content_request=content_request,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #53 mentor_content_delete
@router.delete(
    "/mentor/content/{content_id}",
    status_code=status.HTTP_200_OK,
    response_model=DeleteContentEnvelope,
    response_model_exclude_none=True,
    openapi_extra={
        "parameters": [
            {
                "name": "content_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            }
        ]
    },
)
def delete_mentor_content(
    request: Request,
    content_id: str = Path(
        ...,
        json_schema_extra={"type": "integer", "format": "int64"},
    ),
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận Content ID và Bearer token rồi chuyển API #53 cho lớp điều phối."""

    return delete_content(
        authorization=authorization,
        content_id_value=content_id,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #54 mentor_submissions_list
@router.get(
    "/mentor/submissions",
    status_code=status.HTTP_200_OK,
    response_model=GetMentorSubmissionsEnvelope,
    response_model_exclude_none=True,
)
def get_mentor_submissions_list(
    request: Request,
    course_id: int | None = Query(
        default=None,
        ge=1,
        le=2**63 - 1,
        json_schema_extra={"format": "int64"},
    ),
    status_filter: str | None = Query(default=None, alias="status"),
    page: int = Query(
        default=DEFAULT_PAGE,
        ge=1,
        le=2**31 - 1,
        json_schema_extra={"format": "int32"},
    ),
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận bộ lọc, Bearer token và Session rồi chuyển API #54 cho lớp điều phối Mentor."""

    query = MentorSubmissionsQuery(
        course_id=course_id,
        status=status_filter,
        page=page,
    )
    return get_mentor_submissions(
        authorization=authorization,
        submission_query=query,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #55 mentor_submission_detail
@router.get(
    "/mentor/submissions/{submission_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetMentorSubmissionEnvelope,
    response_model_exclude_none=True,
)
def get_mentor_submission_detail(
    request: Request,
    submission_id: str = Path(
        ...,
        json_schema_extra={"type": "integer", "format": "int64"},
    ),
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận raw Submission ID, Bearer token và Session rồi chuyển API #55 cho view."""

    return get_mentor_submission(
        authorization=authorization,
        submission_id_value=submission_id,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #56 mentor_submissions_grade
@router.post(
    "/mentor/submissions/{submission_id}/grade",
    status_code=status.HTTP_200_OK,
    response_model=GradeMentorSubmissionEnvelope,
    response_model_exclude_none=True,
)
def post_mentor_submission_grade(
    request: Request,
    submission_id: str = Path(
        ...,
        json_schema_extra={"type": "integer", "format": "int64"},
    ),
    grade_request: GradeSubmissionRequest = ...,
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận Submission ID, body chấm điểm, Bearer token và Session cho API #56."""

    return grade_mentor_submission(
        authorization=authorization,
        submission_id_value=submission_id,
        grade_request=grade_request,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #57 mentor_submissions_feedback
@router.post(
    "/mentor/submissions/{submission_id}/feedback",
    status_code=status.HTTP_200_OK,
    response_model=FeedbackMentorSubmissionEnvelope,
    response_model_exclude_none=True,
)
def post_mentor_submission_feedback(
    request: Request,
    submission_id: str = Path(
        ...,
        json_schema_extra={"type": "integer", "format": "int64"},
    ),
    feedback_request: FeedbackSubmissionRequest = ...,
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận Submission ID, feedback body, Bearer token và Session cho API #57."""

    return save_mentor_submission_feedback(
        authorization=authorization,
        submission_id_value=submission_id,
        feedback_request=feedback_request,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #58 mentor_support_requests
@router.get(
    "/mentor/support/requests",
    status_code=status.HTTP_200_OK,
    response_model=GetMentorSupportRequestsEnvelope,
    response_model_exclude_none=True,
)
def get_mentor_support_requests_list(
    request: Request,
    course_id: int | None = Query(
        default=None,
        ge=1,
        le=2**63 - 1,
        json_schema_extra={"format": "int64"},
    ),
    status_filter: str | None = Query(default=None, alias="status"),
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận bộ lọc, Bearer token và Session rồi chuyển API #58 cho lớp điều phối Mentor."""

    support_query = MentorSupportRequestsQuery(
        course_id=course_id,
        status=status_filter,
    )
    return get_mentor_support_requests(
        authorization=authorization,
        support_query=support_query,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #59 mentor_support_request_detail
@router.get(
    "/mentor/support/{request_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetMentorSupportRequestEnvelope,
    response_model_exclude_none=True,
)
def get_mentor_support_request_detail(
    request: Request,
    request_id: str = Path(
        ...,
        json_schema_extra={"type": "integer", "format": "int64"},
    ),
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận support request ID, Bearer token và Session rồi chuyển API #59 cho view."""

    return get_mentor_support_request(
        authorization=authorization,
        request_id_value=request_id,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #60 mentor_support_reply
@router.post(
    "/mentor/support/{request_id}/reply",
    status_code=status.HTTP_200_OK,
    response_model=ReplyMentorSupportRequestEnvelope,
    response_model_exclude_none=True,
)
def post_mentor_support_reply(
    request: Request,
    reply_request: ReplyToMentorSupportRequest,
    request_id: str = Path(
        ...,
        json_schema_extra={"type": "integer", "format": "int64"},
    ),
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận SupportRequest ID, message, refs và chuyển API #60 cho view."""

    return reply_to_mentor_support_request(
        authorization=authorization,
        request_id_value=request_id,
        reply_request=reply_request,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #61 mentor_support_resolve
@router.patch(
    "/mentor/support/{request_id}/resolve",
    status_code=status.HTTP_200_OK,
    response_model=ResolveMentorSupportRequestEnvelope,
    response_model_exclude_none=True,
)
def patch_mentor_support_resolve(
    request: Request,
    request_id: str = Path(
        ...,
        json_schema_extra={"type": "integer", "format": "int64"},
    ),
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận SupportRequest ID, Bearer token và chuyển API #61 cho view."""

    return resolve_mentor_support_request(
        authorization=authorization,
        request_id_value=request_id,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #62 mentor_course_students
@router.get(
    "/mentor/courses/{course_id}/students",
    status_code=status.HTTP_200_OK,
    response_model=GetMentorCourseStudentsEnvelope,
    response_model_exclude_none=True,
    openapi_extra={
        "parameters": [
            {
                "name": "course_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            }
        ]
    },
)
def get_mentor_course_students_list(
    request: Request,
    course_id: str = Path(
        ...,
        json_schema_extra={"type": "integer", "format": "int64"},
    ),
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận course ID, Bearer token và Session rồi chuyển API #62 cho view."""

    return get_mentor_course_students(
        authorization=authorization,
        course_id_value=course_id,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #65 mentor_course_progress
@router.get(
    "/mentor/courses/{course_id}/progress",
    status_code=status.HTTP_200_OK,
    response_model=GetMentorCourseProgressEnvelope,
    response_model_exclude_none=True,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "course_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def get_mentor_course_progress_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw course ID, Bearer header và Session cho lớp điều phối API #65."""

    return get_mentor_course_progress(
        authorization=request.headers.get("Authorization"),
        course_id_value=str(request.path_params.get("course_id", "")),
        db=db,
        trace_id=get_trace_id(request),
    )


# API #66 mentor_course_analytics
@router.get(
    "/mentor/courses/{course_id}/analytics",
    status_code=status.HTTP_200_OK,
    response_model=GetMentorCourseAnalyticsEnvelope,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "course_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def get_mentor_course_analytics_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw course ID, Bearer header và Session cho lớp điều phối API #66."""

    return get_mentor_course_analytics(
        authorization=request.headers.get("Authorization"),
        course_id_value=str(request.path_params.get("course_id", "")),
        db=db,
        trace_id=get_trace_id(request),
    )


# API #67 mentor_student_progress
@router.get(
    "/mentor/courses/{course_id}/students/{student_id}/progress",
    status_code=status.HTTP_200_OK,
    response_model=GetMentorStudentProgressEnvelope,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "course_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "student_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def get_mentor_student_progress_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw path IDs, Bearer header và Session cho lớp điều phối API #67."""

    return get_mentor_student_progress(
        authorization=request.headers.get("Authorization"),
        course_id_value=str(request.path_params.get("course_id", "")),
        student_id_value=str(request.path_params.get("student_id", "")),
        db=db,
        trace_id=get_trace_id(request),
    )


# API #63 mentor_notifications_create
@router.post(
    "/mentor/notifications",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=CreateNotificationEnvelope,
    response_model_exclude_none=True,
)
def create_mentor_notifications_endpoint(
    notification_request: CreateNotificationRequest,
    request: Request,
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận body thông báo, Bearer token và Session rồi chuyển API #63 cho view."""

    return create_mentor_notifications(
        authorization=authorization,
        request_data=notification_request,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #64 mentor_notification_status
@router.get(
    "/mentor/notifications/{notification_id}/status",
    status_code=status.HTTP_200_OK,
    response_model=GetMentorNotificationStatusEnvelope,
    response_model_exclude_none=True,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "Authorization",
                "in": "header",
                "required": False,
                "schema": {"type": "string"},
            },
            {
                "name": "notification_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            },
        ]
    },
)
def get_mentor_notification_status_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận raw path/header từ Request và chuyển API #64 cho view."""

    return get_mentor_notification_status(
        authorization=request.headers.get("Authorization"),
        notification_id_value=request.path_params["notification_id"],
        db=db,
        trace_id=get_trace_id(request),
    )


# API #68 admin_users_list
@router.get(
    "/admin/users",
    status_code=status.HTTP_200_OK,
    response_model=GetAdminUsersEnvelope,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        422: {"description": "DESIGN_VALIDATION_ERROR"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "role",
                "in": "query",
                "required": False,
                "schema": {"type": "string"},
            },
            {
                "name": "status",
                "in": "query",
                "required": False,
                "schema": {"type": "string"},
            },
            {
                "name": "keyword",
                "in": "query",
                "required": False,
                "schema": {"type": "string"},
            },
            {
                "name": "page",
                "in": "query",
                "required": False,
                "schema": {
                    "type": "integer",
                    "format": "int32",
                    "minimum": 1,
                    "maximum": 2147483647,
                    "default": 1,
                },
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def get_admin_users_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw query/header, Session và trace ID cho lớp điều phối API #68."""

    return get_admin_users(
        authorization=request.headers.get("Authorization"),
        role=request.query_params.get("role"),
        status=request.query_params.get("status"),
        keyword=request.query_params.get("keyword"),
        page_value=request.query_params.get("page"),
        db=db,
        trace_id=get_trace_id(request),
    )


# API #69 admin_user_detail
@router.get(
    "/admin/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetAdminUserEnvelope,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "user_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def get_admin_user_detail_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw path/header, Session và trace ID cho lớp điều phối API #69."""

    return get_admin_user(
        authorization=request.headers.get("Authorization"),
        user_id_value=request.path_params["user_id"],
        db=db,
        trace_id=get_trace_id(request),
    )


# API #70 admin_user_update
@router.put(
    "/admin/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UpdateAdminUserEnvelope,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        422: {"description": "DESIGN_VALIDATION_ERROR"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "user_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def update_admin_user_endpoint(
    request: Request,
    user_data: AdminUserUpdateRequest,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận raw path/header cùng JSON body rồi chuyển API #70 cho view."""

    return update_admin_user(
        authorization=request.headers.get("Authorization"),
        user_id_value=request.path_params["user_id"],
        user_data=user_data,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #71 admin_user_status
@router.patch(
    "/admin/users/{user_id}/status",
    status_code=status.HTTP_200_OK,
    response_model=UpdateAdminUserStatusEnvelope,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        422: {"description": "DESIGN_VALIDATION_ERROR"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "user_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def update_admin_user_status_endpoint(
    request: Request,
    user_data: AdminUserStatusRequest,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận raw path/header cùng status body rồi chuyển API #71 cho view."""

    return update_admin_user_status(
        authorization=request.headers.get("Authorization"),
        user_id_value=request.path_params["user_id"],
        user_data=user_data,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #72 admin_user_delete
@router.delete(
    "/admin/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=DeleteAdminUserEnvelope,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        422: {"description": "DESIGN_VALIDATION_ERROR"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "user_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def delete_admin_user_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw path/header, Session và trace ID cho lớp điều phối API #72."""

    return delete_admin_user(
        authorization=request.headers.get("Authorization"),
        user_id_value=request.path_params["user_id"],
        db=db,
        trace_id=get_trace_id(request),
    )


# API #73 admin_courses_list
@router.get(
    "/admin/courses",
    status_code=status.HTTP_200_OK,
    response_model=GetAdminCoursesEnvelope,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        422: {"description": "DESIGN_VALIDATION_ERROR"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "status",
                "in": "query",
                "required": False,
                "schema": {"type": "string"},
            },
            {
                "name": "mentor",
                "in": "query",
                "required": False,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "category",
                "in": "query",
                "required": False,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "page",
                "in": "query",
                "required": False,
                "schema": {
                    "type": "integer",
                    "format": "int32",
                    "minimum": 1,
                    "maximum": 2147483647,
                    "default": 1,
                },
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def get_admin_courses_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw query/header, Session và trace ID cho lớp điều phối API #73."""

    return get_admin_courses(
        authorization=request.headers.get("Authorization"),
        status=request.query_params.get("status"),
        mentor_value=request.query_params.get("mentor"),
        category_value=request.query_params.get("category"),
        page_value=request.query_params.get("page"),
        db=db,
        trace_id=get_trace_id(request),
    )


# API #74 admin_course_detail
@router.get(
    "/admin/courses/{course_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetAdminCourseDetailEnvelope,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "course_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def get_admin_course_detail_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw path/header, Session và trace ID cho lớp điều phối API #74."""

    return get_admin_course_detail(
        authorization=request.headers.get("Authorization"),
        course_id_value=request.path_params["course_id"],
        db=db,
        trace_id=get_trace_id(request),
    )


# API #75 admin_course_update
@router.put(
    "/admin/courses/{course_id}",
    status_code=status.HTTP_200_OK,
    response_model=UpdateAdminCourseEnvelope,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        422: {"description": "DESIGN_VALIDATION_ERROR"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "course_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def update_admin_course_endpoint(
    request: Request,
    course_data: AdminCourseUpdateRequest,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận raw path/header và body rồi chuyển API #75 cho lớp điều phối."""

    return update_admin_course(
        authorization=request.headers.get("Authorization"),
        course_id_value=request.path_params["course_id"],
        course_data=course_data,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #76 admin_course_status
@router.patch(
    "/admin/courses/{course_id}/status",
    status_code=status.HTTP_200_OK,
    response_model=UpdateAdminCourseStatusEnvelope,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        422: {"description": "DESIGN_VALIDATION_ERROR"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "course_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def update_admin_course_status_endpoint(
    request: Request,
    course_data: AdminCourseStatusRequest,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Nhận raw path/header cùng target status rồi chuyển API #76 cho view."""

    return update_admin_course_status(
        authorization=request.headers.get("Authorization"),
        course_id_value=request.path_params["course_id"],
        course_data=course_data,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #77 admin_course_delete
@router.delete(
    "/admin/courses/{course_id}",
    status_code=status.HTTP_200_OK,
    response_model=DeleteAdminCourseEnvelope,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        422: {"description": "DESIGN_VALIDATION_ERROR"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "course_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def delete_admin_course_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw path/header, Session và trace ID cho lớp điều phối API #77."""

    return delete_admin_course(
        authorization=request.headers.get("Authorization"),
        course_id_value=request.path_params["course_id"],
        db=db,
        trace_id=get_trace_id(request),
    )


# API #78 admin_content_pending
@router.get(
    "/admin/content/pending",
    status_code=status.HTTP_200_OK,
    response_model=GetAdminPendingContentsEnvelope,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        422: {"description": "DESIGN_VALIDATION_ERROR — DERIVED query validation"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "type",
                "in": "query",
                "required": False,
                "schema": {"type": "string"},
            },
            {
                "name": "course",
                "in": "query",
                "required": False,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "page",
                "in": "query",
                "required": False,
                "schema": {
                    "type": "integer",
                    "format": "int32",
                    "minimum": 1,
                    "maximum": 2147483647,
                    "default": 1,
                },
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def get_admin_pending_contents_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw query/header, Session và trace ID cho lớp điều phối API #78."""

    return get_admin_pending_contents(
        authorization=request.headers.get("Authorization"),
        content_type_value=request.query_params.get("type"),
        course_value=request.query_params.get("course"),
        page_value=request.query_params.get("page"),
        db=db,
        trace_id=get_trace_id(request),
    )


# API #79 admin_content_detail
@router.get(
    "/admin/content/{content_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetAdminContentEnvelope,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "content_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def get_admin_content_detail_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw path/header, Session và trace ID cho lớp điều phối API #79."""

    return get_admin_content(
        authorization=request.headers.get("Authorization"),
        content_id_value=request.path_params["content_id"],
        db=db,
        trace_id=get_trace_id(request),
    )


# API #80 admin_content_approve
@router.patch(
    "/admin/content/{content_id}/approve",
    status_code=status.HTTP_200_OK,
    response_model=ApproveAdminContentEnvelope,
    response_model_exclude_none=True,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        422: {"description": "DESIGN_VALIDATION_ERROR"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "content_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def approve_admin_content_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw path/header, Session và trace ID cho lớp điều phối API #80."""

    return approve_admin_content(
        authorization=request.headers.get("Authorization"),
        content_id_value=request.path_params["content_id"],
        db=db,
        trace_id=get_trace_id(request),
    )


# API #81 admin_content_reject
@router.patch(
    "/admin/content/{content_id}/reject",
    status_code=status.HTTP_200_OK,
    response_model=RejectAdminContentEnvelope,
    response_model_exclude_none=True,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        422: {"description": "DESIGN_VALIDATION_ERROR"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "content_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def reject_admin_content_endpoint(
    request: Request,
    content_request: RejectAdminContentRequest,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw path/header, body, Session và trace ID cho API #81."""

    return reject_admin_content(
        authorization=request.headers.get("Authorization"),
        content_id_value=request.path_params["content_id"],
        content_request=content_request,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #82 admin_lessons_list
@router.get(
    "/admin/lessons",
    status_code=status.HTTP_200_OK,
    response_model=GetAdminLessonsEnvelope,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        422: {"description": "DESIGN_VALIDATION_ERROR — DERIVED query handling"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "course",
                "in": "query",
                "required": False,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "status",
                "in": "query",
                "required": False,
                "schema": {"type": "string"},
            },
            {
                "name": "type",
                "in": "query",
                "required": False,
                "schema": {"type": "string"},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def get_admin_lessons_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw query/header, Session và trace ID cho lớp điều phối API #82."""

    return get_admin_lessons(
        authorization=request.headers.get("Authorization"),
        course_value=request.query_params.get("course"),
        status=request.query_params.get("status"),
        type_value=request.query_params.get("type"),
        db=db,
        trace_id=get_trace_id(request),
    )


# API #83 admin_lesson_detail
@router.get(
    "/admin/lessons/{lesson_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetAdminLessonEnvelope,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "lesson_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def get_admin_lesson_detail_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw path/header, Session và trace ID cho lớp điều phối API #83."""

    return get_admin_lesson_detail(
        authorization=request.headers.get("Authorization"),
        lesson_id_value=request.path_params["lesson_id"],
        db=db,
        trace_id=get_trace_id(request),
    )


# API #84 admin_lesson_update
@router.put(
    "/admin/lessons/{lesson_id}",
    status_code=status.HTTP_200_OK,
    response_model=UpdateAdminLessonEnvelope,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        422: {"description": "DESIGN_VALIDATION_ERROR"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "lesson_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def update_admin_lesson_endpoint(
    request: Request,
    lesson_data: AdminLessonUpdateRequest,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw path/header, body, Session và trace ID cho API #84."""

    return update_admin_lesson(
        authorization=request.headers.get("Authorization"),
        lesson_id_value=request.path_params["lesson_id"],
        lesson_data=lesson_data,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #86 admin_lesson_delete
@router.delete(
    "/admin/lessons/{lesson_id}",
    status_code=status.HTTP_200_OK,
    response_model=DeleteAdminLessonEnvelope,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        422: {"description": "DESIGN_VALIDATION_ERROR"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "lesson_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def delete_admin_lesson_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw path/header, Session và trace ID cho API #86."""

    return delete_admin_lesson(
        authorization=request.headers.get("Authorization"),
        lesson_id_value=request.path_params["lesson_id"],
        db=db,
        trace_id=get_trace_id(request),
    )


# API #87 admin_quizzes_list
@router.get(
    "/admin/quizzes",
    status_code=status.HTTP_200_OK,
    response_model=GetAdminQuizzesEnvelope,
    response_model_exclude_none=True,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        422: {"description": "DESIGN_VALIDATION_ERROR — DERIVED query handling"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "course",
                "in": "query",
                "required": False,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "status",
                "in": "query",
                "required": False,
                "schema": {"type": "string"},
            },
            {
                "name": "page",
                "in": "query",
                "required": False,
                "schema": {
                    "type": "integer",
                    "format": "int32",
                    "minimum": 1,
                    "maximum": 2147483647,
                    "default": 1,
                },
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def get_admin_quizzes_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw query/header, Session và trace ID cho lớp điều phối API #87."""

    return get_admin_quizzes(
        authorization=request.headers.get("Authorization"),
        course_value=request.query_params.get("course"),
        status_value=request.query_params.get("status"),
        page_value=request.query_params.get("page"),
        db=db,
        trace_id=get_trace_id(request),
    )


# API #88 admin_quizzes_create
@router.post(
    "/admin/quizzes",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateAdminQuizEnvelope,
    response_model_exclude_none=True,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        422: {"description": "DESIGN_VALIDATION_ERROR"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "required": ["config", "questions"],
                        "additionalProperties": False,
                        "properties": {
                            "config": {"type": "string"},
                            "questions": {"type": "string"},
                        },
                    }
                }
            },
        },
    },
)
async def create_admin_quiz_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw body/header qua API #88 mà chưa parse body trước shared ADMIN guard."""

    # Chỉ lấy raw bytes; view sẽ xác thực token trước khi parse JSON hoặc truy vấn DB.
    raw_body = await request.body()
    return await run_in_threadpool(
        create_admin_quiz,
        authorization=request.headers.get("Authorization"),
        raw_body=raw_body,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #89 admin_quizzes_update
@router.put(
    "/admin/quizzes/{quiz_id}",
    status_code=status.HTTP_200_OK,
    response_model=UpdateAdminQuizEnvelope,
    response_model_exclude_none=True,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        422: {"description": "DESIGN_VALIDATION_ERROR — body/path/history proposal"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "quiz_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "required": ["config", "questions"],
                        "additionalProperties": False,
                        "properties": {
                            "config": {"type": "string"},
                            "questions": {"type": "string"},
                        },
                    }
                }
            },
        },
    },
)
async def update_admin_quiz_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw path/body/header sang view sau khi giữ nguyên thứ tự auth trước parse."""

    # Chỉ đọc bytes; validator của view xác thực ADMIN trước khi decode JSON.
    raw_body = await request.body()
    return await run_in_threadpool(
        update_admin_quiz,
        authorization=request.headers.get("Authorization"),
        quiz_id_value=request.path_params["quiz_id"],
        raw_body=raw_body,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #90 admin_quizzes_delete
@router.delete(
    "/admin/quizzes/{quiz_id}",
    status_code=status.HTTP_200_OK,
    response_model=DeleteAdminQuizEnvelope,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        422: {"description": "DESIGN_VALIDATION_ERROR — quiz_id"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "quiz_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64", "minimum": 1},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ]
    },
)
async def delete_admin_quiz_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw path/header qua API #90 để ADMIN chạy trước path parsing."""

    # Route không khai báo hoặc đọc body/query vì catalog #90 chỉ nhận Quiz ID.
    return await run_in_threadpool(
        delete_admin_quiz,
        authorization=request.headers.get("Authorization"),
        quiz_id_value=request.path_params["quiz_id"],
        db=db,
        trace_id=get_trace_id(request),
    )


# API #91 admin_quizzes_statistics
@router.get(
    "/admin/quizzes/{quiz_id}/statistics",
    status_code=status.HTTP_200_OK,
    response_model=GetAdminQuizStatisticsEnvelope,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "quiz_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64", "minimum": 1},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ]
    },
)
async def get_admin_quiz_statistics_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw path và Authorization qua API #91 để guard chạy trước parse."""

    # Route chỉ nhận quiz_id; auth và parse được điều phối trong view.
    return await run_in_threadpool(
        get_admin_quiz_statistics,
        authorization=request.headers.get("Authorization"),
        quiz_id_value=request.path_params["quiz_id"],
        db=db,
        trace_id=get_trace_id(request),
    )


# API #92 admin_notifications_list
@router.get(
    "/admin/notifications",
    status_code=status.HTTP_200_OK,
    response_model=GetAdminNotificationsEnvelope,
    response_model_exclude_none=True,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        422: {"description": "DESIGN_VALIDATION_ERROR — DERIVED page validation"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
        503: {"description": "DESIGN_DEPENDENCY_UNAVAILABLE"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "status",
                "in": "query",
                "required": False,
                "schema": {"type": "string"},
            },
            {
                "name": "channel",
                "in": "query",
                "required": False,
                "schema": {"type": "string"},
            },
            {
                "name": "page",
                "in": "query",
                "required": False,
                "schema": {
                    "type": "integer",
                    "format": "int32",
                    "minimum": 1,
                    "maximum": 2147483647,
                    "default": 1,
                },
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ]
    },
)
def get_admin_notifications_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw query/header, Session và trace ID cho lớp điều phối API #92."""

    # Route giữ raw query để view xác thực ADMIN trước khi parse page.
    return get_admin_notifications(
        authorization=request.headers.get("Authorization"),
        status_value=request.query_params.get("status"),
        channel_value=request.query_params.get("channel"),
        page_value=request.query_params.get("page"),
        db=db,
        trace_id=get_trace_id(request),
    )


# API #93 admin_notifications_create
@router.post(
    "/admin/notifications",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=CreateAdminNotificationEnvelope,
    response_model_exclude_none=True,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        422: {"description": "DESIGN_VALIDATION_ERROR — recipient/channel fallback"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
        503: {"description": "DESIGN_DEPENDENCY_UNAVAILABLE"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "required": ["title", "content", "channels"],
                        "additionalProperties": False,
                        "properties": {
                            "recipients": {
                                "type": "array",
                                "items": {
                                    "type": "integer",
                                    "format": "int64",
                                    "minimum": 1,
                                },
                            },
                            "segment": {
                                "description": (
                                    "AudienceSegment chưa có enum/predicate; runtime trả 422."
                                ),
                            },
                            "title": {"type": "string", "maxLength": 200},
                            "content": {"type": "string"},
                            "channels": {
                                "type": "array",
                                "items": {"type": "string", "enum": ["PUSH", "EMAIL"]},
                            },
                        },
                    }
                }
            },
        },
    },
)
async def create_admin_notification_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw body/header cho API #93 để shared ADMIN guard chạy trước parsing."""

    # Giữ nguyên bytes tới view để request body sai không lấn át lỗi auth/role.
    raw_body = await request.body()
    return await run_in_threadpool(
        create_admin_notification,
        authorization=request.headers.get("Authorization"),
        raw_body=raw_body,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #94 admin_notifications_update
@router.put(
    "/admin/notifications/{notification_id}",
    status_code=status.HTTP_200_OK,
    response_model=UpdateAdminNotificationEnvelope,
    response_model_exclude_none=True,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        422: {"description": "DESIGN_VALIDATION_ERROR"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "notification_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64", "minimum": 1},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "required": ["title", "content"],
                        "additionalProperties": False,
                        "properties": {
                            "title": {"type": "string", "maxLength": 200},
                            "content": {"type": "string"},
                        },
                    }
                }
            },
        },
    },
)
async def update_admin_notification_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw path/body/header cho API #94 để shared ADMIN guard chạy trước parse."""

    raw_body = await request.body()
    return await run_in_threadpool(
        update_admin_notification,
        authorization=request.headers.get("Authorization"),
        notification_id_value=request.path_params["notification_id"],
        raw_body=raw_body,
        db=db,
        trace_id=get_trace_id(request),
    )


# API #95 admin_notifications_delete
@router.delete(
    "/admin/notifications/{notification_id}",
    status_code=status.HTTP_200_OK,
    response_model=DeleteAdminNotificationEnvelope,
    response_model_exclude_none=True,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        422: {"description": "DESIGN_VALIDATION_ERROR"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "notification_id",
                "in": "path",
                "required": True,
                "schema": {
                    "type": "integer",
                    "format": "int64",
                    "minimum": 1,
                    "maximum": 9223372036854775807,
                },
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
async def delete_admin_notification_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw path/header cho API #95 để shared ADMIN guard chạy trước parse."""

    return await run_in_threadpool(
        delete_admin_notification,
        authorization=request.headers.get("Authorization"),
        notification_id_value=request.path_params["notification_id"],
        db=db,
        trace_id=get_trace_id(request),
    )


# API #96 admin_notifications_status
@router.get(
    "/admin/notifications/{notification_id}/status",
    status_code=status.HTTP_200_OK,
    response_model=GetAdminNotificationStatusEnvelope,
    response_model_exclude_none=True,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "notification_id",
                "in": "path",
                "required": True,
                "schema": {
                    "type": "integer",
                    "format": "int64",
                    "minimum": 1,
                    "maximum": 9223372036854775807,
                },
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
async def get_admin_notification_status_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw path/header cho API #96 để ADMIN guard chạy trước parse."""

    return await run_in_threadpool(
        get_admin_notification_status,
        authorization=request.headers.get("Authorization"),
        notification_id_value=request.path_params["notification_id"],
        db=db,
        trace_id=get_trace_id(request),
    )


# API #97 admin_discussions_reported
@router.get(
    "/admin/discussions/reported",
    status_code=status.HTTP_200_OK,
    response_model=GetAdminReportedDiscussionsEnvelope,
    response_model_exclude_none=True,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        422: {"description": "DESIGN_VALIDATION_ERROR — DERIVED page validation"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "reason",
                "in": "query",
                "required": False,
                "schema": {"type": "string"},
            },
            {
                "name": "severity",
                "in": "query",
                "required": False,
                "schema": {"type": "string"},
            },
            {
                "name": "page",
                "in": "query",
                "required": False,
                "schema": {
                    "type": "integer",
                    "format": "int32",
                    "minimum": 1,
                    "maximum": 2147483647,
                    "default": 1,
                },
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def get_admin_reported_discussions_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw query/header cho API #97 để ADMIN guard chạy trước parse."""

    # Route giữ nguyên chuỗi query để view áp dụng exact-match filter.
    return get_admin_reported_discussions(
        authorization=request.headers.get("Authorization"),
        reason_value=request.query_params.get("reason"),
        severity_value=request.query_params.get("severity"),
        page_value=request.query_params.get("page"),
        db=db,
        trace_id=get_trace_id(request),
    )


# API #98 admin_discussions_detail
@router.get(
    "/admin/discussions/{discussion_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetAdminDiscussionDetailEnvelope,
    response_model_exclude_none=True,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "discussion_id",
                "in": "path",
                "required": True,
                "schema": {
                    "type": "integer",
                    "format": "int64",
                    "minimum": 1,
                    "maximum": 9223372036854775807,
                },
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
async def get_admin_discussion_detail_endpoint(
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw path/header cho API #98 để ADMIN guard chạy trước parse."""

    return await run_in_threadpool(
        get_admin_discussion_detail,
        authorization=request.headers.get("Authorization"),
        discussion_id_value=request.path_params["discussion_id"],
        db=db,
        trace_id=get_trace_id(request),
    )


# API #85 admin_lesson_status
@router.patch(
    "/admin/lessons/{lesson_id}/status",
    status_code=status.HTTP_200_OK,
    response_model=UpdateAdminLessonStatusEnvelope,
    responses={
        401: {"description": "DESIGN_AUTHENTICATION_REQUIRED"},
        403: {"description": "DESIGN_ACCESS_DENIED"},
        404: {"description": "DESIGN_RESOURCE_NOT_FOUND"},
        422: {"description": "DESIGN_VALIDATION_ERROR"},
        500: {"description": "DESIGN_INTERNAL_ERROR"},
    },
    openapi_extra={
        "parameters": [
            {
                "name": "lesson_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer", "format": "int64"},
            },
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
)
def update_admin_lesson_status_endpoint(
    request: Request,
    lesson_data: AdminLessonStatusRequest,
    db: Session = db_dependency,
) -> dict[str, Any] | JSONResponse:
    """Chuyển raw path/header, body, Session và trace ID cho API #85."""

    return update_admin_lesson_status(
        authorization=request.headers.get("Authorization"),
        lesson_id_value=request.path_params["lesson_id"],
        lesson_data=lesson_data,
        db=db,
        trace_id=get_trace_id(request),
    )
