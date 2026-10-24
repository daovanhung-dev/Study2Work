---
task_id: "2026-10-24-create-study-api94-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #94 — Admin cập nhật notification

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ contract trực tiếp riêng với `DERIVED`; không suy luận table/counter hoặc runtime.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Giữ nguyên response cardinality theo catalog; field/value chưa có nguồn thì ghi `SOURCE_REQUIRED`.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Schema chỉ là candidate, không đồng nghĩa runtime; theo dõi query/mutation/response-source matrix.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Yêu cầu: Tạo một DD Markdown tiếng Việt cho API #94 sau khi lập plan; đọc AC-36 và DD #92–#93, tham chiếu các precedent PUT Admin; không sửa source, catalog, diagram hoặc schema.
- Catalog #94: `PUT /api/v1/admin/notifications/{notification_id}`; Bearer JWT; role Admin; path `notification_id:int64!`; không khai báo query hoặc body; response `ApiEnvelope<Notification>`; HTTP 200 `DESIGN_RESOURCE_UPDATED`; errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`.
- AC-36: Admin cần notification-management permission; nhánh UPDATE gọi #94, cập nhật Notification rồi reload notification management. Diagram không nêu body, field rules, trạng thái chuyển tiếp hoặc scheduler effect.

## CURRENT_BEHAVIOR

- API source scan: không tìm thấy route/module/view/test cho #94 trong Study server; status `UNWIRED / NOT_FOUND`.
- Legacy `notifications` DDL: BIGINT id, nullable `user_id`/`sender_id`, `title`, `content`, `type`, `is_read`, `created_at`; không có campaign recipient relation, `channels`, notification `status` hoặc `scheduled_at`.
- V1-PILOT notifications/deliveries dùng UUID và learner/delivery grain; không phải Admin notification model, không gộp vào legacy hoặc catalog ID.
- AC-36 #93 có recipients/segment/title/content/channels; #94 body và schedule không được định nghĩa. `NotificationChannel`, `NotificationStatus`, `AudienceSegment`, Admin permission policy và scheduler persistence chưa có nguồn đủ để xác nhận.
- Runtime/deployment chưa được kiểm tra; không chạy app tests cho task docs-only.

## SOURCE_TRACE

```text
Catalog #94 -> AC-36 UPDATE branch -> #92/#93 notification DDs + #95/#96 group neighbors -> legacy/pilot schema candidates -> Study routes/views/middleware
```

## API REQUIREMENT MATRIX

| ID | Method/path | Actor/auth | Direct request | Direct response/success/errors | Business intent | Status |
|---|---|---|---|---|---|---|
| #94 | `PUT /api/v1/admin/notifications/{notification_id}` | Bearer JWT; Admin; AC permission required | Path `notification_id:int64!`; no direct body/query | `ApiEnvelope<Notification>`; 200 `DESIGN_RESOURCE_UPDATED`; exact 401/403/404/422/500 catalog codes | AC-36 UPDATE Notification then reload management | Direct contract; editable fields/eligibility unresolved |

## REQUEST USAGE MATRIX

| Input | Direct source/use | Proposal or validation | Query/mutation use | Gap/status |
|---|---|---|---|---|
| `Authorization` | Bearer JWT; Admin role | Notification-management permission from AC-36 | Principal for authorization/audit actor | Claim, policy, scope and actor column `SOURCE_REQUIRED` |
| `notification_id` | Required path `int64` | Integer parse required by type; positive range not stated | Locate target Notification | Physical relation and missing-target precedence unresolved |
| Query | None declared | No query field inferred | None | Direct N/A |
| Body fields | None in catalog/diagram | `DERIVED` proposal: full replacement of recipients-or-segment, title, content, channels, scheduled_at to make UPDATE actionable and reuse #93 fields | Update Notification logical record; replace recipient association only when audience is supplied | Entire body and replacement semantics require owner confirmation |
| Editable lifecycle | Diagram title says draft/scheduled conditionally; no explicit status values | `DERIVED` proposal: allow conceptual Draft/Scheduled targets only; null schedule means Draft, future schedule means Scheduled; dispatched/cancelled target rejected using existing 422 | Guard before writes; scheduler effects not claimed | Enum/state transitions/clock/timezone and scheduler API `SOURCE_REQUIRED` |

