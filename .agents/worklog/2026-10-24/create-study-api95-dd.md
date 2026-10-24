---
task_id: "2026-10-24-create-study-api95-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #95 — Admin xóa hoặc hủy notification

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ expected/current tách biệt, không bịa mapping hoặc runtime; các giả định phải gắn `DERIVED`.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Giữ response theo catalog, giữ `UNWIRED`/`SOURCE_REQUIRED`, không ghép schema khác grain.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Candidate DDL không phải runtime; kiểm tra cross-API logic và giữ contract/error set nguyên vẹn.
- shortage: `none`
- Additional current artifact reviewed: `.agents/worklog/2026-10-24/create-study-api94-dd.md` and the post-#94 count inventory.

## EXPECTED_BEHAVIOR

- Requirement: Tạo một DD tiếng Việt cho API #95, lập plan trước authoring, đọc kỹ AC-36 diagram, tham chiếu #92–#94 và các DELETE Admin precedents, rồi kiểm tra ngay. Chưa đóng macro-review AC-36 trước khi #96 DD hoàn tất.
- Catalog #95: `DELETE /api/v1/admin/notifications/{notification_id}`; Bearer JWT; role Admin; path `notification_id:int64!`; không khai báo body/query; response `ApiEnvelope<DeleteResult>`; HTTP 200 `DESIGN_RESOURCE_DELETED`; exact errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`.
- Reusable `DeleteResult`: `id:int64`, `status:"deleted"`, `deleted_at:date-time`.
- AC-36: Admin có notification-management permission; nhánh DELETE đi tới logical node `DELETE/mark cancelled`, rồi reload notification management. Catalog purpose cho phép xóa draft/cancel nếu policy cho phép.

## CURRENT_BEHAVIOR

- Source scan: không có route/module/view/test API #95 trong Study source hiện tại; status `UNWIRED / NOT_FOUND`.
- Legacy Study `notifications`: BIGINT id, `user_id`, `sender_id`, `title`, `content`, `type`, `is_read`, `created_at`; không có deletion timestamp, status, schedule hoặc campaign delivery relation.
- V1-PILOT `notifications`/`notification_deliveries`: UUID, learner/delivery grain; delivery rows có append-only rule. Không dùng model này làm physical target cho API Admin BIGINT.
- API #96 response là `Notification`, không có delivery aggregate fields; không thể dùng contract #96 để chứng minh dispatch chưa bắt đầu.
- Admin permission, target persistence, lifecycle enum, delivery-start signal, tombstone timestamp và scheduler cancellation contract chưa có source đủ để xác nhận.
- Runtime/deployment/live DB chưa được kiểm tra; không chạy application tests cho task docs-only.

## SOURCE_TRACE

```text
Admin + notification-management permission -> DELETE notification_id -> load logical Notification and determine deletion/cancellation eligibility -> mark removed/cancelled without losing history (DERIVED proposal) -> DeleteResult/200 or exact catalog error -> reload management; scheduler state and physical writes remain SOURCE_REQUIRED
```

## API REQUIREMENT MATRIX

| ID | Method/path | Actor/auth | Direct request | Direct response/success/errors | Business intent | Status |
|---|---|---|---|---|---|---|
| #95 | `DELETE /api/v1/admin/notifications/{notification_id}` | Bearer JWT; Admin; AC permission required | Path `notification_id:int64!`; no body/query | `ApiEnvelope<DeleteResult>`; 200 `DESIGN_RESOURCE_DELETED`; exact 401/403/404/422/500 codes | AC-36 DELETE/mark cancelled then reload | Direct contract; conditional policy not specified |

## REQUEST USAGE MATRIX

