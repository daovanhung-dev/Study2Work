---
task_id: "2026-10-24-create-study-api64-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "IN_PROGRESS"
---

# Worklog: Tạo DD Study API #64 — Theo dõi trạng thái gửi

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ phân biệt direct contract với candidate schema; API read-only dùng N/A mutation; không xem DDL candidate là live.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Dùng requirement/request/query/mutation/response matrices; chỉ ghi suy diễn là DERIVED; không invent query/schema.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: AC-22/33 có các điểm mở; preserve source gaps và macro-review theo nhóm khi đủ DD.
- shortage: `none`
- Additional related DDs reviewed: #18, #43, #45, #62, #63; API #64 thuộc AC-25 và operation handoff #18.

## EXPECTED_BEHAVIOR

- Requirement: Tạo một DD Markdown tiếng Việt cho API #64 trong phiên này; lập plan và ma trận trước khi tạo thư mục DD; đọc kỹ toàn bộ flow AC-25; giữ contract trực tiếp và nêu discrepancy với schema/source; kiểm tra tĩnh sau authoring; khi #64 hoàn tất, macro-review nhóm #62–#64 cùng API #18.
- Canonical contract `docs/lists/list_api.md` row #64: `GET /api/v1/mentor/notifications/{notification_id}/status`; Bearer JWT, role Mentor; path `notification_id:int64!`; không khai báo body/query; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Operation>`; lỗi đúng 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`.
- AC-25 diagram direct flow: Mentor chọn course/soạn thông báo → #62 đọc active enrollments → chọn recipients/title/content → #63 tạo Notification + recipients → Push/Email → #64 đọc delivery status → UI hiển thị. Node generic API #18 có trong diagram nhưng không có edge nối với flow.

## CURRENT_BEHAVIOR

- Source/config: Không tìm thấy route `/api/v1/mentor/notifications/{notification_id}/status`, module API #64, query hoặc test/provider delivery trong `apps/study-server/app` và `tests`. `DESIGN_CONTRACT_PATHS` không chứa path; chưa có runtime để kiểm chứng.
- DB artifacts: Legacy Study `notifications` dùng BIGSERIAL, `user_id`/`sender_id`, `is_read`; không có delivery row/status/channel hay Study Operation table. V1-PILOT có notifications UUID theo `learner_id` và append-only `notification_deliveries` UUID, `channel=IN_APP|EMAIL`, `status=QUEUED|SENT|DELIVERED|FAILED|SUPPRESSED`; đây là model thay thế, không phải live schema, và không khớp path ID int64.
- Contract conflict: API #64 nhận `notification_id:int64` và trả Operation; reusable `NotificationDelivery` có `notification_id:int64`, `status:OperationStatus`, `queued/sent/failed`; reusable `Operation.id` là UUID và `result?:Payment`. Chưa có mapping giữa delivery record, operation, hay ID do #63 trả.
- Runnable tests: Không chạy; docs-only. Không có test API #64.
- Related flow: #63 trả Operation nhưng không nêu `notification_id`; #62 trả `Page<Course>` dù diagram cần roster học viên. #43/#45 là read-state, không phải delivery status.

## SOURCE_TRACE

```text
Mentor Bearer principal -> GET status theo notification_id:int64 -> xác thực quyền xem notification -> logical SELECT delivery state -> map response theo catalog Operation -> HTTP 200/401/403/404/500; storage, authorization relation và response mapping chưa có runtime source
```

## PLAN BEFORE DD AUTHORING

1. Giữ nguyên contract #64: GET/path ID int64/Mentor Bearer/no body or query/200 `DESIGN_RESOURCE_RETRIEVED`/`ApiEnvelope<Operation>` và đúng bốn lỗi 401/403/404/500. Không thêm filter, status code hay request field.
2. Bám mọi node/edge AC-25; #64 đọc trạng thái delivery sau Push/Email. Ghi API #18 là operation-job polling riêng, đang detached trong diagram và có xung đột ID type; không nhập hai flow.
3. Đối chiếu #62/#63 để nêu end-to-end gap: #62 roster projection và pagination thiếu; #63 recipient encoding/course scope chưa rõ; #63 response không đưa notification_id cho #64. Đối chiếu #18 cho Operation persistence/result/owner, #43/#45 để tách read-state khỏi delivery state.
4. Q1 chỉ mô tả logical read theo notification ID và access scope. Không viết SQL/physical query: legacy DDL không lưu delivery state; pilot delivery UUID model không khớp int64 path và chưa chứng minh live.
5. Giữ authorization relation `SOURCE_REQUIRED`; khuyến nghị đơn giản (nếu đưa ra) phải gắn `DERIVED`, không tự áp dụng owner/sender predicate từ candidate `sender_id`.
6. Response matrix liệt kê toàn bộ field reusable `Operation`, gồm nested Payment fields theo schema nhưng đánh dấu không map được cho delivery. Nêu `NotificationDelivery` schema gần với intent nhưng khác response contract; giữ cả hai direct contract và đề xuất sửa contract ở trạng thái DERIVED/open.
7. Phân biệt `notification_id:int64` với `operation_id:uuid`; không dùng `notifications.is_read` làm trạng thái gửi; không gộp `NotificationStatus`, `OperationStatus`, `notification_status` nếu enum semantics chưa được xác nhận.
8. Tạo 8 sheet + `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`; sheet DB prototype ghi `N/A — READ-ONLY API`. Không ZIP, code, schema, catalog hay diagram edits.
9. Static verify exact 11-file manifest, front matter, template fingerprints/appendix byte equality, exact catalog request/response/error contract, JSON, field coverage, relative paths/anchors, table widths, fences, whitespace và `git diff --check`. Runtime tests `NOT_RUN`.
10. Sau khi #64 pass static checks, macro-review #62–#64 và #18 handoff; cập nhật report/worklog của nhóm, giữ các conflict chưa có nguồn ở trạng thái open.

