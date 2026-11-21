# PLAN_RESULT — Study API #44

DD folder: apps/study-server/docs/dd/44_notifications_mark_read/.
Status: Draft — Needs Confirmation.
Runtime `status`: `UNWIRED` / `NOT_FOUND`.

## Kết quả

- API #44 — `PATCH` `/api/v1/notifications/{notification_id}/read`; `Student` `Bearer` `JWT`; path `notification_id`:`int64`!.
- Response `ApiEnvelope<Page<Notification>>`; `HTTP` 200 `DESIGN_RESOURCE_UPDATED`; errors 401/403/404/422/500 đúng catalog.
- Runtime `UNWIRED` / `NOT_FOUND`; DD Draft — Needs Confirmation.
- AC-20 ONE branch → API #44 → update recipient read state → UI update.
- Physical candidate `UPDATE` `notifications`.`is_read`=`TRUE` chỉ cho row của principal. Đây là `DERIVED` vì diagram yêu cầu `NotificationRecipient`.`read_at`.
- Đã tạo 8 template sheets và sẽ kèm 3 Markdown reports. Response còn `SOURCE_REQUIRED` do schema thiếu field.

## Input Manifest và Coverage

| ID | Source | Đơn vị đã đọc | Trạng thái |
|---|---|---|---|
| S1 | AGENTS.md, .agents/AGENTS.md, context-map.md | Router, map, scope boundary | VERIFIED |
| S2 | Worklog README/TEMPLATE và selector-chọn #41–#43 | Preflight, carry-forward | VERIFIED |
| S3 | server-study AGENTS/INDEX/workflow/declared routes | Study boundary, Markdown-only | VERIFIED |
| S4 | context manifest, skill index và createDD-markdown | Skill wiring, authoring/validation gates | VERIFIED |
| S5 | DD_API_Template_MD/00–07 | 8 template files, hash and heading/fm | VERIFIED |
| S6 | list_api.md | APIs #43–#45 and reusable `Page`/`Notification` schemas | VERIFIED |
| S7 | AC index + all AC-20 diagram nodes/edges | ONE branch, mutation node and UI node | VERIFIED |
| S8 | DB table guide, ERD and checked-in DDL | `notifications` fields/relation and missing recipient/`read_at` | VERIFIED |
| S9 | API guidelines and current route/auth/response source | Envelope, `Idempotency-Key` note, helper discrepancy, no #44 route | VERIFIED |
| S10 | API #42/#43 and #40/#41 DD precedents | Singleton `Page` and mutation mapping pattern | VERIFIED |
| S11 | Archive search in Study docs/app/schema/skill scope | ZIP/XLSX/XLSM | None found |

## API Requirement Matrix và các ma trận trước authoring


### API Requirement Matrix

| API ID | Name | Method / endpoint | Actor / auth | Request field | Response / `success` | Errors |
|---|---|---|---|---|---|---|
| #44 | Đánh dấu một thông báo đã đọc (`Conditional`) | ``PATCH` `/api/v1/notifications/{notification_id}/read`` | ``Student`` / `Bearer` ``JWT`` | ``Authorization`` | ``ApiEnvelope<Page<Notification>>``; `HTTP` 200 ``DESIGN_RESOURCE_UPDATED`` | 401 ``DESIGN_AUTHENTICATION_REQUIRED``; 403 ``DESIGN_ACCESS_DENIED``; 404 ``DESIGN_RESOURCE_NOT_FOUND``; 422 ``DESIGN_VALIDATION_ERROR``; 500 ``DESIGN_INTERNAL_ERROR`` |
| #44 | Đánh dấu một thông báo đã đọc (`Conditional`) | Same | Same | ``notification_id`:`int64`!` path | Same contract | Same catalog error set only |

### Request Usage Matrix

| Request field | Source | Validation / normalization | SQL or branch use | Response use | Gap |
|---|---|---|---|---|---|
| ``Authorization`` | `HTTP` header | `Bearer`/`JWT`; require `Student`; take principal ID from token | Owner predicate `n.`user_id`=:`principal_id`` | Never echo token/user ID | API #44 has no route; shared helper exists. |
| ``notification_id`` | Required path ``int64`` | Parse as `int64`; invalid/out-of-range follows declared 422; do not add an unsupported positivity rule | Target `n.id=:`notification_id`` | ``data`.`items`[0].id` from returned row | Ownership and broadcast recipient model unresolved. |

### Query Matrix

| ID | Purpose | Type | Base table / alias | Column / condition | Value source | Result / branch | Evidence `status` |
|---|---|---|---|---|---|---|---|
| M1 | Mark the owned notification as read and return its display projection | ``UPDATE` ... `RETURNING`` | ``notifications` AS n` | `SET n.`is_read`=`TRUE`` | AC-20 action mapped to existing boolean read flag | Updated notification row | ``DERIVED``; diagram instead says ``read_at``. |
| M1 | Same | `WHERE` | ``notifications` AS n` | `n.id=:`notification_id`` | Path | Require one target row | Direct key + request contract |
| M1 | Same | `WHERE` | ``notifications` AS n` | `n.`user_id`=:`principal_id`` | Authenticated `Student` principal | Prevent cross-user update; no matching row maps to 404 | ``DERIVED`` from recipient-per-user diagram; nullable/broadcast rows excluded |
| M1 | Same | ``RETURNING`` | ``notifications` AS n` | `id` | Updated row | `notification_row.id` | Direct candidate |
| M1 | Same | ``RETURNING`` | ``notifications` AS n` | ``title`` | Updated row | `notification_row.`title`` | Direct candidate |
| M1 | Same | ``RETURNING`` | ``notifications` AS n` | ``content`` | Updated row | `notification_row.`content`` | Direct candidate |
| M1 | Same | ``RETURNING`` | ``notifications` AS n` | ``created_at`` | Updated row | `notification_row.`created_at`` | Candidate; timezone unresolved |