## QUERY MATRIX

| Query ID | Purpose | Physical source/columns | Predicate/order | Status |
|---|---|---|---|---|
| Q1 | Resolve target notification | No approved Admin campaign table; legacy row is only an incompatible candidate | Match logical `notification_id`; editability predicate depends on unknown status model | `SOURCE_REQUIRED`; do not publish SQL |
| Q2 | Validate/replace explicit recipients or expand segment | No approved campaign-recipient relation or audience predicate | Exactly one selector is a `DERIVED` proposal; element, duplicate, and segment rules unresolved | `SOURCE_REQUIRED` |

## MUTATION MATRIX

| ID | Logical operation | Candidate target | Fields | Transaction/failure | Mapping/status |
|---|---|---|---|---|---|
| M1 | Update notification metadata/schedule | No approved Admin persistence model; legacy `notifications` is partial only | Proposed `title`, `content`, `channels`, `scheduled_at` | Atomicity, audit, updated timestamp, state guard not specified by source | `07_table.md`; physical mapping `SOURCE_REQUIRED` |
| M2 | Replace audience recipient association | No compatible legacy relation; V1-PILOT delivery model is not interchangeable | Proposed `recipients[]` or `segment` | Transaction and behavior for existing deliveries unresolved | `08_notification_recipients_update.md`; `DERIVED` logical mutation, physical mapping `SOURCE_REQUIRED` |
| M3 | Reschedule queued work | No scheduler/queue source found | No direct physical fields or operation ID | Do not claim enqueue/cancel/retry side effect | `SOURCE_REQUIRED`; no invented table or error code |

## RESPONSE SOURCE MATRIX

| Response field | Direct type/source | Transform/null rule | Gap/status |
|---|---|---|---|
| `success` | Shared envelope | true on HTTP 200 | Envelope convention |
| `businessCode` | Catalog | `DESIGN_RESOURCE_UPDATED` | `DIRECT` |
| `message` | Envelope/application | Wording unspecified | `SOURCE_REQUIRED` |
| `meta` | Shared envelope | Exact shape follows API guidelines | `SOURCE_REQUIRED` |
| `traceId` | Shared request context | Propagate current trace convention | Convention; #94 route absent |
| `data.id` | `Notification.id:int64` | Target notification identity | Physical allocator/model unverified |
| `data.title` | Notification schema | Stored updated title only if body proposal approved | Body directness/persistence `DERIVED / SOURCE_REQUIRED` |
| `data.content` | Notification schema | Stored updated content only if body proposal approved | `DERIVED / SOURCE_REQUIRED` |
| `data.channels[]` | `NotificationChannel[]` | No token set/projection available | `SOURCE_REQUIRED` |
| `data.status` | `NotificationStatus` | No enum/transition source | `SOURCE_REQUIRED` |
| `data.read_at?` | Optional date-time | No mutation semantics specified | `SOURCE_REQUIRED`; do not change read state |
| `data.scheduled_at?` | Optional date-time | Proposed schedule value; omit/null behavior not approved | `DERIVED / SOURCE_REQUIRED` |
| `data.created_at` | Notification schema | Preserve existing value | Persistence source/precision unknown |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status/impact |
|---|---|---|
| Missing request body | Catalog/diagram path only; purpose says update draft/scheduled notification | `DISCREPANCY`; body proposal remains `DERIVED` |
| Lifecycle eligibility | Draft/scheduled intent without enum or transition table | `SOURCE_REQUIRED`; conceptual guard is proposed only |
| Audience persistence | #93 supports recipients/segment; legacy schema has one nullable `user_id`; no Admin association table | `DISCREPANCY`; logical update is not physical implementation mapping |
| Schema models | Legacy BIGINT model vs V1-PILOT UUID learner/delivery model | `DISCREPANCY`; keep models separate |
| Scheduler behavior | No schedule/queue storage or worker contract in reviewed sources | `SOURCE_REQUIRED`; no delivery side effect claimed |
| Notification fields | Channels/status/read_at/scheduled_at lack complete compatible physical source | `SOURCE_REQUIRED` |
| Authorization | AC-36 names permission; current Study Admin guard not verified | `UNWIRED / SOURCE_REQUIRED` |
| #93 Operation response | Notification-vs-Operation and ID bridge conflict remains open | Carry to AC-36 macro-review; #94 does not reconcile it |