| Input | Direct source/use | Validation/proposal | Query/mutation use | Gap/status |
|---|---|---|---|---|
| `Authorization` | Bearer JWT; Admin role | AC-36 requires notification-management permission | Authorization before resource operation | Claim/policy/scope `SOURCE_REQUIRED` |
| `notification_id` | Required path `int64` | No positivity/range rule declared | Locate target notification | Physical table/key and parse behavior unresolved |
| Body/query | None declared | Do not add a reason/action field | None | Direct N/A |
| Delete/cancel policy | Purpose says draft delete/cancel if allowed | `DERIVED` proposal: draft → logical removal; scheduled and not yet dispatched → mark cancelled; any delivery started → reject with existing 422 | Eligibility guard before mutation | Status values and delivery-start source `SOURCE_REQUIRED` |

## QUERY MATRIX

| Query ID | Purpose | Physical source/columns | Predicate/order | Status |
|---|---|---|---|---|
| Q1 | Resolve target notification | No approved Admin campaign table; legacy BIGINT row is partial only | Logical id equals `notification_id` | `SOURCE_REQUIRED`; no SQL invented |
| Q2 | Determine lifecycle state and delivery-start eligibility | No approved Admin state/delivery relation; #96 contract does not expose an aggregate | Draft/Scheduled/no-send-started proposal | `DERIVED / SOURCE_REQUIRED`; no reliable source today |
| Q3 | Determine scheduled work to cancel | No scheduler/queue/Operation persistence source found | No external operation selector in direct request | `SOURCE_REQUIRED`; no cancellation call specified as current behavior |

## MUTATION MATRIX

| ID | Logical operation | Candidate target | Fields/effect | Transaction/failure | Mapping/status |
|---|---|---|---|---|---|
| M1 | Remove draft from active management | Admin Notification; no approved physical model | Proposed soft/tombstone removal, retaining recipient/delivery history | Atomic state transition and timestamp source unresolved | `07_notifications_delete.md`; logical effect DERIVED, physical columns SOURCE_REQUIRED |
| M2 | Cancel eligible scheduled notification | Admin Notification plus any scheduler job | Proposed mark-cancelled before any delivery starts; no provider action or delivery-row rewrite inferred | Scheduler cancellation/idempotency/transaction unresolved | `08_notification_delivery_cancel.md`; external contract SOURCE_REQUIRED |
| M3 | Hard delete recipients/delivery history | None | Not proposed; preserve history | No DELETE cascade inferred | N/A |

## RESPONSE SOURCE MATRIX

| Response field | Direct type/source | Transform/null rule | Gap/status |
|---|---|---|---|
| `success` | Shared envelope | true on successful request | Envelope convention |
| `businessCode` | Catalog | `DESIGN_RESOURCE_DELETED` | DIRECT |
| `message` | Envelope/application | Exact wording unspecified | SOURCE_REQUIRED |
| `data.id` | DeleteResult `int64` | Target notification ID | Direct type; physical source unresolved |
| `data.status` | Literal `"deleted"` | Preserve direct literal for delete and cancel result | DIRECT shape; meaning for cancellation needs confirmation |
| `data.deleted_at` | `date-time` | Proposed time logical removal/cancellation commits | DIRECT field; timestamp source/persistence SOURCE_REQUIRED |
| `traceId` | Shared request context | Propagate current trace convention | Convention; route absent |
| `meta` | Shared envelope | Follow API Guidelines/current helper boundary | Exact shape/source discrepancy remains |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status/impact |
|---|---|---|
| Delete versus cancel | Catalog says delete draft/cancel if policy permits; diagram DB node says `DELETE/mark cancelled` | `DISCREPANCY`; use one logical API with conditional outcomes only as DERIVED proposal |
| Eligibility rule | No state enum, policy table or delivery-start definition | `SOURCE_REQUIRED`; proposed draft/scheduled rule needs owner confirmation |
| `DeleteResult` on cancellation | Direct literal is `status:"deleted"`; business action may be cancellation | `DISCREPANCY`; preserve contract and clarify literal semantics |
| Tombstone/timestamp | Legacy table has no deleted/cancelled state or timestamp | `SOURCE_REQUIRED`; no column invented |
| Delivery model | V1-PILOT delivery rows use UUID and append-only policy; Admin contract uses int64 Notification | `DISCREPANCY`; do not update/delete pilot rows by analogy |
| #96 status contract | API #96 returns Notification; no delivery aggregate fields in schema | `DISCREPANCY`; cannot use its response to choose cancellation policy |
| Scheduler/operation | No Admin scheduler persistence/producer; #93 Operation response/ID conflict is still open | `SOURCE_REQUIRED / DISCREPANCY`; #95 does not invent an operation ID |
| Authorization | AC-36 requires Admin permission, no Study Admin guard verified | `UNWIRED / SOURCE_REQUIRED` |

