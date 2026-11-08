# ST-10 — Kiểm tra quyền và bắt đầu học · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-10` |
| Module | Student |
| Route | `/student/lessons/:lessonId/start` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** BLOCKED · **Implementation:** BLOCKED · **Runtime:** NOT VERIFIED |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ST-10.md](../../screen_stitch/03_student/ST-10_kiem-tra-quyen-va-bat-dau-hoc/ST-10.md), [ST-10_PLAN.md](../../screen_stitch/03_student/ST-10_kiem-tra-quyen-va-bat-dau-hoc/ST-10_PLAN.md), [ST-10_markers.json](../../screen_stitch/03_student/ST-10_kiem-tra-quyen-va-bat-dau-hoc/ST-10_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Không phát video hay lộ nội dung khi chưa có entitlement được xác minh phía server.
- In-scope: GET #22 → nếu allowed, POST #23 → GET #24 → ST-11; retry/idempotency và #23 auto-vs-click chưa chốt.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-14 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Không phát video hay lộ nội dung khi chưa có entitlement được xác minh phía server. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #22, #23, #24
- Liên kết màn hình dự kiến: [ST-11](../ST-11-TrinhHocBaiLessonPlayer/00-overview.md), [ST-09](../ST-09-TongQuanKhoaDangHoc/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | checking/denied/started/failure |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-10 source screen.png](../../screen_stitch/03_student/ST-10_kiem-tra-quyen-va-bat-dau-hoc/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-10_kiem-tra-quyen-va-bat-dau-hoc/screen_annotated.png))
- Luồng: GET #22 → nếu allowed, POST #23 → GET #24 → ST-11; retry/idempotency và #23 auto-vs-click chưa chốt.
- Priority: P1; Gate/source status: **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** #22–#24 catalog/API-DD Draft, no Student route/module/query/test; AC-14/15 gate and payload gaps; public #09 exposes published `content`/`video_url` without enrollment check; BIGINT vs V1-PILOT UUID progress schema mismatch; ST-09 lessonId handoff absent; ST-10/ST-11 #24 ownership unresolved; Study Web UNWIRED; `423_LOCKED`/Session Token copy is static

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ST-10 — Kiểm tra quyền và bắt đầu học

> **DD status:** BLOCKED · **Implementation:** BLOCKED · **Runtime:** NOT VERIFIED
> **Phạm vi phiên:** chỉ ST-10. Đây là đặc tả theo bằng chứng thiết kế/source hiện có; mockup và API Draft không xác nhận hành vi đang chạy.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ST-10 — Kiểm tra quyền và bắt đầu học (Transition) |
| Mục tiêu mong đợi | Kiểm tra Student có quyền học lesson, ghi nhận lần bắt đầu theo contract đã duyệt, lấy nội dung lesson rồi chuyển sang ST-11. Nếu access bị từ chối, không tải nội dung/media. |
| Actor | Student đã đăng nhập và đã enrolled vào course chứa lesson theo AC-14. AC-15 yêu cầu Student có quyền xem lesson. |
| Route | Inventory đề xuất /student/lessons/:lessonId/start. Study Web không có editable source/router; route chưa được xác minh khi chạy. |
| Input chính | lessonId từ ST-09. Path param được catalog #22–#24 khai báo lesson_id:int64!; range/validation ngoài kiểu bắt buộc chưa được chốt. |
| Màn hình trước/sau | ST-09 → ST-10 → ST-11. ST-09 design hiện không có lesson list/selection hoặc lessonId handoff; ST-11 route được inventory ghi là /student/lessons/:lessonId. |
| API thiết kế | #22 GET /api/v1/lessons/{lesson_id}/access; #23 POST /api/v1/lessons/{lesson_id}/start; #24 GET /api/v1/lessons/{lesson_id}. Cả ba yêu cầu Bearer JWT/Student trong catalog, nhưng chưa có current route/module/query/test source. |
| Asset hiện có | PNG đầy đủ 1566×1600; HTML mockup tĩnh cho entitlement gate. Hình là thiết kế handoff, không phải browser/runtime capture. |
| Trạng thái | DD BLOCKED bởi access predicate, payload, idempotency, lesson projection và upstream lessonId chưa chốt. Implementation BLOCKED do Study Web route/source và APIs #22–#24 chưa wired. Runtime NOT VERIFIED. |

### Nguồn và mức độ bằng chứng

