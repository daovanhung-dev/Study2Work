---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "51"
api_name: "Cập nhật nội dung Mentor"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
1. Đọc Authorization Bearer, decode principal và xác nhận role Mentor; Study chưa có Mentor guard/identity mapping.
2. Parse content_id:int64! theo catalog; body không có trong contract. Nếu áp dụng proposal, validate full body content_type/title/payload.
3. Q1 load Content theo content_id để lấy course ownership, current content và response fields; physical relation chưa được xác định.
4. Q2 kiểm tra quyền quản lý course theo stored course_id; legacy courses.id/mentor_id chỉ là direct-owner candidate.
5. Q3/version source kiểm tra revision hiện hành/eligibility; schema và rule SOURCE_REQUIRED.
6. Trong một transaction, áp dụng logical UPDATE Content + version theo AC-22. Proposal: tạo revision mới từ body, giữ revision cũ, revision mới PENDING_REVIEW.
7. Nếu cập nhật version hoặc Content thất bại, rollback toàn bộ logical write; physical transaction/SQL chưa thể xác định.
8. Trả HTTP 200 DESIGN_RESOURCE_UPDATED với ApiEnvelope<Content>; AC-22 sau đó reload cây.
~~~

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Catalog yêu cầu Bearer JWT và `role=Mentor`.
- AC-22 yêu cầu Mentor có quyền quản lý course chứa Content.
- Lấy `course_id` từ Content đã lưu, không tin một giá trị course/owner do client gửi.
- Current Study auth helper có Student guard; Mentor guard, principal claim và assignment relation chưa có source.

### 0.2. Query/check quyền

| Target | Column/field | Condition/value | Remarks |
|---|---|---|---|
| JWT principal | role | Mentor | Contract DIRECT; runtime guard cho API #51 NOT_FOUND. |
| Content logical entity | `id` | bằng path `content_id` | Q1 logical lookup; physical table/column SOURCE_REQUIRED. |
| Content logical entity | `course_id` | lấy từ row Q1 | Không nhận từ body proposal; mapping vật lý SOURCE_REQUIRED. |
| Legacy `courses` candidate | `id` | bằng stored `course_id` | Candidate BIGINT schema; live schema chưa xác minh. |
| Legacy `courses` candidate | `mentor_id` | so với numeric Mentor principal | DERIVED direct-owner check; assignment/identity chưa có nguồn. |

### 0.3. Check kết quả

- JWT thiếu/không hợp lệ: 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Không có role Mentor hoặc không có quyền quản lý course: 403 `DESIGN_ACCESS_DENIED`.
- Không tìm thấy Content theo `content_id`: 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Body sai theo proposed/approved validation: 422 `DESIGN_VALIDATION_ERROR`.
- Lỗi lưu Content hoặc version: 500 `DESIGN_INTERNAL_ERROR`.

## 1. Validate data input

### 1.1. Contract trực tiếp

- `content_id`: required int64 path theo catalog.
- Catalog không khai báo body, range của int64 hoặc malformed-path HTTP behavior.

### 1.2. Proposed body validation — DERIVED

Chỉ áp dụng nếu contract owner chấp thuận proposed full-replacement body:

| Field | Validation candidate | Unresolved rule |
|---|---|---|
| `content_type` | Required enum `ContentType` | Enum members và type-change policy. |
| `title` | Required string | Empty/whitespace, max length và normalization. |
| `payload` | Required JSON object | Subtype schema, nested fields, size and safety limits. |

Không nhận `course_id`, `status`, `parent_id`, `order` hoặc `id` trong proposed body. Không suy diễn field-level constraints từ legacy/pilot schema khác model.

### Request Usage Matrix

