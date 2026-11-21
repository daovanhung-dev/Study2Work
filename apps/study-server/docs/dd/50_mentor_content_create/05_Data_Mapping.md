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
1. Nhận Bearer JWT và body `{course_id, content_type, title, payload}` theo catalog #50.
2. Shared guard yêu cầu role Mentor và numeric JWT subject; view khóa course row rồi kiểm tra direct ownership qua `courses.mentor_id`.
3. FastAPI strict-validates signed-int64 course ID, string fields, JSON object payload và từ chối body field ngoài contract. Enum/payload subtype chưa có nguồn.
4. Course thiếu hoặc không thuộc Mentor map cùng 403 `DESIGN_ACCESS_DENIED` theo implementation decision; không thêm 404.
5. Lấy order kế tiếp của active root siblings (`GREATEST(MAX(content_order)+1, 0)`, first order 0) trong khi course row lock còn hiệu lực.
6. INSERT `contents` với root `parent_id=NULL`, status `PENDING_REVIEW`, body fields và `content_order`; cast serialized JSON sang JSONB.
7. Kiểm tra toàn bộ `RETURNING` projection, commit transaction rồi dựng response.
8. Trả HTTP 201 `DESIGN_RESOURCE_CREATED`; AC-22 mô tả client reload cây sau create. Các default status/root/order là `DERIVED`; local DDL/tests không chứng minh live DB.
~~~

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Authentication là Bearer JWT và role Mentor theo catalog.
- AC-22 precondition yêu cầu Mentor có quyền quản lý course.
- Không nhận `mentor_id`, principal ID hoặc quyền từ body.
- Shared guard trả numeric subject; implementation dùng direct `courses.mentor_id` convention của API #47/#49.
- Assigned-course relation không có trong legacy source; không khẳng định assigned Mentor được phép tạo.

### 0.2. Query/check quyền

| Target | Column/field | Condition/value | Remarks |
|---|---|---|---|
| JWT principal | role | Mentor | Contract DIRECT; shared guard source-backed. |
| Legacy `courses` | `id` | bằng request `course_id` | Local BIGINT DDL; lookup locks row for order allocation. |
| Legacy `courses` | `mentor_id` | so với numeric Mentor principal | Direct-owner implementation convention; assignment policy remains open. |
| Legacy `contents` | `course_id` | Authorized request course | Local DDL/migration 006; live schema unverified. |

### 0.3. Check kết quả

- Thiếu/không hợp lệ JWT: HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Không phải Mentor, course không tồn tại, hoặc course không thuộc direct owner: HTTP 403 `DESIGN_ACCESS_DENIED`.
- Sai body type/required field/extra field: HTTP 422 `DESIGN_VALIDATION_ERROR`.
- Không thêm 404; absent-course → 403 là quyết định `DERIVED` trong error set catalog.
- Lỗi storage/DB hoặc lỗi nội bộ: HTTP 500 `DESIGN_INTERNAL_ERROR`.

## 1. Validate data input

| Field | Contract validation | Validation detail not established |
|---|---|---|
| `course_id` | Required strict signed int64 | Values outside signed int64 fail framework validation; missing course maps 403 by implementation decision. |
| `content_type` | Required strict string | `ContentType` enum members remain unknown; implementation does not validate a closed set. |
| `title` | Required strict string | No whitespace, empty, max-length or normalization rule is applied. |
| `payload` | Required JSON object | Only object shape is validated; subtype keys/size rules remain unknown. |

HTTP 422 `DESIGN_VALIDATION_ERROR` is declared and route path is in `DESIGN_CONTRACT_PATHS`. Framework request errors preserve that code. No 404 is declared for this endpoint.

### Request Usage Matrix

| Request field | Source | Data Mapping step | Validate | SQL/Mutation usage | Branch/Loop | Response usage | Gap |
|---|---|---:|---|---|---|---|---|
| Authorization | Header | 1–2 | Bearer JWT, role Mentor | Numeric subject for direct-owner check | Auth/access branch | Not echoed | Assignment relation/policy is not source-backed |
| `course_id` | Body | 1–5 | Required strict int64 | Course lock/owner query and Content FK | Missing/non-owner → 403 | `data.course_id` | 403 mapping is DERIVED; live FK unverified |
| `content_type` | Body | 1, 3, 6 | Required strict string | Insert open string | No closed enum branch | `data.content_type` | Enum members/payload compatibility absent |
| `title` | Body | 1, 3, 6 | Required strict string | Insert unchanged | No extra branch | `data.title` | No max/trim rule |
| `payload` | Body | 1, 3, 6 | Required JSON object | JSON serialize and cast to JSONB | Subtype validation not available | `data.payload` | Subtype schema absent |

