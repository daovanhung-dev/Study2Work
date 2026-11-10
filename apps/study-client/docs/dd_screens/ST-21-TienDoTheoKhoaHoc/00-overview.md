# ST-21 — Tiến độ theo khóa học · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-21` |
| Module | Student |
| Route | `/student/progress/:courseId` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái:** DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. API #37 chưa có Student route/module/query/test; `UserProfile` theo catalog không chứa dữ liệu tiến độ; quy tắc aggregate/access/empty state còn mở. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ST-21.md](../../screen_stitch/03_student/ST-21_tien-do-theo-khoa-hoc/ST-21.md), [ST-21_PLAN.md](../../screen_stitch/03_student/ST-21_tien-do-theo-khoa-hoc/ST-21_PLAN.md), [ST-21_markers.json](../../screen_stitch/03_student/ST-21_tien-do-theo-khoa-hoc/ST-21_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Các bài đã/đang/chưa học, tỷ lệ hoàn thành, mốc thời gian có chứng cứ.
- In-scope: GET #37 theo course_id; liên kết lesson_id → ST-10/11 sau gate.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-18 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Các bài đã/đang/chưa học, tỷ lệ hoàn thành, mốc thời gian có chứng cứ. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #37
- Liên kết màn hình dự kiến: [ST-11](../ST-11-TrinhHocBaiLessonPlayer/00-overview.md), [ST-20](../ST-20-TongQuanTienDo/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/empty/in-progress/completed |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-21 source screen.png](../../screen_stitch/03_student/ST-21_tien-do-theo-khoa-hoc/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-21_tien-do-theo-khoa-hoc/screen_annotated.png))
- Luồng: GET #37 theo course_id; liên kết lesson_id → ST-10/11 sau gate.
- Priority: P2; Gate/source status: **D**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ST-21 — Tiến độ theo khóa học

> **Trạng thái:** DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. API #37 chưa có Student route/module/query/test; `UserProfile` theo catalog không chứa dữ liệu tiến độ; quy tắc aggregate/access/empty state còn mở.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### A.1. Định danh

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ST-21 — Tiến độ theo khóa học (Page) |
| Mục tiêu | Cho Student xem trạng thái học theo một course, các unit đã/đang/chưa học, tỷ lệ hoàn thành và mốc thời gian có nguồn. |
| Actor | Student theo inventory và API catalog #37; route guard hiện không có trong Study Web source. |
| Route thiết kế | `/student/progress/:courseId` — route đề xuất, chưa có frontend router/runtime. |
| API dự kiến | GET API #37 `/api/v1/users/me/progress/{course_id}`. |
| Màn hình liên quan | Vào từ ST-20 khi chọn course; quay lại ST-20; theo inventory, `lesson_id` có thể dẫn tới ST-10/ST-11 sau access gate. |
| Elements / events | 11 nhóm element `ST21-EL-01…ST21-EL-11`; 9 event `ST21-EV-01…ST21-EV-09`. |
| Trạng thái | DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. |

### A.2. Expected behavior

- Inventory ST-21 yêu cầu route `/student/progress/:courseId`, AC-18, API #37; các lesson đã/đang/chưa học, tỷ lệ hoàn thành và timestamp có chứng cứ; links tới ST-10/ST-11 sau gate; states `loading/empty/in-progress/completed`.
- API #37 catalog khai báo `GET /api/v1/users/me/progress/{course_id}`, Student Bearer JWT, path `course_id:int64!`, không có query/body, response `ApiEnvelope<UserProfile>`. Success: HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; errors: 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`.
- AC-18 mô tả Student đã đăng nhập chọn course, gọi #37 và “Aggregate lesson + quiz + assignment progress”. Không có schema output, công thức, denominator, weighting, selection policy hoặc rounding rule.
- API #37 DD `Draft — Needs Confirmation`; response giữ `UserProfile` theo catalog nhưng ghi rõ không có progress fields. Chín câu hỏi mở bao gồm response DTO, aggregate, quiz/submission selection, enrollment/access, 403/404 masking, course chưa có progress, path parse, JWT identity/live schema và UserProfile projection.

