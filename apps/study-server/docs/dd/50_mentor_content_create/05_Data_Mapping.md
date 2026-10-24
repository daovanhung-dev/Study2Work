---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "50"
api_name: "Tạo nội dung mới Conditional"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
1. Nhận Bearer JWT và body {course_id, content_type, title, payload} theo catalog #50.
2. AuthN/AuthZ: yêu cầu role Mentor và quyền quản lý course (AC-22). Identity binding/assigned-course relation chưa có trong Study source.
3. Validate required/type contract. Enum ContentType và schema payload chưa có nguồn; không áp đặt field/max-length riêng.
4. Candidate course lookup/owner check có thể dùng legacy courses.id/mentor_id nhưng chỉ DERIVED; không dùng làm live assertion.
5. Logical INSERT Content theo AC-22. AC-33 cho biết queue review chứa status=PENDING_REVIEW; suy ra trạng thái khởi tạo của POST là đề xuất DERIVED, chưa được AC-22 ghi trực tiếp. Content physical table/model chưa được duyệt.
6. Candidate defaults do request không nhận parent_id/order: root parent_id=null và order nối tiếp trong root siblings của course; DERIVED, cần confirmation.
7. Map mọi field Content và envelope; id generation, physical projection, payload schema và storage chưa được xác nhận.
8. Trả 201 DESIGN_RESOURCE_CREATED. AC-22 sau đó reload cây; API #50 hiện UNWIRED/NOT_FOUND.
~~~

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Authentication là Bearer JWT và role Mentor theo catalog.
- AC-22 precondition yêu cầu Mentor có quyền quản lý course.
- Không nhận `mentor_id`, principal ID hoặc quyền từ body.
- Legacy `courses.mentor_id` có thể là candidate direct-owner relation; không bao gồm course assignment và chưa có principal mapping. Không coi đây là rule đã duyệt.

### 0.2. Query/check quyền

| Target | Column/field | Condition/value | Remarks |
|---|---|---|---|
| JWT principal | role | Mentor | Contract DIRECT; guard/binding hiện `NOT_FOUND` cho route. |
| Legacy `courses` candidate | `id` | bằng request `course_id` | Candidate BIGINT; schema artifact, live DB chưa xác minh. |
| Legacy `courses` candidate | `mentor_id` | so với numeric Mentor principal | `DERIVED`; principal mapping/assignment chưa có nguồn. |
| Content write target | N/A | N/A | Physical table/model `SOURCE_REQUIRED`; không dựng INSERT SQL. |

### 0.3. Check kết quả

- Thiếu/không hợp lệ JWT: HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Không phải Mentor hoặc không có quyền quản lý course: HTTP 403 `DESIGN_ACCESS_DENIED`.
- Không thấy course / ID không hợp lệ: API không khai báo 404; map sang 422, 403 hay nhánh khác cần xác nhận. Không tự thêm code.
- Lỗi storage/DB hoặc lỗi nội bộ: HTTP 500 `DESIGN_INTERNAL_ERROR`.

## 1. Validate data input

| Field | Contract validation | Validation detail not established |
|---|---|---|
| `course_id` | Required int64 | Positive range, existence semantics and missing-course code mapping. |
| `content_type` | Required `ContentType` | Enum members and allowed values. |
| `title` | Required string | Whitespace/empty policy, maximum length, normalization. |
| `payload` | Required object | Per-type schema, nested validation, size/complexity limits. |

HTTP 422 `DESIGN_VALIDATION_ERROR` is declared. Runtime middleware currently has a generic validation fallback; when wiring, add this path/contract so it emits the declared `DESIGN_*` code. No 404 is declared for this endpoint.

### Request Usage Matrix

