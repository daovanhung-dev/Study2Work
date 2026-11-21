---
task_id: "2026-10-11-create-study-api20-dd"
date: "2026-10-11"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD cho Study API #20

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: /home/daovanhung/.local/node-v24.21.0-linux-x64/bin/node scripts/select-worklogs.mjs --type docs --limit 3
- selector_result: 33 available; selected three; shortage none.
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-10-11/create-study-api16-dd.md
    - carry_forward: Giữ thiết kế và runtime tách biệt; source thiếu thì đánh dấu SOURCE_REQUIRED; API #20 không kế thừa schema của Order hoặc Payment.
  - path: .agents/worklog/2026-10-11/create-study-api17-dd.md
    - carry_forward: Không lấy response/payment semantics của API #17 làm contract cho API #20; giữ business code và hiện trạng theo nguồn riêng.
  - path: .agents/worklog/2026-10-11/create-study-api18-dd.md
    - carry_forward: Dùng đủ tám sheet template; giữ UNWIRED / NOT_FOUND; không tự giải quyết discrepancy.
  - path: .agents/worklog/2026-10-11/create-study-api19-dd.md
    - carry_forward: Draft khi còn gap; giữ DESIGN_ONLY tách khỏi runtime/schema; dùng OPEN_QUESTIONS.md, PLAN_RESULT.md, VERIFICATION_REPORT.md; không tạo ZIP theo Study workflow.
- shortage: none

## EXPECTED_BEHAVIOR

- Requirement: Tạo API Detail Design Markdown cho API #20 trong apps/study-server/docs/dd/20_users_me_courses/.
- Approved design contract: GET /api/v1/users/me/courses; Bearer JWT; role Student; query status?:string, page?:int32; ApiEnvelope<UserProfile>; 200 DESIGN_RESOURCE_RETRIEVED, 401 DESIGN_AUTHENTICATION_REQUIRED, 403 DESIGN_ACCESS_DENIED, 422 DESIGN_VALIDATION_ERROR, 500 DESIGN_INTERNAL_ERROR.
- AC-13: Liệt kê khóa đã đăng ký bằng Enrollment + Course; gọi riêng API #21 để lấy progress; client ghép danh sách và tiến độ, hiển thị empty state khi không có khóa học.
- Deliverables: Tám sheet theo template, ba report (OPEN_QUESTIONS.md, PLAN_RESULT.md, VERIFICATION_REPORT.md); không có ZIP.

## CURRENT_BEHAVIOR

- Router apps/study-server/app/api/v1.py chưa khai báo endpoint /users/me/courses; không có module hoặc test API #20 trong inventory đã kiểm tra.
- Shared auth helper hiện xác thực Bearer/JWT, chuyển sub số dương sang user ID và yêu cầu role STUDENT; API #20 chưa được wiring nên đây không phải bằng chứng endpoint chạy.
- Catalog UserProfile schema và current API #4 Pydantic model khác nhau ở bio; API #20 chưa có model riêng.
- DB_UNICA_TABLES.md liệt kê query API #20 trên enrollments là DESIGN_ONLY; DB.sql có bảng enrollments và courses, nhưng đây là checked-in schema/design evidence, không xác nhận live schema.
- API #21 dùng request/response có gap riêng; DD #20 chỉ ghi ranh giới gọi API #21 theo AC-13.

## SOURCE_TRACE

~~~text
GET /users/me/courses
  -> Bearer JWT / Student design contract
  -> AC-13: Enrollment JOIN Course
  -> client gọi riêng GET /users/me/progress (API #21), ghép course + progress
  -> hiện tại: route/module/test API #20 NOT_FOUND; query design-only
~~~

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Response payload | API catalog khai báo ApiEnvelope<UserProfile>; AC-13 và endpoint purpose cần danh sách Course | DISCREPANCY / SOURCE_REQUIRED | Giữ nguyên type catalog; không tự đổi thành Page<Course> hoặc thêm progress. |
| Filter status | Query khai báo string; enrollment/course status enum và target filter chưa được xác định | SOURCE_REQUIRED | Không liệt kê enum, default hoặc predicate như contract. |
| Pagination | Chỉ có page:int32; page base, size, ordering và meta chưa được nêu | SOURCE_REQUIRED | Không tự thêm page_size, LIMIT/OFFSET, sort hoặc Page metadata. |
| Empty result | AC-13 yêu cầu UI empty state; API wire shape khi rỗng chưa có contract | SOURCE_REQUIRED | Không tự xác định data=[], items=[] hay envelope khác. |
| Identity mapping | API dùng /me; current auth helper parse numeric JWT sub; query API #20 chưa wired tới enrollments.user_id | SOURCE_REQUIRED | Ghi evidence hiện có, không khẳng định query predicate/runtime behavior. |
| Runtime | Không có route/module/test cho API #20 | UNWIRED / NOT_FOUND | DD không được xem là runtime verification. |

## CONTEXT_UPDATES

- None expected; docs-only deliverable, không sửa context registry hoặc canonical source.

## VERIFICATION

- Deliverables: 8 template sheets and 3 reports in apps/study-server/docs/dd/20_users_me_courses/; no ZIP created.
- Static checker: STATIC_VALIDATION_OK; all JSON examples parsed; table widths consistent; code fences paired; relative links and anchors resolved.
- Whitespace: no trailing whitespace in DD files; git diff --check passed.
- Runtime inventory: no API #20 route/module/test found; status remains UNWIRED / NOT_FOUND.
- Study runtime tests: NOT_RUN — endpoint chưa được wiring và phạm vi chỉ tạo DD.
- Context validator: NOT_REQUIRED — no canonical context page or manifest changed.

## HANDOFF

- Human/API owner decisions in OPEN_QUESTIONS.md are required before the DD becomes Ready/Final or is used as an implementation contract.