### A.3. Current behavior và tài sản

- `screen.png` nguyên trạng 1280×1024, SHA256 `1bd43f7a29ad1b1591953a03846d57ce5736839e8fa6c47921d12a334056bf65`; ảnh gần như chỉ có nền trống và dải tối ở đáy, không có thành phần UI để đọc/đánh số.
- `code.html` SHA256 `7eb0ba19f73bccf1b248205fdbac94eedf25ec059345f69c77175cfd2f3bcda6`; là static no-progress fallback gồm header, breadcrumb, heading/copy, icon, empty card, nút quay lại ST-20 và footer. Không có script, API call, auth, route-param binding hoặc lesson list.
- Tạo `screen_rendered.png` riêng từ `code.html` bằng Chrome Stable headless/CDP, kích thước 1280×916, SHA256 `ac30e06639a2002b0c2343303d6c91955be2885d925ec0a71dd16b69688f9ded`. Đây là HTML/CSS render tĩnh, không phải application/API runtime. `screen_annotated.png` (1376×916) dựa trên ảnh render này; ảnh nguồn `screen.png` và HTML không bị sửa.
- Study Web hiện chỉ có docs/assets và ignored compiled `dist` với root route `/`; không có editable app source/package/router/route ST-21. Serving/deployment chưa xác minh.
- API #37 Student route/module/query/test không có trong current Study Server source. API #65/#67 là Mentor progress endpoints khác actor/path/authorization, không thay thế #37.

### A.4. API và trạng thái source

| Thuộc tính | API #37 |
|---|---|
| Method / endpoint | `GET /api/v1/users/me/progress/{course_id}` |
| Authentication | Bearer JWT; role Student theo catalog. Claim-to-user mapping và route guard chưa được #37 xác định trong current source. |
| Path | `course_id:int64!`; min/max/domain, parse/range behavior chưa đặc tả. |
| Query / body | Không có query parameter hoặc request body trong catalog/DD request. |
| Success | HTTP 200, `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<UserProfile>`. `UserProfile` không có progress fields nên không map được expected course/lesson progress. |
| Errors | Chỉ 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`. Catalog không khai báo 400/422. |
| Current source | `DECLARED_NOT_RUNNABLE`: #37 route/module/query/test NOT_FOUND. API DD Draft; không có request chạy được để xác minh. |

### A.5. Data candidates, quy tắc và bảo mật

- API #37 DD nêu candidate sources: `lesson_progress`→`lessons`/`courses`; `quiz_attempts`→`quizzes`; `assignment_submissions`→`assignments`. Đó là candidate read set, không phải query/rule đã duyệt.
- Legacy `infra/postgres/study-server/DB.sql` có `lesson_progress` với `status`, `progress_percent`, `last_accessed_at`, `completed_at`. `infra/postgres/02_study_db.sql` lại có V1-PILOT `lesson_progress_facts` (UUID enrollment/lesson, status, first_started/completed times) và `progress_snapshots` (scope, counts, percent, high watermark, calculation version). Đây là hai schema generation khác nhau; không tự chọn hoặc reconcile chúng. Không nguồn nào ở đây chứng minh live schema/deployment cho #37.
- `progress_percent` của từng lesson không tự cho biết course completion rate. Không đặt denominator, quiz weighting, assignment weighting, latest/best attempt, submitted/graded policy, hidden/inapplicable item rules, overall state, timestamp selection hoặc rounding.
- Chưa chốt có cần enrollment/active course/published state, principal JWT mapping, quyền theo course, 403-vs-404 masking và resource visibility. Không nhận `user_id` do client nhập; `/me` identity phải đến từ principal sau khi API contract quy định.
- Không dùng dữ liệu của Mentor #65/#67 làm nguồn thay thế; không expose nội dung lesson trong trang progress trước gate của flow học.