| Request field | Source | Data Mapping step | Validate | SQL/Mutation usage | Branch/Loop | Response usage | Gap |
|---|---|---:|---|---|---|---|---|
| Authorization | Header | 1–2 | Bearer JWT, role Mentor | Principal for course access guard | Auth/access branch | Not echoed | Guard and principal mapping unresolved |
| `course_id` | Body | 1–4 | Required int64 | Bind candidate Q1; logical Content scope | Missing/access decision unresolved | `data.course_id` | Physical FK and course-not-found mapping unresolved |
| `content_type` | Body | 1, 3 | Required ContentType | Logical Content subtype | Subtype rules unresolved | `data.content_type` | Enum and payload schema absent |
| `title` | Body | 1, 3 | Required string | Logical Content title | No extra branch known | `data.title` | Length/trim rule absent |
| `payload` | Body | 1, 3 | Required JSON object | Logical Content payload | Type-specific validation unresolved | `data.payload` | Approved payload schema absent |

## 2. Get thông tin

### 2.1. Query

#### Query Matrix

| Query | Type | Source | Columns | Predicate | Evidence/status |
|---|---|---|---|---|---|
| Q1 (candidate) | SELECT | Legacy `courses AS c` | `id`, `mentor_id` | `id = :course_id`; owner comparison needs resolved Mentor principal | `DERIVED` only; not live-schema proof |
| Q2 | N/A | Content | N/A | No pre-read specified by diagram; uniqueness/existence check unspecified | `SOURCE_REQUIRED` |

Candidate Q1 for the legacy schema only:

~~~sql
SELECT c.id, c.mentor_id
FROM courses AS c
WHERE c.id = :course_id;
~~~

This query does not establish an approved auth implementation. No course-assignment join is known. Do not run against a live DB without matching schema and resolved identity model.

### 2.2. JOIN

| Table | Join type | Join condition | Purpose | Evidence |
|---|---|---|---|---|
| Legacy `courses AS c` | No join in Q1 candidate | N/A | Candidate course/direct-owner lookup | Legacy DDL only; `DERIVED` |
| Content persistence relation | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | Persist Content and possibly enforce FK | No generic Content table in legacy schema; pilot block model differs |

### 2.3. WHERE

| Condition | Value source | Purpose | Evidence/status |
|---|---|---|---|
| `c.id = :course_id` | Body `course_id` | Candidate course lookup | `DERIVED` legacy-only |
| `c.mentor_id = :principal_id` | Resolved Mentor principal | Candidate direct-owner check | `DERIVED`; ID binding and assigned course relation absent |
| Content predicates/duplicate/idempotency | Not established | No diagram rule | `SOURCE_REQUIRED`; do not invent uniqueness or retry behavior |

### 2.4. ORDER BY

Không có read/list response trong API #50. Candidate order allocation is a write concern and remains `DERIVED`: next order among root Content siblings for the course. Exact partition/locking/concurrency behavior needs confirmation; no query is approved.

## 3. Insert/Update thông tin

### 3.1. Target table

- Logical target: one `Content` per catalog/AC-22.
- Physical target/table/model: `SOURCE_REQUIRED`.
- Legacy `DB.sql` has `courses`/`lessons` but no generic Content table. V1-PILOT `content_blocks` uses UUID and `lesson_id`; it is not a direct mapping to catalog Content with BIGINT `course_id`.

### 3.2. Conditions

| Condition | Source | Effect | Status |
|---|---|---|---|
| Authenticated Mentor | JWT/catalog | Continue only for Mentor role | DIRECT contract; implementation absent |
| Can manage `course_id` | AC-22 | Allow create | DIRECT precondition; check mechanism SOURCE_REQUIRED |
| Valid request fields | Catalog | Accept/reject request | DIRECT required fields; detailed enum/payload checks SOURCE_REQUIRED |
| Review state | AC-22 + AC-33 | Đề xuất item mới vào moderation queue | `PENDING_REVIEW` là DERIVED candidate; cần xác nhận transition create → pending |

### 3.3. Items insert

