---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

1. Nhận Bearer JWT và path operation_id.
2. Xác thực caller theo Bearer JWT; caller-to-owner authorization rule còn có discrepancy.
3. Parse operation_id only after contract owner selects int64 or UUID.
4. Resolve Operation from an approved Study storage/query source; that source is SOURCE_REQUIRED.
5. Return ApiEnvelope<Operation> on success or one of the catalog-listed errors.

## Request Usage Matrix

| Request field | Nguồn | Data Mapping step | Validate | SQL/Mutation usage | Branch/Loop | Response usage | Gap |
|---|---|---|---|---|---|---|---|
| Authorization | Header; Bearer JWT per API #18 row | 0.1/0.2 | Authentication required; token claims and owner mapping are not specified here | Caller identity is needed for authorization; physical predicate is SOURCE_REQUIRED | 0.3 | No direct response field | Keep 401/403 contract; see Q-18-02 |
| operation_id | Path /api/v1/operations/{operation_id} | 1.1/1.2/2.1 | Required; accepted scalar type conflicts between int64 and UUID sources | Logical lookup by Operation ID is DERIVED; physical query/column is SOURCE_REQUIRED | 3.1/3.2 | data.id | See Q-18-01 |

## Query Matrix

| Query ID | Mục đích | Type | Base table/view | Alias | Columns | JOIN | WHERE | GROUP/HAVING | ORDER | Pagination | Result variable | Branch |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | Read one Operation by supplied identifier | Logical SELECT only | SOURCE_REQUIRED — no Study physical table/view identified | N/A | Logical Operation fields from list_api.md; physical columns SOURCE_REQUIRED | N/A — no relation is specified | Logical Operation ID match is DERIVED; physical predicate SOURCE_REQUIRED | N/A | N/A | N/A | operation_record | If source returns a record, map response; absent record follows 404 contract; ownership rule remains unresolved |

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
| data.id | UUID in reusable schema | Logical Operation | Physical source/column SOURCE_REQUIRED | 4.1/5.1 | Direct logical field | Required on success | Path ID type conflict |
| data.kind | OperationKind | Logical Operation | Physical source/column SOURCE_REQUIRED | 4.1/5.1 | Direct logical field | Required on success | Enum values unresolved |
| data.status | OperationStatus | Logical Operation | Physical source/column SOURCE_REQUIRED | 4.1/5.1 | Direct logical field | Required on success | Enum values/lifecycle unresolved |
| data.owner_id | int64 | Logical Operation | Physical source/column SOURCE_REQUIRED | 4.1/5.1 | Direct logical field | Required on success | Caller ownership rule unresolved |
| data.submitted_at | date-time | Logical Operation | Physical source/column SOURCE_REQUIRED | 4.1/5.1 | ISO-8601 | Required on success | Source/precision unresolved |
| data.updated_at | date-time | Logical Operation | Physical source/column SOURCE_REQUIRED | 4.1/5.1 | ISO-8601 | Required on success | Lifecycle unresolved |
| data.completed_at | date-time, optional | Logical Operation | Physical source/column SOURCE_REQUIRED | 4.1/5.1 | ISO-8601 | Optional; null/omission policy unresolved | |
| data.result | optional Payment in reusable schema | Logical Operation | Physical source/column SOURCE_REQUIRED | 4.1/5.1 | Direct logical field | Optional | Per-kind result conflict |
| meta | object | Envelope default | N/A | 5.1/5.2 | Illustrative empty object | Shape unspecified | |
| traceId | UUID | Shared envelope | Current trace context/generator | 5.1/5.2 | Shared schema type | Required by reusable schema | API #18 runtime behavior not verified |

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Require Bearer JWT per API #18 catalog row.
- The catalog row names the Operation owner as the actor.
- The operation-tracking summary permits owner or Admin.
- AC diagrams list Student, Mentor and Admin with owner-only access.
- Caller identity claim mapping and any Admin override are unresolved; see OPEN_QUESTIONS.md.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Operation logical resource | owner_id | Compare to authenticated caller only after the identity mapping is approved | Physical table, owner column and Admin policy are SOURCE_REQUIRED |
| Bearer JWT | caller identity/role claims | Authentication required; exact claim names are not specified by API #18 contract | Current runtime behavior is not evidence for this unwired endpoint |

### 0.3. Check kết quả

- Missing or invalid Bearer JWT maps to HTTP 401 / DESIGN_AUTHENTICATION_REQUIRED per catalog.
- Access denial maps to HTTP 403 / DESIGN_ACCESS_DENIED per catalog.
- Whether non-owner access returns 403 or is hidden as 404 is unresolved.
- Do not infer Admin bypass from role presence alone.

## 1. Validate data input

### 1.1. Get request path

- operation_id: read from path /api/v1/operations/{operation_id}.
- No query parameter or request body is declared.

### 1.2. Validate operation_id

- The API #18 row declares int64.
- Catalog convention, reusable Operation.id and AC diagrams declare UUID.
- Keep parse/format validation SOURCE_REQUIRED until one accepted type is approved.
- Do not apply numeric range, UUID version, case normalization or other constraints absent from the canonical contract.

## 2. Get thông tin

### 2.1. Query

- Logical operation: retrieve the Operation identified by operation_id.
- Physical table, columns, query implementation and live schema are SOURCE_REQUIRED.
- Study DB.sql, DB_UNICA_TABLES.md and DB_UNICA_ERD.drawio do not define an Operation table.
- The similarly named Work Server table is tied to work_users and is not a confirmed Study API backing store.

### 2.2. JOIN

| Target table | Join condition | Join type |
|---|---|---|
| N/A | N/A | No join is specified by the contract |

### 2.3. WHERE

- Logical Operation identifier matches the supplied operation_id — DERIVED from the resource endpoint and Operation schema.
- Physical predicate and owner predicate are SOURCE_REQUIRED.

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
- Do not add a path validation status code while operation_id type is unresolved.

### 4.4. Ngoài trường hợp trên

- If the Operation does not exist, the catalog lists HTTP 404 / DESIGN_RESOURCE_NOT_FOUND.
- Whether an ownership failure is also represented by 404 is SOURCE_REQUIRED.
- Keep the API in Draft until the open questions are resolved.

> API read-only không có BEGIN TRANSACTION, COMMIT hoặc ROLLBACK.

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/05_Data_Mapping.md.
- Sheet logic: 3. Data mapping.
