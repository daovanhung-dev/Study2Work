---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
---

# Data Mapping

## Current source audit (2026-11-21)

The Draft mapping below describes the logical generic Operation contract. Current Study source implements only a notification-specific lookup: `notifications.operation_id` joined to `notification_deliveries`, grouped by UUID and filtered by authenticated `sender_id`/owner. It returns `NOTIFICATION_DISPATCH` and local `QUEUED`/`FAILED`/`SENT` projections. There is no generic Study `operations` table. The handler has 8 dedicated source-level HTTP tests; this does not verify live schema/deployment or approve the generic mapping.

## Flow xử lý data

1. Nhận Bearer JWT và path operation_id.
2. Xác thực caller theo Bearer JWT; Student/Mentor/Admin are supported and all are restricted to the authenticated owner.
3. Parse `operation_id` as UUID before querying the notification-specific operation view; malformed values return the existing 404 resource-not-found response.
4. Query the notification-specific operation view from `notifications` plus `notification_deliveries`; generic Operation storage remains unsupported.
5. Return ApiEnvelope<Operation> on success or one of the catalog-listed errors.

## Request Usage Matrix

| Request field | Nguồn | Data Mapping step | Validate | SQL/Mutation usage | Branch/Loop | Response usage | Gap |
|---|---|---|---|---|---|---|---|
| Authorization | Header; Bearer JWT per API #18 row | 0.1/0.2 | Current source allows Student/Mentor/Admin roles and reads authenticated subject | Query is owner-bound; no Admin ownership bypass | 0.3 | No direct response field | Other roles return 403; wrong-owner is hidden as 404 |
| operation_id | Path /api/v1/operations/{operation_id} | 1.1/1.2/2.1 | Required UUID | Query binds UUID against `notifications.operation_id` | 3.1/3.2 | data.id | UUID selected in the reconciled API row |

## Query Matrix

| Query ID | Mục đích | Type | Base table/view | Alias | Columns | JOIN | WHERE | GROUP/HAVING | ORDER | Pagination | Result variable | Branch |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | Read one notification Operation by supplied UUID and owner | SELECT | `notifications` + `notification_deliveries` | n/d | Operation UUID, sender/owner ID and channel statuses | `notification_deliveries.notification_id` | UUID and owner predicates from authenticated subject | Aggregate notification state | N/A | N/A | operation_record | Missing and non-owner rows return the same 404 response |

## Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|---|
| N/A | N/A — read-only | N/A | N/A | N/A | N/A | N/A | 07_table.md | N/A | No DB mutation is specified |

## Response Source Matrix

| Response field | Type | Source type | Table/column or generator | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| success | boolean | Branch constant | N/A | 5.1/5.2 | true on success; false on error | N/A | Envelope behavior is design-only |
| businessCode | string | Branch constant | DESIGN_OPERATION_RETRIEVED or catalog error code | 5.1/5.2 | Fixed by branch | N/A | Codes are design-only |
| message | string | Branch message | SOURCE_REQUIRED | 5.1/5.2 | No literal defined | SOURCE_REQUIRED | Do not invent message text |
| data.id | UUID | Notification operation group | `notifications.operation_id` | 4.1/5.1 | Direct; equals requested UUID | Required on success | Current notification source |
| data.kind | string | Derived notification group | Literal `NOTIFICATION_DISPATCH` | 4.1/5.1 | Fixed for this handler | Required on success | Not a generic enum registry |
| data.status | string | `notification_deliveries.status` | Aggregate `QUEUED`/`FAILED`/`SENT` | 4.1/5.1 | Queued takes precedence, then failed, else sent | Required on success | Current notification state projection |
| data.owner_id | int64 | Notification Operation | `notifications.sender_id` | 4.1/5.1 | Direct mapping from authenticated sender | Required on success | Owner-only lookup; no Admin bypass |
| data.submitted_at | date-time | Notification group | `MIN(notifications.created_at)` | 4.1/5.1 | ISO-8601 | Required on success | Current notification group timestamp |
| data.updated_at | date-time | Notification/outbox group | `MAX(COALESCE(delivery.updated_at, notification.created_at))` | 4.1/5.1 | ISO-8601 | Required on success | Current notification projection |
| data.completed_at | date-time, optional | Notification/outbox group | Same aggregate timestamp when no delivery remains queued | 4.1/5.1 | ISO-8601 | Omitted while queued | Current notification terminal-state rule |
| data.result | optional Payment in reusable schema | N/A for notification projection | Omitted (`None`, excluded from current source response) | 4.1/5.1 | No notification result mapping | Omitted | Generic per-kind result remains unresolved |
| meta | object | Envelope default | N/A | 5.1/5.2 | Illustrative empty object | Shape unspecified | |
| traceId | UUID | Shared envelope | Current trace context/generator | 5.1/5.2 | Shared schema type | Required by reusable schema | API #18 runtime behavior not verified |

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Require Bearer JWT per API #18 catalog row.
- Supported roles are Student, Mentor and Admin.
- Every role is owner-only; Admin has no ownership bypass.
- Current source uses the authenticated numeric subject as the owner predicate.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Operation logical resource | owner_id | Compare to authenticated numeric JWT subject | Current notification query owner-binds the lookup for all supported roles |
| Bearer JWT | caller identity/role claims | Require Student, Mentor or Admin | Other roles are rejected before DB access |