| Request item | Source | Data Mapping step | Validate | Query/mutation usage | Branch/Loop | Response usage | Gap |
|---|---|---:|---|---|---|---|---|
| Authorization | Header | 1, 2 | Bearer JWT + role Mentor | Principal for course access | Auth/access branches | Không echo token/claims | Identity binding SOURCE_REQUIRED |
| `content_id` | Path | 2–4 | Required int64 | Q1 target; resolve stored course/version | Missing row → 404 candidate by code | `data.id` | Physical source/malformed path unresolved |
| `content_type` (proposal) | Body | 2, 3, 6 | Required ContentType | M1 revision content | Type-specific branch | `data.content_type` | Body/enum DERIVED/SOURCE_REQUIRED |
| `title` (proposal) | Body | 2, 3, 6 | Required string | M1 revision content | No extra branch defined | `data.title` | Body/normalization DERIVED/SOURCE_REQUIRED |
| `payload` (proposal) | Body | 2, 3, 6 | Required JSON object | M1 revision content | Subtype validation unresolved | `data.payload` | Body/schema DERIVED/SOURCE_REQUIRED |
| Existing `course_id` | Stored Content | 3–4 | Read-only scope | Q2 course access | Access branch | `data.course_id` | Physical mapping SOURCE_REQUIRED |
| Existing status/tree fields | Stored Content | 3, 6 | Preserve in this proposal except new revision status | Version/presentation | Review/publish branch open | `data.status`, `data.parent_id`, `data.order` | DERIVED/SOURCE_REQUIRED |

## 2. Get thông tin

### 2.1. Query

#### Query Matrix

| Query ID | Purpose | Type | Base relation | Columns | JOIN | WHERE | Result/branch | Status |
|---|---|---|---|---|---|---|---|---|
| Q1 | Load Content target | SELECT | `SOURCE_REQUIRED` Content relation | `id`, `course_id`, `content_type`, `title`, `payload`, `status`, `parent_id`, `order` | SOURCE_REQUIRED | `id = :content_id` logical predicate | No row → 404 | Physical schema SOURCE_REQUIRED |
| Q2 | Resolve owning course/direct owner | SELECT | Legacy `courses AS c` candidate | `c.id`, `c.mentor_id` | None | `c.id = :stored_course_id` | Candidate owner/access decision | DERIVED legacy only |
| Q3 | Read current revision/version | SELECT or version metadata | `SOURCE_REQUIRED` | Version identifier/current marker/history | SOURCE_REQUIRED | By Content ID/current version | Eligibility/advance version | Model and rule SOURCE_REQUIRED |

Q1 chỉ mô tả logical target. Chưa có câu SQL Content nào được duyệt vì chưa xác định được bảng/cột vật lý tương thích. Q2 dưới đây chỉ là candidate cho legacy DDL:

~~~sql
SELECT c.id, c.mentor_id
FROM courses AS c
WHERE c.id = :stored_course_id;
~~~

Q2 does not resolve JWT-to-Mentor ID or assigned-course permissions and is not live-schema evidence.

### 2.2. JOIN

| Relation | Join type | Join condition | Purpose | Status |
|---|---|---|---|---|
| Content to course | SOURCE_REQUIRED | `Content.course_id` → course key | Access check | Logical relationship implied by `Content.course_id`; physical key not confirmed |
| Content to version | SOURCE_REQUIRED | Content/version relationship unknown | Read current version/history | AC-22 says `+ version`; exact relation SOURCE_REQUIRED |

### 2.3. WHERE

| Condition | Source | Purpose | Status |
|---|---|---|---|
| Content ID equals `:content_id` | Path | Select only target Content | Direct logical key; physical query SOURCE_REQUIRED |
| Stored course owner/assignment allows principal | AC-22 + auth model | Ensure Mentor can manage target | DIRECT permission requirement; predicate SOURCE_REQUIRED |
| Version is current/editable | Version/business rule | Prevent editing wrong revision | No status/editability branch specified; SOURCE_REQUIRED |

### 2.4. ORDER BY

API không trả danh sách hoặc thứ tự sắp xếp. Quy tắc thời gian/thứ tự version là `SOURCE_REQUIRED`; không tự đặt số version hoặc tie-breaker.

## 3. Insert/Update thông tin

### 3.1. Target table

- Logical target: existing `Content` plus its version/revision state, matching AC-22 “UPDATE Content + version”.
- Physical table/model: `SOURCE_REQUIRED`; neither legacy DDL nor V1-PILOT DDL maps directly to the catalog Content contract.
- Do not use `content_blocks.row_version` as semantic Content version without approval; it is a different UUID/lesson-bound model.

### 3.2. Conditions

