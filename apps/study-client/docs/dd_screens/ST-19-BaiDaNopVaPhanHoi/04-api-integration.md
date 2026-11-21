# ST-19 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## Current caller status — 2026-11-20

ST-19 calls #36 with Student Bearer, follows route changes, cancels stale reads,
validates the exact success code/ID/payload and offers retry. #36 derives
`user_id` from the authenticated Student and filters the query by both owner
and submission ID; missing or foreign rows return 404. The query returns
score/feedback only for `GRADED` and maps the legacy single `file_url` to a
zero-or-one files array. The page does not open the returned URL and hides
score/feedback unless status is `GRADED`. Runtime and tests were not verified.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-19-API-001` | #36 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #36
- Orchestration/data notes: ST-18 passes returned `data.id` as `submissionId`; GET #36 returns only the authenticated Student's matching submission. Display score/feedback only when returned status is `GRADED`; never open file URLs here.
- BE/source status and gate: **DD BLOCKED; IMPLEMENTATION PARTIAL; RUNTIME NOT VERIFIED:** #36 route/view/query/model and caller exist; query is owner-scoped and returns a single mapped file at most; score/feedback are projected only for GRADED. `data.id`/inventory `submission_id`, status/timezone/live-schema semantics and file URL access remain open; loaded-design fields (rubric, mentor/cohort/skill/next assignment) have no API data contract; PNG/HTML states and visual target differ.
- Contract sources and discrepancies are preserved in the source excerpts below.

> Source-DD excerpts below retain the earlier `UNWIRED`/`NOT_FOUND` snapshot; current source is summarized above.

### Trích từ DD nguồn: Nguồn truy vết

- [Inventory / F06](../../list_screen.md)
- [Original PNG](../../screen_stitch/03_student/ST-19_bai-da-nop-va-phan-hoi/screen.png), [HTML companion](../../screen_stitch/03_student/ST-19_bai-da-nop-va-phan-hoi/code.html), [marker map](../../screen_stitch/03_student/ST-19_bai-da-nop-va-phan-hoi/ST-19_markers.json), [annotated PNG](../../screen_stitch/03_student/ST-19_bai-da-nop-va-phan-hoi/screen_annotated.png)
- [API catalog #36](../../../../../docs/lists/list_api.md)
- [API #36 overview](../../../../study-server/docs/dd/36_submissions_detail/02_Overview.md), [request](../../../../study-server/docs/dd/36_submissions_detail/03_Request.md), [response](../../../../study-server/docs/dd/36_submissions_detail/04_Response.md), [data mapping](../../../../study-server/docs/dd/36_submissions_detail/05_Data_Mapping.md), [errors](../../../../study-server/docs/dd/36_submissions_detail/06_Error.md), [open questions](../../../../study-server/docs/dd/36_submissions_detail/OPEN_QUESTIONS.md)
- [AC-17](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio), [AC-23](../../../../study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio)
- [Mentor API #55 current implementation](../../../../study-server/app/modules/mentor/api_55_mentor_submissions_detail/view.py)
- [Candidate Study DDL](../../../../../infra/postgres/study-server/DB.sql), [Study Web current design/source status](../../../../../.agents/web-study/design.md)

### Trích từ DD nguồn: A.4. API contract và trạng thái source

| Thuộc tính | API #36 |
|---|---|
| Method / endpoint | `GET /api/v1/submissions/{submission_id}` |
| Authentication | Student Bearer JWT theo catalog; caller identity lấy từ token, không nhận user ID từ URL/body. |
| Path | `submission_id:int64!`; positivity, range và parse-failure response chưa được định nghĩa. |
| Query / body | Không khai báo query parameter hoặc request body. |
| Success | HTTP 200, `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Submission>`. |
| Errors | Chỉ 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`. Không thêm 400/422 theo suy đoán. |
| Current source | Student API #36 route/module/query/test `NOT_FOUND`; không có runtime call để xác minh. Mentor API #55 là operation khác. |
| Open policy | Owner/access predicate; 403-vs-404 masking; score/feedback release; file association/URL; status lifecycle/timezone; malformed path; candidate schema vs live schema. |

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-19_bai-da-nop-va-phan-hoi/ST-19.md)