| Logical Content field | Input/default | Intended value | Mapping status |
|---|---|---|---|
| `course_id` | Body | Accepted course ID | DIRECT contract; physical column/FK SOURCE_REQUIRED |
| `content_type` | Body | Approved enum member | DIRECT field; enum/storage SOURCE_REQUIRED |
| `title` | Body | Request title | DIRECT field; column/normalization SOURCE_REQUIRED |
| `payload` | Body | Request JSON object | DIRECT field; serialization/schema SOURCE_REQUIRED |
| `status` | Server-side lifecycle | `PENDING_REVIEW` candidate | DERIVED từ AC-22 create + AC-33 pending queue; transition/persistence mapping SOURCE_REQUIRED |
| `parent_id` | No request field | Candidate `null` (root) | DERIVED proposal; parent relation/optional serialization need confirmation |
| `order` | No request field | Candidate next order among course roots | DERIVED proposal; allocation/concurrency rule need confirmation |
| `id` | Server/storage | Generated Content identifier | SOURCE_REQUIRED; strategy and BIGINT mapping unknown |
| Audit/time fields | Not in contract | Unspecified | SOURCE_REQUIRED; do not invent |

### 3.4. Parameters

- Contract body parameters: `course_id`, `content_type`, `title`, `payload`.
- Do not accept client-supplied status, parent, order, owner, ID, audit actor or timestamps.
- Exact SQL, bind parameters, transaction boundary and DB return projection remain blocked on the physical schema. Current database helpers leave transaction ownership to caller; that is not a concrete route implementation.

#### Mutation Matrix

| Mutation | Target | Conditions | Fields | Response | Status |
|---|---|---|---|---|---|
| M1 — logical INSERT | `Content` (physical relation `SOURCE_REQUIRED`) | Mentor manages course; request validates | Four body fields + intended state/defaults above | HTTP 201 `DESIGN_RESOURCE_CREATED`, `ApiEnvelope<Content>` | AC-22 direct logical flow; implementation/schema absent |
| UPDATE/DELETE | N/A | Not part of API #50 | N/A | N/A | Separate APIs #51–#53 |

## Response Source Matrix

| Response field | Contract type | Source/candidate | Transform/null rule | Status |
|---|---|---|---|---|
| `success` | boolean | Envelope branch | `true` on success | Envelope convention |
| `businessCode` | string | Catalog | `DESIGN_RESOURCE_CREATED` | DIRECT |
| `message` | string | Application | Human-readable; exact wording open | DERIVED |
| `data.id` | int64 | Content persistence | Generated value | SOURCE_REQUIRED |
| `data.course_id` | int64 | Body and stored row | Must identify authorized course | DIRECT logical input; persistence SOURCE_REQUIRED |
| `data.content_type` | ContentType | Body and stored row | Valid member per approved enum | SOURCE_REQUIRED enum/storage |
| `data.title` | string | Body and stored row | Preserve or normalize after rule confirmation | SOURCE_REQUIRED storage/normalization |
| `data.payload` | object | Body and stored row | Return approved stored JSON | SOURCE_REQUIRED schema/storage |
| `data.status` | ContentStatus | AC-22 + AC-33 lifecycle | Intended initial `PENDING_REVIEW` candidate | DERIVED transition; enum/schema SOURCE_REQUIRED |
| `data.parent_id` | int64? | Proposed server default | `null` under root-content proposal | DERIVED; confirm |
| `data.order` | int32 | Proposed server allocation | Next root sibling order proposal | DERIVED; confirm |
| `meta` | object | Envelope | No pagination metadata declared | Helper serialization to confirm |
| `traceId` | uuid | Request trace | Envelope trace propagation | Current generic convention; route behavior absent |

## 4. Check kết quả execute query

### 4.1. Thành công

Only after the logical Content is durably created should success return HTTP 201 `DESIGN_RESOURCE_CREATED`. AC-22 then reloads the tree. An exact response object cannot be implemented until ID, storage, enum, payload and optional-field serialization are resolved.

### 4.2. Lỗi hệ thống

Unexpected persistence/mapping errors map to HTTP 500 `DESIGN_INTERNAL_ERROR`. Do not return SQL, physical schema names, stack traces or provider details. Atomicity/retry/idempotency are not specified by this API contract.

### 4.3. Validate lỗi

HTTP 422 `DESIGN_VALIDATION_ERROR` is present in the catalog. Preserve it for confirmed request validation branches. Exact behavior for an unknown enum member, type-specific payload failure, nonexistent course and ID overflow is not fully specified; no new code/status may be added here.