| Condition | Source | Effect | Status |
|---|---|---|---|
| Authenticated Mentor | Catalog | Continue as Mentor | DIRECT contract; implementation absent |
| Can manage stored Content course | AC-22 | Allow update | DIRECT precondition; access query SOURCE_REQUIRED |
| Content exists | Path resource + catalog 404 | Update target | 404 code DIRECT; exact lookup SOURCE_REQUIRED |
| Body is valid | Catalog declares 422; body fields absent | Validate proposed body | Error code DIRECT; field contract DERIVED |
| Current revision can be edited | Version state | Allow/deny mutation | SOURCE_REQUIRED; no state transition matrix in AC-22 |

### 3.3. Items update/version

| Logical value | Input/source | Proposed action | Evidence/status |
|---|---|---|---|
| Content identity `id` | Path + stored row | Preserve | DIRECT resource target; physical mapping SOURCE_REQUIRED |
| `course_id` | Stored row | Preserve; authorize against it | DERIVED immutable scope proposal |
| `content_type` | Proposed body | Replace for new revision | DERIVED; type-change policy open |
| `title` | Proposed body | Replace for new revision | DERIVED |
| `payload` | Proposed body | Replace full JSON object for new revision | DERIVED; payload schema SOURCE_REQUIRED |
| `status` | Server lifecycle | New revision candidate `PENDING_REVIEW` | DERIVED from AC-22 update/version + AC-33 queue |
| `parent_id` | Stored row | Preserve | DERIVED; no move operation in AC-22 body |
| `order` | Stored row | Preserve | DERIVED; no reorder input in AC-22 body |
| Previous revision | Existing version state | Preserve immutable history | DERIVED proposal; schema/retention SOURCE_REQUIRED |
| New revision | Proposed full body | Advance current logical version | AC-22 version effect DIRECT; exact version operation SOURCE_REQUIRED |
| Audit/updated fields | Not in contract | No column/value assigned | SOURCE_REQUIRED |

### 3.4. Parameters and transaction

- Catalog path parameter: `content_id`.
- Proposed body parameters only: `content_type`, `title`, `payload`.
- Do not accept client-supplied course, status, parent, order, ID, version number, audit actor or timestamps under this proposal.
- Recommendation: update Content/current-version reference and write new revision in one transaction; rollback all versioned writes if any step fails. Atomicity is `DERIVED` from one logical update/version operation; exact DB transaction boundary depends on selected schema.
- Current Study DB helpers do not commit; when an implementation is designed, the view/use case must own transaction. This is source convention, not API #51 runtime behavior.

#### Mutation Matrix

| Mutation ID | Operation | Target | Record condition | Fields/effect | Mapping | Transaction/failure | Status |
|---|---|---|---|---|---|---|---|
| M1 | Logical UPDATE + new version | Content + version model (`SOURCE_REQUIRED` physical relation) | Existing `content_id`; Mentor manages stored course; proposed body validates | `content_type` từ proposed body | `07_table.md` | Transaction proposal; rollback on failure | Body DERIVED; physical mapping SOURCE_REQUIRED |
| M1 | Logical UPDATE + new version | Content + version model (`SOURCE_REQUIRED` physical relation) | Như trên | `title` từ proposed body | `07_table.md` | Cùng transaction M1 | Body DERIVED; physical mapping SOURCE_REQUIRED |
| M1 | Logical UPDATE + new version | Content + version model (`SOURCE_REQUIRED` physical relation) | Như trên | `payload` từ proposed body | `07_table.md` | Cùng transaction M1 | Body DERIVED; payload schema SOURCE_REQUIRED |
| M1 | Logical UPDATE + new version | Content + version model (`SOURCE_REQUIRED` physical relation) | Như trên | Giữ nguyên `id` | `07_table.md` | Cùng transaction M1 | Preserve rule DERIVED; physical mapping SOURCE_REQUIRED |
| M1 | Logical UPDATE + new version | Content + version model (`SOURCE_REQUIRED` physical relation) | Như trên | Giữ nguyên `course_id` | `07_table.md` | Cùng transaction M1 | Preserve rule DERIVED; physical mapping SOURCE_REQUIRED |
| M1 | Logical UPDATE + new version | Content + version model (`SOURCE_REQUIRED` physical relation) | Như trên | Giữ nguyên `parent_id` | `07_table.md` | Cùng transaction M1 | Preserve rule DERIVED; physical mapping SOURCE_REQUIRED |
| M1 | Logical UPDATE + new version | Content + version model (`SOURCE_REQUIRED` physical relation) | Như trên | Giữ nguyên `order` | `07_table.md` | Cùng transaction M1 | Preserve rule DERIVED; physical mapping SOURCE_REQUIRED |
| M1 | Logical UPDATE + new version | Content + version model (`SOURCE_REQUIRED` physical relation) | Như trên | Tạo/advance logical version; trạng thái revision mới candidate `PENDING_REVIEW` | `07_table.md` | Cùng transaction M1; rollback mọi phần nếu lỗi | AC-22 version effect DIRECT; state DERIVED; schema SOURCE_REQUIRED |