### Mutation Matrix

| ID | Operation | Target | Changed column | Value | Transaction / failure |
|---|---|---|---|---|---|
| M1 | Mark read | ``notifications`` | ``is_read`` | ``TRUE`` | One atomic statement in caller-owned transaction; commit when matched, no `data` change on 404, rollback on DB failure. No ``read_at`` column exists. |

The M1 row conditions are recorded separately in Query Matrix (`id=:`notification_id`` and ``user_id`=:`principal_id``), one condition per row.

### Response Source Matrix

| Response field | Contract type | Candidate source / transform | Null / `page` rule | Status |
|---|---|---|---|---|
| ``success`` | boolean | Fixed `true` | Required | Direct envelope convention |
| ``businessCode`` | string | ``DESIGN_RESOURCE_UPDATED`` | Required | Direct catalog |
| ``message`` | string | Safe `message` | Literal not specified | Needs wording only |
| ``data`.`items`[]` | `Notification`[] | One updated row from M1 | Exactly one item on matched `success` | ``DERIVED`` singleton `page` proposal, API #42 precedent |
| ``data`.`items`[].id` | `int64` | `notification_row.id` | Required | Direct candidate |
| ``data`.`items`[].`title`` | string | `notification_row.`title`` | Required | Direct candidate |
| ``data`.`items`[].`content`` | string | `notification_row.`content`` | Required | Direct candidate |
| ``data`.`items`[].`channels`` | ``NotificationChannel`[]` | No physical source; do not map `type` | Required by schema | ``SOURCE_REQUIRED`` |
| ``data`.`items`[].`status`` | ``NotificationStatus`` | No physical source; do not infer enum/read-state meaning | Required by schema | ``SOURCE_REQUIRED`` |
| ``data`.`items`[].`read_at`` | date-time? | Diagram target has no DDL source; do not derive timestamp | Optional/omission rule open | `DISCREPANCY / `SOURCE_REQUIRED`` |
| ``data`.`items`[].`scheduled_at`` | date-time? | No physical source | Optional/omission rule open | ``SOURCE_REQUIRED`` |
| ``data`.`items`[].`created_at`` | date-time | `notification_row.`created_at`` | Required; timezone rule open | ``SOURCE_REQUIRED`` for timezone |
| ``data`.`pagination`.`page`` | int32 | Fixed 1 | Singleton `page` | ``DERIVED`` |
| ``data`.`pagination`.`size`` | int32 | Fixed 1 | Singleton `page` | ``DERIVED`` |
| ``data`.`pagination`.`total`` | `int64` | Fixed 1 | One updated resource | ``DERIVED`` |
| ``data`.`pagination`.`total_pages`` | int32 | Fixed 1 | One updated resource | ``DERIVED`` |
| ``meta`` | object | Empty metadata | `{}` | Envelope convention |
| ``traceId`` | uuid | Current request trace | Required | Shared convention; endpoint unwired |

### Planned DD structure and review boundary

1. Preserve API #44 catalog method/path/actor/path field/response/`status`/error set exactly.
2. Trace the AC-20 `ONE` edge: API #44 then ``UPDATE` `read_at` cho notification recipient`, then UI badge/read-state update. Preserve this logical target as expected behavior.
3. Because current physical design has only ``notifications`.`is_read``, propose a single atomic ``UPDATE` ... SET `is_read`=`TRUE` WHERE id=:`notification_id` AND `user_id`=:`principal_id` `RETURNING` ...` as a simple physical candidate. Mark the mismatch with logical ``NotificationRecipient`.`read_at``; do not add a table or column. Treat no owner-matching row (missing, other user, or broadcast with ``user_id` IS NULL`) as 404 to avoid exposing another user's notification. Repeating the state assignment is idempotent.
4. Do not add a body, query, user ID, `status` field, or undocumented error code. Map invalid `int64` syntax/range to the catalog's 422; a well-formed ID with no owner-matching row maps to catalog 404.
5. Use API #42's single-resource ``Page`<T>` precedent to propose one updated notification in a one-item `page` (``page`=1,`size`=1,`total`=1,`total_pages`=1`), all labeled ``DERIVED``. The response still cannot be fully populated because required ``channels``/``status`` have no source; ``read_at`` also conflicts with DDL. Preserve those gaps as ``SOURCE_REQUIRED`` and open questions. Later API #45 must use consistent read-state and response semantics.
6. Build the request, mutation/query, response, error, and `07_notifications_mark_read.md` mappings; one request field, SQL field/condition and error case per row. Keep the whole DD `Draft — Needs Confirmation`.
7. Create eight template sheets plus `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md` only under `apps/study-server/docs/dd/44_notifications_mark_read/`; no ZIP/runtime/schema/catalog/diagram edits.
8. Immediately verify the exact file set, front matter, API contract/`status`/errors, AC-20 trace, one-field/condition/error-per-row matrices, `JSON`, Markdown, local links, code fences, and source `status`. Update API #43 only if review finds a concrete contradiction; keep broader AC-20 macro review for API #45's DD session.
