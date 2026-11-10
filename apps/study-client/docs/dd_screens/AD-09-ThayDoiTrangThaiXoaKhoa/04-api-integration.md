# AD-09 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-09-API-001` | #74 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `AD-09-API-002` | #76 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `AD-09-API-003` | #77 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #74, #76, #77
- Orchestration/data notes: PATCH #76 hoặc DELETE #77 sau khi policy được duyệt → reload #73/#74 theo điều hướng được chốt.
- BE/source status và gate: **R** local source #76/#77 route/module/test; API DD Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** #76 body/enum/transition còn DERIVED; `archive` không có mapping; #77 local soft-delete trái copy permanent-delete, dependency/repeat/restore/audit policy chưa duyệt; AC-32 permission vs `ADMIN`, live schema và Study Web UNWIRED; back/cancel và reload còn mở. **RUNTIME NOT VERIFIED**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API matrix — #74 / #76 / #77

| API | Method/endpoint | Auth and input | Response | Errors and current status |
|---|---|---|---|---|
| #74 | `GET /api/v1/admin/courses/{course_id}` | Bearer/Admin catalog; `course_id:int64`; no body. AC-32 finer permission mapping open. | `ApiEnvelope<Page<Course>>`; local #74 query maps Course+mentor in singleton Page; counters absent. | Catalog 401/403/404/500. Local route/source exists; API DD Draft; no DELETED filter. |
| #76 | `PATCH /api/v1/admin/courses/{course_id}/status` | Bearer/Admin; int64 path. Direct body absent. Local strict candidate `{status}` with DRAFT/PUBLISHED/SUSPENDED only. | `ApiEnvelope<Page<Course>>`; success `DESIGN_RESOURCE_UPDATED`; local message `Course status updated.` and singleton Page. | 401/403/404/422/500; route/module/tests local. Body/enum/transition/audit schema DERIVED; DD Draft. |
| #77 | `DELETE /api/v1/admin/courses/{course_id}` | Bearer/Admin; int64 path; no body/query. | `ApiEnvelope<DeleteResult>`; success `DESIGN_RESOURCE_DELETED`; fields `id`, literal `status:"deleted"`, `deleted_at`. | 401/403/404/422/500; dependency 422 and soft-delete policy DERIVED; route/module/tests local; DD Draft. |

**Status candidate details — DERIVED, owner decision required**

| Candidate body value | Current local effect | Contract/status |
|---|---|---|
| `DRAFT` | Directly sets legacy course status and `updated_at`; no separate enrollment/content mutation. Public API #06 filters PUBLISHED, but learner access behavior is not settled. | Body/enum and effects need approval. |
| `PUBLISHED` | Directly sets status; no readiness/content gate. Public listing may expose it under #06 PUBLISHED filter. | Body/enum/readiness need approval. |
| `SUSPENDED` | Directly sets status; does not alter existing enrollments/access. Learner access behavior remains open. | Body/enum/access policy need approval. |
| `ARCHIVED` | Not accepted by local #76 model; prototype radio says `archive`. | No mapping; do not send. |
| `DELETED` | Not in #76 request model. #77 locally sets tombstone after dependency check. #76 currently has no DELETED-target filter and can overwrite a tombstone with one of its candidate statuses. | Visibility/restore policy open; do not call this an approved restore action. |

**Delete dependency candidate details — DERIVED**

| Local check | Current predicate | Open question |
|---|---|---|
| Enrollment | Any row with matching `course_id`, regardless of status. | Whether completed/inactive records should block. |
| Generic Content | Any matching Content with `deleted_at IS NULL`. | Whether all course-linked content types/history are covered. |
| Lessons | Any matching lesson row. | Whether deleted/inactive lesson states should be excluded. |
| Quizzes | Any matching quiz row. | Whether deleted/inactive quiz states should be excluded. |
| Assignments | Any matching assignment row. | Whether assignment submissions/other course-linked relations need explicit checks. |

No dependency child is deleted by #77. The selected set may be incomplete; do not represent it as an owner-approved comprehensive dependency policy.

### Trích từ DD nguồn: Nguồn truy vết

- [Screen inventory](../../list_screen.md) · [Global screen plan](../../screen_stitch/dd_screens/PLAN.md) · [AC-32 admin flow](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [API catalog](../../../../../docs/lists/list_api.md) · [API #76 router](../../../../study-server/app/api/v1.py) · [#76 model](../../../../study-server/app/modules/admin/api_76_admin_course_status/models.py) · [#76 validator](../../../../study-server/app/modules/admin/api_76_admin_course_status/validate.py) · [#76 view](../../../../study-server/app/modules/admin/api_76_admin_course_status/view.py) · [#76 SQL](../../../../study-server/app/modules/admin/api_76_admin_course_status/query.py)
- [API #77 model](../../../../study-server/app/modules/admin/api_77_admin_course_delete/models.py) · [#77 validator](../../../../study-server/app/modules/admin/api_77_admin_course_delete/validate.py) · [#77 view](../../../../study-server/app/modules/admin/api_77_admin_course_delete/view.py) · [#77 SQL](../../../../study-server/app/modules/admin/api_77_admin_course_delete/query.py)
- [#76 open questions](../../../../study-server/docs/dd/76_admin_course_status/OPEN_QUESTIONS.md) · [#77 open questions](../../../../study-server/docs/dd/77_admin_course_delete/OPEN_QUESTIONS.md) · [#76 tests](../../../../study-server/tests/modules/admin/api_76_admin_course_status/test_admin_course_status.py) · [#77 tests](../../../../study-server/tests/modules/admin/api_77_admin_course_delete/test_admin_course_delete.py)
- [API #73 list SQL](../../../../study-server/app/modules/admin/api_73_admin_courses_list/query.py) · [API #74 detail SQL](../../../../study-server/app/modules/admin/api_74_admin_course_detail/query.py) · [legacy candidate DDL](../../../../../infra/postgres/study-server/DB.sql) · [migration 010 candidate](../../../../../infra/postgres/study-server/migrations/010_course_status_audit_logs.sql) · [V1-PILOT Course DDL](../../../../../infra/postgres/02_study_db.sql)
- [Study Web design target](../../../../../.agents/web-study/design.md) · [Study Web scope index](../../../../../.agents/web-work/study/INDEX.md)

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-09_thay-doi-trang-thai-xoa-khoa/AD-09.md)