### 4.4. Ngoài trường hợp trên

- 401 and 403 are the only other declared client/auth errors.
- Do not add 404, 409 or 503 to API #50.
- Do not treat an AC-33 state diagram as proof of current persistence or runtime behavior.

## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `3. Data mapping`
- Dimension: `B1:BB61`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `63`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Flow xử lý data |  |
| 4 | `D4` | 0. |  |
| 4 | `E4` | Check quyền |  |
| 5 | `E5` | ・ |  |
| 5 | `F5` | Thực hiện check quyền |  |
| 6 | `E6` | ・ |  |
| 6 | `F6` | Get count khi get data từ … |  |
| 7 | `G7` | Table get |  |
| 7 | `K7` | : |  |
| 8 | `G8` | Conditions |  |
| 8 | `K8` | : |  |
| 10 | `E10` | ・ |  |
| 10 | `F10` | Trường hợp giá trị get được lớn hơn 0, thực hiện các xử lý tiếp theo |  |
| 11 | `E11` | ・ |  |
| 11 | `F11` | Trường hợp giá trị get được bằng 0, trả về status 2 |  |
| 13 | `D13` | 1. |  |
| 13 | `E13` | validate data input |  |
| 14 | `F14` | refer sheet [４．Error] |  |
| 16 | `D16` | 2. |  |
| 16 | `E16` | Get thông tin… |  |
| 18 | `F18` | Table get |  |
| 18 | `K18` | Column get |  |
| 18 | `P18` | Chú thích |  |
| 18 | `U18` | Remarks |  |
| 29 | `F29` | Target table / join condition |  |
| 30 | `F30` | Target table |  |
| 30 | `N30` | Join condition |  |
| 30 | `AL30` | 結合種類 |  |
| 31 | `F31` | txn_ams_t0320 AS a |  |
| 32 | `F32` | txn_amm_v0002 AS b |  |
| 32 | `N32` | ON a . chy_typ = b . kbn_typ AND b . dmin_cd = A AND b . kbnknr_cd = 001 |  |
| 32 | `AL32` | LEFT JOIN |  |
| 33 | `F33` | txn_amm_v0002 AS c |  |
| 33 | `N33` | ON a . chy_typ = c . kbn_typ AND c . dmin_cd = A AND c . kbnknr_cd = Z02 |  |
| 33 | `AL33` | LEFT JOIN |  |
| 35 | `F35` | ・ |  |
| 35 | `G35` | Điều kiện get data |  |
| 37 | `F37` | ・ |  |
| 37 | `G37` | Điều kiện sort |  |
| 41 | `D41` | 3. |  |
| 41 | `E41` | Insert/Update thông tin … |  |
| 42 | `E42` | Update table…. |  |
| 43 | `E43` | ・ |  |
| 43 | `F43` | Items update |  |
| 44 | `F44` | ・ |  |
| 44 | `G44` | Refer sheet [xxxx] |  |
| 45 | `E45` | ・ |  |
| 45 | `F45` | Điều kiện get data |  |
| 46 | `F46` | ・ |  |
| 46 | `G46` | auth_user. id = user hiện tại theo token |  |
| 48 | `D48` | 4. |  |
| 48 | `E48` | check kết quả execute query  |  |
| 49 | `E49` | 1. Thành công |  |
| 50 | `F50` | HTTPStatus = 200 |  |
| 51 | `F51` | Trả về kết quả status = 1 |  |
| 52 | `E52` | 2. Lỗi hệ thống phát sinh |  |
| 53 | `F53` | HTTPStatus = 500 |  |
| 54 | `F54` | Trả về kết quả status = 2 |  |
| 55 | `E55` | 3. Validate lỗi |  |
| 56 | `F56` | HTTPStatus = 400 |  |
| 57 | `F57` | Trả về kết quả status = 2 |  |
| 58 | `E58` | 4. Ngoài trường hợp trên |  |
| 59 | `F59` | Trả về kết quả status = 2 |  |

</details>