## 2. Get thông tin

### 2.1. Query

#### Query Matrix

| Query | Type | Source | Columns | Predicate | Evidence/status |
|---|---|---|---|---|---|
| Q1 | SELECT ... FOR UPDATE | Legacy `courses` | `id`, `mentor_id` | `id = :course_id` | Implemented; direct-owner pattern is DERIVED; local DDL only |
| Q2 | Aggregate SELECT | Legacy `contents` | `MAX(content_order)` | course match, root (`parent_id IS NULL`), active (`deleted_at IS NULL`) | Implemented; first order 0; allocation is DERIVED |
| Q3 | INSERT ... RETURNING | Legacy `contents` | All Content response columns | Request fields + server status/root/order | Implemented against local DDL; live schema unverified |

Q1 used by current source:

~~~sql
SELECT id, mentor_id
FROM courses
WHERE id = :course_id
LIMIT 1
FOR UPDATE;
~~~

The shared auth guard resolves the numeric JWT subject. The course row lock remains held through order allocation and INSERT/commit. No course-assignment join is known; checked-in DDL does not prove live schema.

Q2 computes the next order from active root siblings:

~~~sql
SELECT GREATEST(COALESCE(MAX(content_order::BIGINT) + 1, 0), 0) AS next_order
FROM contents
WHERE course_id = :course_id
  AND parent_id IS NULL
  AND deleted_at IS NULL;
~~~

Q3 inserts one root node with `status='PENDING_REVIEW'` and returns the stored Content projection; payload is bound as JSON text and cast to JSONB.

### 2.2. JOIN

| Table | Join type | Join condition | Purpose | Evidence |
|---|---|---|---|---|
| Legacy `courses` | No join | N/A | Lock course and read direct owner | Current source; legacy DDL only; live schema unverified |
| `contents` | `course_id` FK | `courses.id` | Persist Content and enforce course relation | DDL/migration 006 source-backed locally; live schema unverified |

### 2.3. WHERE

| Condition | Value source | Purpose | Evidence/status |
|---|---|---|---|
| `id = :course_id` | Body `course_id` | Course lock and existence lookup | Current source; local schema only |
| `mentor_id = :principal_id` | Shared Mentor guard | Direct-owner check | Implementation convention; assigned-course relation absent |
| `course_id = :course_id AND parent_id IS NULL AND deleted_at IS NULL` | Body | Root order allocation | Current source; query is in `NEXT_ROOT_CONTENT_ORDER` |

### 2.4. ORDER BY

Không có read/list response trong API #50. Order allocation là write concern: view lấy aggregate từ active root siblings, bắt đầu từ 0, và giữ khóa course row đến khi commit. Đây là implementation rule `DERIVED`, không phải rule trực tiếp trong catalog/diagram.

## 3. Insert/Update thông tin

### 3.1. Target table

- Logical target: one `Content` per catalog/AC-22.
- Physical target: legacy `contents`; local source implements API #50, while live availability is unverified.
- Legacy `DB.sql` now includes generic `contents` fields used by API #49. V1-PILOT `content_blocks` uses UUID and `lesson_id`; it is not a direct mapping to catalog Content with BIGINT `course_id`.

### 3.2. Conditions

| Condition | Source | Effect | Status |
|---|---|---|---|
| Authenticated Mentor | JWT/catalog | Continue only for Mentor role | DIRECT contract; shared guard source-backed |
| Direct owner of `course_id` | API #47/#49 convention + AC-22 | Allow create | DERIVED implementation pattern; assignment support absent |
| Valid request fields | Catalog + Pydantic model | Accept/reject request | Required types and extra-field rejection are tested; enum/payload subtype remain open |
| Review state | AC-33 queue | Create node in moderation queue | `PENDING_REVIEW` is DERIVED implementation choice |
| Parent placement | Request has no `parent_id` | Create a root node | `NULL` is DERIVED from request shape |
| Root order | Local Content tree field | Next active root order, first 0 | DERIVED; course row lock held through transaction |

### 3.3. Items insert