## PLANNED_OUTPUT

- API folder: `apps/study-server/docs/dd/95_admin_notifications_delete/`.
- Eight standard sheets: `00_Cover.md`, `01_Lich_su.md`, `02_Overview.md`, `03_Request.md`, `04_Response.md`, `05_Data_Mapping.md`, `06_Error.md`, `07_notifications_delete.md`.
- Supplementary logical cancellation mapping: `08_notification_delivery_cancel.md`.
- Three reports: `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`.
- Expected package: 12 Markdown files total (9 sheets including supplementary mapping, plus 3 reports).
- Preserve the catalog response/error set; label all lifecycle, idempotency, tombstone and scheduler proposals `DERIVED` or `SOURCE_REQUIRED`.
- Expected after creation: 95 DD folders, 8 IDs #96–#103 missing, 83 complete standard report packages; source-programmed count remains 12/103 with 91 lacking a route-plus-view pair.
- AC-36 macro-review remains pending until API #96 DD is authored.
- No application tests/runtime changes, catalog, schema, diagram or context edits.

## PLAN STATUS

Plan and requirement/request/query/mutation/response-source matrices were recorded before creation of the API #95 DD folder. Authoring and immediate static verification are recorded below.

## VERIFICATION_RESULT

- Package: 12 Markdown files — eight standard sheets, one supplementary cancellation-boundary mapping, and three reports.
- Template appendix: 9/9 sheets match the corresponding template-backed appendix from API #94 byte-for-byte.
- Front matter: 9/9 sheets carry dd_id `95` and `Draft — Needs Confirmation`.
- Direct contract: catalog method/path/path type/no body/query/DeleteResult/HTTP 200 and exact five errors checked against source; lifecycle proposals remain DERIVED.
- Static content checks: 1/1 JSON example parses; 32 Markdown tables have consistent widths; code fences are balanced; 32 local links/anchors resolve; all files have final newlines and no trailing whitespace.
- Source scan: no API #95 route/module/test marker found in scoped `apps/study-server/app` and `tests`; `UNWIRED / NOT_FOUND` (static only).
- Inventory: 95 DD folders with all eight core sheet roles; 8 missing (#96–#103); 83/95 have all three standard reports. Static route+view source count remains 12/103; 91 lack that pair.
- No application tests, runtime/deployment checks or live DB checks were run. No application source, catalog, schema, diagram or context page changed; context validator not applicable.

## HANDOFF

- Next API DD: #96, Admin notification status; after authoring, macro-review the full AC-36 set #92–#96.
- Keep lifecycle eligibility, tombstone/timestamp, scheduler cancellation, DeleteResult semantics and idempotency proposals unapproved until owner confirmation.

## GROUP_MACRO_REVIEW

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` after API #96 DD was created; document-level cross-review covers #92–#96.
- Report: `apps/study-server/docs/dd/96_admin_notifications_status/AC-36_MACRO_REVIEW.md`.
- Findings: list response/cardinality remains unresolved; #93 Notification-vs-Operation, conditional Send and ID bridge remain unresolved; #94 body/schedule are DERIVED; #95 delete/cancel and delivery-start policy are SOURCE_REQUIRED; #96 aggregate intent is not represented in its direct Notification response. Shared Admin model, grain, enums and permission remain open.
- Application tests, runtime and live schema were not checked as part of this document review.
