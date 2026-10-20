---
title: "Overview"
order: 2
dd_id: "28"
api_name: "Lấy metadata/câu hỏi được phép hiển thị"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 28 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | GET |
| Endpoint | /api/v1/quizzes/{quiz_id} |
| Purpose | Đọc metadata quiz và question set mà Student được phép xem trong AC-16. |
| Consumer/Actor | Student |
| Authentication | Bearer JWT theo API catalog. |
| Authorization | Catalog yêu cầu role Student; AC-16 yêu cầu Student có quyền làm quiz và quiz đang mở. Predicate thực tế chưa được đặc tả. |
| Basis | DIRECT — API catalog, AC-16 index/activity diagram; candidate persistence mapping từ DB design. |
| Status | Draft — Needs Confirmation |
| Transaction | N/A — GET chỉ đọc theo contract. |
| Side effects | N/A — không có mutation hoặc external side effect được mô tả. |

## Sources

- [API catalog](../../../../../docs/lists/list_api.md) — method, endpoint, Student Bearer, path, response schema và error codes của API #28.
- [AC API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-16 yêu cầu Student có quyền làm quiz, quiz đang mở; postcondition là attempt được nộp và kết quả/trạng thái chấm được trả về.
- [AC-16 activity diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — API #28 đọc Quiz, rule và question set; nhánh tiếp theo ghi “Được phép làm bài?” và “Hết lượt/hết hạn → 403/409”.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md), [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) và [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — candidate tables, fields và relations; đều là design evidence.
- [API Guidelines](../../../../../contracts/api-guidelines/README.md) — envelope fields, error data=null và safe field-level details.
- [Current router](../../../app/api/v1.py), [Study modules](../../../app/modules/) và [Study tests](../../../tests/) — trạng thái wiring hiện tại.

## Tables read

- quizzes — candidate source cho Quiz metadata và quiz status; query/runtime chưa được xác minh.
- quiz_questions — candidate source cho question ID, text và thứ tự trong quiz.
- quiz_choices — candidate source cho choice ID/text; không trả cột đáp án đúng cho Student.
- quiz_attempts — có thể liên quan nếu eligibility dựa trên attempt count; API #28 query không được nguồn chốt nên chưa coi là bảng đọc của API.

## Tables write

- N/A — API catalog khai báo GET; không có mutation.

## Mục chú ý

- API catalog là APPROVED_DESIGN_CONTRACT, chưa runtime-verified. Contract khai báo HTTP 200 DESIGN_RESOURCE_RETRIEVED, 401 DESIGN_AUTHENTICATION_REQUIRED, 403 DESIGN_ACCESS_DENIED, 404 DESIGN_RESOURCE_NOT_FOUND và 500 DESIGN_INTERNAL_ERROR.
- Logical Quiz gồm id, course_id, title, duration_minutes?, passing_score và questions. QuizQuestion gồm id, text, type và choices; catalog dùng QuizChoice[] nhưng không định nghĩa schema QuizChoice.
- AC-16 activity diagram đặt bước đọc Quiz/rule/question set trước bước kiểm tra quyền làm bài; nhánh sơ đồ nêu 403/409 cho trường hợp không đủ điều kiện/hết lượt/hết hạn. API #28 catalog không liệt kê 409.
- DB design có quizzes.name, description, passing_score, time_limit_minutes và status; quiz_questions có question_text, sort_order và score; quiz_choices có choice_text và is_correct. Các field không có trong logical Quiz/QuizQuestion chưa được thêm vào response.
- Không trả quiz_choices.is_correct trong response Student theo yêu cầu hiện tại. Đây là thông tin đáp án, không phải field được phép suy ra từ QuizChoice[].
- DB_UNICA_TABLES.md mô tả các foreign key quiz/course/question là bắt buộc; checked-in DDL không đặt NOT NULL cho các foreign key này. Live schema chưa được xác minh.
- Source scan hiện tại không tìm thấy route, module hoặc test quiz trong Study Server.

## Assumptions

- Giữ nguyên contract API #28 trong catalog; DD không sửa API catalog, OpenAPI hoặc runtime.
- Giữ trạng thái Draft — Needs Confirmation và ghi các rule/schema gap vào OPEN_QUESTIONS.md.
- Loại trừ is_correct khỏi response cho Student. Hình dạng đầy đủ của QuizChoice vẫn SOURCE_REQUIRED.
- Dùng DB fields chỉ như candidate mapping, không khẳng định SQL hoặc live persistence.

## Conflicts

- DISCREPANCY: AC-16 diagram gắn nhánh eligibility/hết lượt/hết hạn với 403/409; catalog API #28 chỉ khai báo 403 và không có 409. DD giữ nguyên business-code set của catalog.
- SOURCE_REQUIRED: AC-16 nói quiz đang mở và Student có quyền làm quiz nhưng không định nghĩa enrollment, trạng thái quiz được phép, giới hạn lượt hoặc deadline.
- SOURCE_REQUIRED: QuestionType chưa có enum values hoặc cột vật lý; QuizChoice chưa có logical field definition.
- DISCREPANCY: Logical Quiz.course_id là required; checked-in DDL cho quizzes.course_id nullable. DB table design mô tả quan hệ bắt buộc. Live schema chưa được xác minh.
- UNWIRED / NOT_FOUND: Không tìm thấy API #28 trong Study router, module hoặc tests hiện tại.

## Security note

- Response Student không chứa is_correct hoặc dữ liệu đáp án đúng từ quiz_choices.
- Không nhận user_id từ client; endpoint chỉ khai báo quiz_id. Không suy đoán claim name hoặc enrollment predicate.
- Không suy ra quyền truy cập chỉ từ việc client đã gọi API khác trong AC-16.
- Không trả raw SQL, stack trace hoặc thông tin nội bộ trong error response.

## Performance note

- Contract không quy định pagination, cache, latency hoặc query plan.
- Catalog yêu cầu toàn bộ questions trong Quiz nhưng không quy định giới hạn kích thước; không tự thêm phân trang.
- quiz_questions.sort_order có thể làm candidate ordering theo câu hỏi; tie-break và thứ tự choices chưa được xác nhận.