### API Requirement Matrix — plan gate

| API ID | Method/path | Actor/auth | Input | Success/response | Errors | Status |
|---|---|---|---|---|---|---|
| #64 | `GET /api/v1/mentor/notifications/{notification_id}/status` | Bearer JWT; Mentor | `notification_id:int64!`; no body/query | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Operation>` | 401 authentication; 403 access; 404 resource not found; 500 internal | Catalog DIRECT; delivery/Operation mapping and handoff unresolved |

### Request Usage Matrix — plan gate

| Request item | Contract source/use | Mapping/query use | Evidence/gap |
|---|---|---|---|
| Authorization | Required Bearer JWT; Mentor role | Principal for notification access scope | Role DIRECT; claim, numeric ID and ownership relation SOURCE_REQUIRED |
| `notification_id` | Required path int64 | Logical delivery lookup and response identity | Type DIRECT; legacy ID candidate is BIGINT, pilot ID is UUID; live source absent |
| Body/query | None | None | DIRECT from catalog |

### Query Matrix — plan gate

| Query | Type/target | Purpose | Status |
|---|---|---|---|
| Q1 | Logical SELECT notification + delivery state | Find requested notification, authorize Mentor, read delivery summary | Physical table/columns and authorization predicate SOURCE_REQUIRED; legacy lacks delivery, pilot UUID model conflicts |
| Q2 | Optional aggregate of delivery state | Derive status and queued/sent/failed counts | Not approved: pilot rows are attempts without recipient ID; do not count attempts as recipients |

### Mutation Matrix — plan gate

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | GET read-only | No INSERT/UPDATE/DELETE/provider call specified | `N/A — READ-ONLY API` |

### Response Source Matrix — plan gate

| Response field | Contract | Candidate source/transform | Status |
|---|---|---|---|
| Envelope | `ApiEnvelope<Operation>` | Shared schema/catalog | DIRECT shape; message/meta/null policy partly unresolved |
| `data.id` | UUID | Operation | Schema DIRECT; no Study operation store or mapping from int64 notification ID |
| `data.kind/status/owner_id/timestamps` | Operation fields | Operation record | Schema DIRECT; values/source/lifecycle/owner mapping SOURCE_REQUIRED |
| `data.result?:Payment` | Optional Payment | Operation schema | Direct reusable schema but unrelated to notification delivery |
| `NotificationDelivery` | notification_id:int64, status:OperationStatus, queued/sent/failed | Reusable schema | Intent-aligned candidate, not #64 direct response; counts/status semantics unresolved |
| `traceId` | UUID | Shared envelope | Convention DIRECT; runtime behavior absent for #64 |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #64 runtime | Current Study router/module/test/provider scan | `UNWIRED / NOT_FOUND` | Design-only; no runtime behavior claim |
| Delivery storage | Legacy `notifications` has only `is_read`; pilot deliveries use UUID/attempt rows | `DISCREPANCY / SOURCE_REQUIRED` | Cannot approve physical query or counts |
| Response shape | AC asks for delivery status; row returns Operation; NotificationDelivery is separate reusable schema | `DISCREPANCY` | Client contract does not expose a clear delivery summary |
| ID handoff | #63 returns Operation UUID; #64 takes notification int64; no response mapping links them | `SOURCE_REQUIRED / AC-25 BLOCKER` | Client cannot reliably invoke status lookup after creation |
| Authorization | Catalog role Mentor; no ownership/course/notification relation specified | `SOURCE_REQUIRED` | Cannot finalize permission query or 403/404 order |
| Read state | #43/#45 + legacy `is_read` concern reading; diagram #64 concerns delivery | `DISCREPANCY IF REUSED` | Must not treat read receipt as send status |

## CHANGES

- Files changed: This worklog before DD creation; DD #64 folder is not created yet.
- CONTEXT_UPDATES: None planned; no source/schema/catalog/diagram/context page edits.
- Context pages changed: None planned.
- Assumptions: Keep direct contract authoritative; record any simplest proposal as DERIVED and require confirmation; no invented physical query.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector/review | Selected #48/#49/#50; all three read; shortage none. | `VERIFIED` |
| Context and skill registry | Root/global map, Study scope/workflow, `createDD-markdown` registry entry and skill read. | `VERIFIED_STATIC_ONLY` |
| AC-25 diagram | All nodes/edges read; #18 node exists without edge. | `VERIFIED_STATIC_ONLY` |
| Catalog and reusable schemas | Rows #18/#62–#64, Operation, NotificationDelivery and error contracts read. | `VERIFIED_STATIC_ONLY` |
| Prior DDs | #18/#43/#45/#62/#63 inspected for operation, read state and connected Mentor flow. | `VERIFIED_STATIC_ONLY` |
| Current source/DB | No #64 runtime source; legacy/pilot discrepancy recorded; live schema not verified. | `VERIFIED_STATIC_ONLY` |
| DD authoring/static verification | Pending until after plan gate and authoring. | `IN_PROGRESS` |

## HANDOFF

- Remaining blockers: NotificationDelivery physical mapping/status aggregation, notification ownership predicate, Operation result/persistence, and #63-to-#64 ID handoff.
- Next owner/action: Finish API #64 DD and static verification, then macro-review the complete AC-25 group #62–#64 with API #18.
