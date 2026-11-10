# ST-17 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-17-API-001` | #33 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #33
- Orchestration/data notes: GET #33 → server quyết định deadline/permission; không dùng clock UI làm nguồn quyền. CTA chỉ handoff `assignmentId` sang ST-18 khi eligibility contract được duyệt.
- BE/source status và gate: **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** API #33 Draft, Student route/module/test NOT_FOUND; access/deadline/submission-rule/403-vs-409 unresolved; Assignment response thiếu phần lớn loaded-screen fields; legacy BIGINT assignment tables vs V1-PILOT không có business assignment tables, adapter/live schema chưa xác minh; PNG/HTML actor-state mismatch và visual target mismatch; Study Web UNWIRED; #34 chỉ là upload source-backed, #35/#36 Student routes chưa có
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: F. Acceptance checklist, blockers and source trace

### F.1. Blockers to resolve before DD READY

1. Implement/register Student API #33 and Study Web route; add runnable route/module/test evidence before describing runtime behavior.
2. Approve direct assignment/course access predicate and 403-vs-404 masking.
3. Define whether #33 returns after deadline, exact deadline boundary/timezone/server-time source, and reconcile AC-17 403/409 with the catalog's 401/403/404/500 set.
4. Define the AC-17 “submission rule” schema and owner; do not add it to `Assignment` without contract approval.
5. Reconcile `course_id`/`max_score` required logical fields with nullable candidate DDL; define optional null/omit behavior, timestamp timezone and decimal scale/rounding.
6. Supply approved sources for course title, status/submitted state/history, weight/progress, rubric/objectives, resources/video, mentor/SLA, checklist, late policy and contact actions—or remove those claims from the loaded design.
7. Approve ST-17 → ST-18 route/eligibility handoff and define which server state enables the CTA.
8. Reconcile the loaded Student PNG with the Guest unavailable HTML fallback; align the selected state/layout with the Study Web font, width, responsive and control-size target; define empty/loading/error UI and destinations.
9. Reconcile the legacy BIGINT assignment tables with the V1-PILOT schema, which has no business assignment/submission tables; approve the source schema and API #33 adapter before implementation.

### F.2. Checklist

- [x] ST-17 plan completed before marker map, annotated image and DD authoring.
- [x] Original `screen.png` and `code.html` preserved; hashes/dimensions recorded.
- [x] 49 ordered markers map one-to-one to 49 elements in section C.
- [x] Route load, response mapping, deadline, checklist, resource/contact, ST-18 handoff and auth/error/navigation events described.
- [x] API catalog, API #33 Draft DD, AC-17, candidate DDL and current missing Student route/source kept distinct.
- [x] Screenshot/HTML discrepancy, unsupported fields/actions and API 403/409 discrepancy recorded.
- [x] Legacy BIGINT vs V1-PILOT assignment-schema gap and Study Web design-target mismatch recorded.
- [ ] Resolve F.1 contract/source blockers before declaring DD READY or implementation-ready.
- [ ] Verify actual route/API/runtime before marking RUNTIME VERIFIED.

### F.3. Source traceability

- [ST-17 plan](../../screen_stitch/03_student/ST-17_chi-tiet-bai-tap/ST-17_PLAN.md), [marker map](../../screen_stitch/03_student/ST-17_chi-tiet-bai-tap/ST-17_markers.json), [annotated screen](../../screen_stitch/03_student/ST-17_chi-tiet-bai-tap/screen_annotated.png), [source PNG](../../screen_stitch/03_student/ST-17_chi-tiet-bai-tap/screen.png), [HTML companion](../../screen_stitch/03_student/ST-17_chi-tiet-bai-tap/code.html).
- [Screen inventory / ST-17 and linked ST-18/ST-09](../../list_screen.md).
- [API catalog #33 and Assignment schema](../../../../../docs/lists/list_api.md).
- API #33 DD: [overview](../../../../study-server/docs/dd/33_assignments_detail/02_Overview.md), [request](../../../../study-server/docs/dd/33_assignments_detail/03_Request.md), [response](../../../../study-server/docs/dd/33_assignments_detail/04_Response.md), [mapping](../../../../study-server/docs/dd/33_assignments_detail/05_Data_Mapping.md), [errors](../../../../study-server/docs/dd/33_assignments_detail/06_Error.md), [open questions](../../../../study-server/docs/dd/33_assignments_detail/OPEN_QUESTIONS.md), [verification report](../../../../study-server/docs/dd/33_assignments_detail/VERIFICATION_REPORT.md).
- [AC/API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-17 activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio).
- [Candidate assignment table design](../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md), [legacy candidate DDL](../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT schema artifact](../../../../../infra/postgres/02_study_db.sql).
- [Current Study route inventory](../../../../../.agents/server-study/apis/declared-routes.md), [Study Web status](../../../../../.agents/web-work/study/INDEX.md), [Study Web design target](../../../../../.agents/web-study/design.md).
- Current downstream upload source: [API #34 route](../../../../study-server/app/api/v1.py), [upload flow](../../../../study-server/app/modules/student/api_34_uploads/view.py). This does not establish current #35/#36 Student routes.

### Trích từ DD nguồn: A.4. API #33 contract và giới hạn

| Thuộc tính | Contract hiện có | Giới hạn |
|---|---|---|
| Method / endpoint | `GET /api/v1/assignments/{assignment_id}` | Catalog/design-only; route Student hiện hành không có. |
| Authentication | Bearer JWT; role Student | API #33 chưa gọi auth helper; direct assignment/course access predicate chưa chốt. |
| Path | `assignment_id:int64!` | Không có min/max/positivity/parse-failure mapping. |
| Query / body | Không khai báo | Không thêm filter, `user_id` hoặc request body. |
| Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Assignment>` | API DD `Draft — Needs Confirmation`; exact optional/null serialization chưa chốt. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR` | AC-17 403/409 nhánh quá hạn/không quyền khác catalog; không thêm 409. |
| Assignment fields | `id`, `course_id`, `title`, `description?`, `due_at?`, `max_score` | Không chứa những dữ liệu phụ trong mockup; logical `course_id`/`max_score` bắt buộc nhưng DDL cho nullable. |

API #33 DD questions Q-33-01…05 giữ mở: access/403-vs-404; deadline GET/rejection/boundary/403-vs-409; submission-rule ownership/schema; nullability/timezone/decimal serialization; path parsing/error mapping. Candidate `assignments` table là design evidence, không phải live schema.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-17_chi-tiet-bai-tap/ST-17.md)