Không suy ra thao tác insert/delete identity Content. API #50 tạo; #52 publish; #53 xóa.

## Response Source Matrix

| Response field | Type | Source/candidate | Transform/null rule | Status |
|---|---|---|---|---|
| `success` | boolean | Envelope branch | true on successful update | Envelope convention |
| `businessCode` | string | Catalog | `DESIGN_RESOURCE_UPDATED` | DIRECT |
| `message` | string | Application | Safe localized text; exact copy open | DERIVED |
| `data.id` | int64 | Path + persisted Content | Preserve `content_id` | Physical projection SOURCE_REQUIRED |
| `data.course_id` | int64 | Stored Content | Preserve owning course | SOURCE_REQUIRED physical mapping |
| `data.content_type` | ContentType | Proposed body/new version | Return accepted member | DERIVED body; enum/schema SOURCE_REQUIRED |
| `data.title` | string | Proposed body/new version | Return accepted normalized value only after rule known | DERIVED body; storage/normalization SOURCE_REQUIRED |
| `data.payload` | object | Proposed body/new version | Return complete stored object | DERIVED body; schema/storage SOURCE_REQUIRED |
| `data.status` | ContentStatus | Proposed review lifecycle | `PENDING_REVIEW` for new revision candidate | DERIVED; status model SOURCE_REQUIRED |
| `data.parent_id` | int64? | Stored Content | Preserve; null/omit serialization unresolved | DERIVED preserve; SOURCE_REQUIRED mapping |
| `data.order` | int32 | Stored Content | Preserve | SOURCE_REQUIRED mapping |
| `meta` | object | Envelope | No pagination metadata | Helper serialization to confirm |
| `traceId` | uuid | Request trace | Propagate request trace | Generic convention; route absent |
| `data.version` | Not in schema | None | Must not add | Not declared; would require catalog change |

## 4. Check kết quả execute query

### 4.1. Thành công

Chỉ trả HTTP 200 `DESIGN_RESOURCE_UPDATED` sau khi logical update Content/version commit thành công. Giữ nguyên response `ApiEnvelope<Content>`; không thêm metadata version vì catalog Content không có field này. Sau đó client AC-22 reload cây.

### 4.2. Lỗi hệ thống

Lỗi bất ngờ khi query/version/storage được map thành HTTP 500 `DESIGN_INTERNAL_ERROR`. Không trả SQL, schema, stack trace hoặc chi tiết provider. Không báo thành công nếu chỉ một phần Content/version được ghi; đảm bảo transaction hiện là đề xuất, chờ schema vật lý.

### 4.3. Validate lỗi

Catalog khai báo HTTP 422 `DESIGN_VALIDATION_ERROR`. Chỉ áp dụng cho validation body sau khi proposal được duyệt. Cần xác nhận cách xử lý ContentType lạ, payload sai subtype và state transition không hợp lệ. Không thêm 409 cho version race vì catalog không có mã này.

### 4.4. Ngoài trường hợp trên

- Preserve exact 401/403/404/422/500 catalog set.
- Do not add 400, 409, 423 or 503.
- If route is later wired, add path to `DESIGN_CONTRACT_PATHS` or current middleware fallback emits generic codes for validation/unhandled exceptions.

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