| Logical Content field | Input/default | Intended value | Mapping status |
|---|---|---|---|
| `course_id` | Body | Authorized course ID | DIRECT contract; local FK to `courses`; live schema unverified |
| `content_type` | Body | Store strict string unchanged | DIRECT field; open string; enum members unknown |
| `title` | Body | Store strict string unchanged | DIRECT field; no added trim/length rule |
| `payload` | Body | JSON serialize, cast and store as JSONB | DIRECT object shape; subtype schema unknown |
| `status` | Server-side lifecycle | `PENDING_REVIEW` | DERIVED from AC-33 queue condition |
| `parent_id` | Server default | `NULL` root | DERIVED from absence of parent input |
| `content_order` | Server allocator | Next active root order, first order 0 | DERIVED; lock course row during allocation |
| `id` | Persistence layer | BIGSERIAL-generated Content ID | Present in local DDL; live schema unverified |
| `deleted_at` | Local DDL default | Omitted from INSERT, therefore NULL | Present in local DDL |
| Audit/time fields | Not in local table/contract | Not written by API #50 | Do not invent fields |

### 3.4. Parameters

- Contract body parameters: `course_id`, `content_type`, `title`, `payload`.
- Do not accept client-supplied status, parent, order, owner, ID, audit actor or timestamps.
- SQL remains a set of constants in `query.py`; `view.py` binds values and owns the transaction. It commits only after validating the `RETURNING` projection and rolls back failures.

#### Mutation Matrix

| Mutation | Target | Conditions | Fields | Response | Status |
|---|---|---|---|---|---|
| M1 — INSERT | `contents` | Mentor direct-owns course; request validates | Four body fields + DERIVED status/root/order | HTTP 201 `DESIGN_RESOURCE_CREATED`, `ApiEnvelope<Content>` | Local implementation + legacy DDL; live schema unverified |
| UPDATE/DELETE | N/A | Not part of API #50 | N/A | N/A | Separate APIs #51–#53 |

## Response Source Matrix

| Response field | Contract type | Source/candidate | Transform/null rule | Status |
|---|---|---|---|---|
| `success` | boolean | Envelope branch | `true` on success | Envelope convention |
| `businessCode` | string | Catalog | `DESIGN_RESOURCE_CREATED` | DIRECT |
| `message` | string | API #50 view | `Content created.` | Current source |
| `data.id` | int64 | `contents.id` | BIGSERIAL-generated value | Base ID mapping is in checked-in DDL; live schema unverified |
| `data.course_id` | int64 | Stored row | Course from authorized request | DIRECT field; local persistence; live schema unverified |
| `data.content_type` | ContentType | Stored row | Open string as submitted | DIRECT field; closed enum remains unknown |
| `data.title` | string | Stored row | String as submitted | DIRECT field; no normalization |
| `data.payload` | object | Stored JSONB row | JSON object from request | DIRECT shape; subtype schema remains unknown |
| `data.status` | ContentStatus | Server-side insert | `PENDING_REVIEW` | DERIVED from AC-33 queue condition |
| `data.parent_id` | int64? | Server-side insert | NULL and omitted by response serialization | DERIVED root placement |
| `data.order` | int32 | Aggregate query | Next active root order, starts at 0 | DERIVED allocation; serialized by shared Content model |
| `meta` | object | Envelope helper | Empty object; no pagination metadata | Current helper behavior |
| `traceId` | uuid | Request trace | Envelope/header trace propagation | Current route behavior covered by TestClient |

## 4. Check kết quả execute query

### 4.1. Thành công

After validating the INSERT/RETURNING row, the view commits and returns HTTP 201 `DESIGN_RESOURCE_CREATED`. AC-22 then reloads the tree. The generated ID and stored row are used in the response; live DB availability remains unverified.

### 4.2. Lỗi hệ thống

Unexpected persistence/mapping errors map to HTTP 500 `DESIGN_INTERNAL_ERROR`. Do not return SQL, physical schema names, stack traces or provider details. Atomicity/retry/idempotency are not specified by this API contract.

### 4.3. Validate lỗi

HTTP 422 `DESIGN_VALIDATION_ERROR` covers framework validation for required/type/body-shape/extra-field failures. Closed enum and subtype validation are absent because no members/schema are source-backed. Nonexistent course maps 403 by the derived decision above; order overflow and DB errors map 500.

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