### 0.3. Check kết quả

- Missing or invalid Bearer JWT maps to HTTP 401 / DESIGN_AUTHENTICATION_REQUIRED per catalog.
- A role outside Student/Mentor/Admin maps to HTTP 403 / DESIGN_ACCESS_DENIED.
- Missing and non-owner notification operations both map to 404 / DESIGN_RESOURCE_NOT_FOUND.

## 1. Validate data input

### 1.1. Get request path

- operation_id: read from path /api/v1/operations/{operation_id}.
- No query parameter or request body is declared.

### 1.2. Validate operation_id

- The API #18 row, current OpenAPI source, reusable Operation.id and AC diagrams use UUID.
- Current source parses a UUID before querying the notification Operation view.
- Do not apply numeric range, UUID version, case normalization or other constraints absent from the canonical contract.

## 2. Get thông tin

### 2.1. Query

- Logical operation: retrieve the Operation identified by operation_id.
- Current notification query reads `notifications` and `notification_deliveries`; the physical schema is a checked-in legacy candidate and live schema is unverified. Generic operation tables are not implemented.
- Study DB.sql, DB_UNICA_TABLES.md and DB_UNICA_ERD.drawio do not define an Operation table.
- The similarly named Work Server table is tied to work_users and is not a confirmed Study API backing store.

### 2.2. JOIN

| Target table | Join condition | Join type |
|---|---|---|
| `notification_deliveries` | `notification_deliveries.notification_id = notifications.id` | LEFT JOIN |

### 2.3. WHERE

- `notifications.operation_id` matches the supplied UUID and `notifications.sender_id` matches the authenticated numeric subject.

### 2.4. ORDER BY

- N/A — single logical resource lookup; physical query is not defined.

## 3. Insert/Update thông tin

### 3.1. Target table

- N/A — READ-ONLY API.

### 3.2. Conditions

- N/A — READ-ONLY API; no mutation predicate.

### 3.3. Items update/insert

- N/A — READ-ONLY API; see 07_table.md.

### 3.4. Parameters

- N/A — READ-ONLY API; no mutation parameters.

## 4. Check kết quả execute query

### 4.1. Thành công

- When an authorized Operation is resolved, return HTTP 200 / DESIGN_OPERATION_RETRIEVED.
- Map the logical fields listed in 04_Response.md.
- Optional field presence and per-kind result mapping remain unresolved.

### 4.2. Lỗi hệ thống

- Query or unexpected processing failure maps to HTTP 500 / DESIGN_INTERNAL_ERROR per catalog.
- Do not return raw SQL, stack traces or internal database detail.

### 4.3. Validate lỗi

- Missing/invalid authentication maps to HTTP 401 / DESIGN_AUTHENTICATION_REQUIRED.
- Access denial maps to HTTP 403 / DESIGN_ACCESS_DENIED.
- Current source maps a malformed UUID path to 404; no extra status code is added.

### 4.4. Ngoài trường hợp trên

- If the Operation does not exist, the catalog lists HTTP 404 / DESIGN_RESOURCE_NOT_FOUND.
- A notification operation not owned by the caller returns the same 404 as a missing operation, as selected for SH-07.
- Keep the API DD in Draft for generic lifecycle, result and non-notification producer questions.

> API read-only không có BEGIN TRANSACTION, COMMIT hoặc ROLLBACK.

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/05_Data_Mapping.md.
- Sheet logic: 3. Data mapping.