## PLANNED_OUTPUT

- API folder: `apps/study-server/docs/dd/94_admin_notifications_update/`.
- Eight standard sheets: `00_Cover.md`, `01_Lich_su.md`, `02_Overview.md`, `03_Request.md`, `04_Response.md`, `05_Data_Mapping.md`, `06_Error.md`, `07_table.md`.
- Supplementary logical recipient update mapping: `08_notification_recipients_update.md`.
- Three reports: `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`.
- All proposed body/state/mutation details are marked `DERIVED` and require confirmation; preserve exact catalog response and errors.
- After creation, expected inventory: 94 DD folders; 9 missing (#95–#103); 82 complete standard report packages; source-programmed count stays 12/103 with 91 lacking route+view pair.
- Preserve AC-36 macro-review as pending until API #96 has a DD.
- No app tests, runtime changes, catalog, schema, diagram, or context page changes.

## PLAN STATUS

Plan complete before creation of the API #94 folder. All required matrices are recorded above. Next step is to author from the canonical eight Markdown templates and verify the complete package.

## VERIFICATION_RESULT

- Package: 12 Markdown files — eight standard sheets, one supplementary recipient-association mapping, and three reports.
- Template appendix: 9/9 sheets match the corresponding template-backed appendix from API #93 byte-for-byte.
- Front matter: 9/9 sheets carry dd_id `94` and `Draft — Needs Confirmation`.
- Contract: method/path/path type, no direct body/query, response, HTTP 200 and exact five catalog error codes are preserved; body/lifecycle proposal is labeled `DERIVED`.
- Static content checks: 2/2 JSON examples parse; 33 Markdown tables have consistent widths; code fences are balanced; 34 local links/anchors resolve; all files have final newlines and no trailing whitespace.
- Source scan: no API #94 route/module/test marker found in scoped `apps/study-server/app` and `tests`; `UNWIRED / NOT_FOUND` (static only).
- Inventory: 94 DD folders with all eight core sheet roles; 9 missing (#95–#103); 82/94 have all three standard reports. Static route+view source count remains 12/103; 91 lack that pair.
- No app tests, runtime/deployment checks or live DB checks were run. No application source, catalog, schema, diagram or context page was changed; context validator not applicable.

## HANDOFF

- Next API DD: #95, Admin notification delete/cancel.
- AC-36 macro-review remains pending until #96 has a DD.
- Keep the proposed body, audience replacement, Draft/Scheduled guard and schedule interpretation unapproved until owner confirmation.

## GROUP_MACRO_REVIEW

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` after API #96 DD was created; document-level cross-review covers #92–#96.
- Report: `apps/study-server/docs/dd/96_admin_notifications_status/AC-36_MACRO_REVIEW.md`.
- Findings: list response/cardinality remains unresolved; #93 Notification-vs-Operation, conditional Send and ID bridge remain unresolved; #94 body/schedule are DERIVED; #95 delete/cancel and delivery-start policy are SOURCE_REQUIRED; #96 aggregate intent is not represented in its direct Notification response. Shared Admin model, grain, enums and permission remain open.
- Application tests, runtime and live schema were not checked as part of this document review.