| Nguồn | Điều dùng làm bằng chứng | Trạng thái |
|---|---|---|
| [Screen inventory](../../list_screen.md) và [global plan](../../screen_stitch/dd_screens/PLAN.md) | ST-10 route, actor, AC-14, APIs #22–#24, trạng thái checking/denied/started/failure và thứ tự gọi dự kiến. | Expected design |
| [ST-10 plan](../../screen_stitch/03_student/ST-10_kiem-tra-quyen-va-bat-dau-hoc/ST-10_PLAN.md) | Scope, source audit, marker/event coverage, blockers. | Plan complete |
| [AC API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) và [AC-14/15 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) | AC-14 precondition enrollment, access/prerequisite decision, start/progress flow, content access. | Business design; chi tiết predicate/response còn mở |
| [API catalog](../../../../../docs/lists/list_api.md) | Method/path/auth/path param/response/status codes cho #22–#24. | Declared design |
| [API #22 DD](../../../../study-server/docs/dd/22_lessons_access/00_Cover.md), [open questions](../../../../study-server/docs/dd/22_lessons_access/OPEN_QUESTIONS.md) | Access rule, identity, 403 reason, 404, projection. | Draft — Needs Confirmation |
| [API #23 DD](../../../../study-server/docs/dd/23_lessons_start/00_Cover.md), [open questions](../../../../study-server/docs/dd/23_lessons_start/OPEN_QUESTIONS.md) | UPSERT identity/state, repeated start, response, authorization, transaction. | Draft — Needs Confirmation |
| [API #24 DD](../../../../study-server/docs/dd/24_lessons_detail/00_Cover.md), [open questions](../../../../study-server/docs/dd/24_lessons_detail/OPEN_QUESTIONS.md) | Entitlement/publish predicate, projection, error/null rules. | Draft — Needs Confirmation |
| Study Server router/modules/tests | Exact search for Student endpoints #22–#24; Admin lesson APIs #82–#86 use a separate `/admin` path and permission. | #22–#24 NOT_FOUND; Admin routes are not substitutes |
| [API #09 current route/query/view](../../../../study-server/app/api/v1.py), [query](../../../../study-server/app/modules/guest/api_09_courses_curriculum/query.py), [view](../../../../study-server/app/modules/guest/api_09_courses_curriculum/view.py) | Public curriculum query returns published lesson fields including `content` and `video_url`; no auth/enrollment context is passed. | Source-backed current behavior; this is not the #24 access contract |
| [DB design](../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md), [BIGINT DDL](../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT UUID DDL](../../../../../infra/postgres/02_study_db.sql), [database context](../../../../../.agents/project/database.md) | Two checked-in models differ for `lesson_progress`; no API #23 mapping or live metadata is verified. | Design/bootstrap artifacts; live schema NOT VERIFIED |
| [Study Web context](../../../../../.agents/web-work/study/INDEX.md) và [Study UI guide](../../../../../.agents/web-study/design.md) | Current client source/wiring status and intended visual target. | Feature routes UNWIRED; guide is intended design |
| [Source PNG](../../screen_stitch/03_student/ST-10_kiem-tra-quyen-va-bat-dau-hoc/screen.png), [source HTML](../../screen_stitch/03_student/ST-10_kiem-tra-quyen-va-bat-dau-hoc/code.html), [marker map](../../screen_stitch/03_student/ST-10_kiem-tra-quyen-va-bat-dau-hoc/ST-10_markers.json), [annotated PNG](../../screen_stitch/03_student/ST-10_kiem-tra-quyen-va-bat-dau-hoc/screen_annotated.png) | Static appearance and interactive markup. | Design assets, not runtime evidence |

### Discrepancies cần giữ rõ

1. Asset hiển thị STATUS: 423_LOCKED. API catalog #22–#24 không khai báo HTTP 423 hoặc business code tương ứng; đây là static copy, không phải API response.
2. API #22 kiểm tra access nhưng success schema là ApiEnvelope<Lesson>, không có access boolean; AC-14 nói nhánh deny trả 403 “+ lý do”, nhưng catalog/envelope chưa quy định field reason. HTTP 200/403 cho phép phân nhánh theo status ở mức thiết kế, song predicate và reason chưa chốt.
3. AC-14 mô tả #23 UPSERT lesson_progress sang IN_PROGRESS; catalog #23 trả 201 Created và ApiEnvelope<Lesson>. Key, repeated-start semantics, field preservation, idempotency, response assembly và direct-call authorization còn mở.
4. #23 generic Lesson response có thể gồm content/video_url theo reusable schema; chưa có quyết định xác nhận payload nào được trả ở bước start.
5. #24 trả ApiEnvelope<Lesson>, với content/video_url optional trong catalog; API chưa có current implementation để xác nhận authorization, publication checks hoặc null serialization.
6. ST-09 source hiện không có lesson card/selection và CTA không có lessonId; vì vậy flow tới ST-10 thiếu đầu vào trong bộ screen design hiện có.
7. HTML nói “Session Token”, “giải phóng media” và “khóa vĩnh viễn” nhưng API catalog/DD không khai báo token/media grant hoặc trạng thái khóa vĩnh viễn.
