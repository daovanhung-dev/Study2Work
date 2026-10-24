---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "52"
api_name: "Publish/unpublish nội dung Mentor"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

0. Xác thực Bearer JWT, yêu cầu role Mentor và quyền quản lý course theo AC-22.
1. Đọc path content_id. Catalog không khai báo body/query.
2. Nếu contract owner chấp thuận proposal, nhận published:boolean làm trạng thái đích; nếu không, request direction vẫn chưa xác định.
3. Đọc logical Content, course scope và publication/review state hiện tại. Chưa có physical relation được duyệt.
4. Khi published=true, kiểm tra readiness. Chỉ APPROVED là điều kiện state candidate; kiểm tra payload/assets cụ thể còn SOURCE_REQUIRED.
5. Khi published=false, chuyển Content đã PUBLISHED về APPROVED theo proposal. Nếu trạng thái đã bằng target, trả lại hiện trạng không ghi thêm.
6. Cập nhật publication status theo AC-22; không đổi content_type/title/payload và không tạo version trong proposal này.
7. Trả HTTP 200 DESIGN_RESOURCE_UPDATED với ApiEnvelope<Content>. AC-22 client reload cây sau response.

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Bearer JWT và role Mentor là DIRECT từ catalog.
- Quyền quản lý course là DIRECT precondition từ AC-22.
- Map principal sang Mentor ID và assigned-course support là SOURCE_REQUIRED.
- Legacy courses.mentor_id chỉ là candidate direct-owner rule, không chứng minh policy được duyệt.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Logical Content | course_id | Load from stored Content selected by content_id | Logical relationship from reusable schema; physical relation SOURCE_REQUIRED. |
| Legacy courses candidate | id, mentor_id | courses.id = stored Content.course_id; compare owner to resolved Mentor | DERIVED only; no identity binding or assigned-course relation. |

### 0.3. Check kết quả

- Nếu Bearer/Mentor and course permission pass, tiếp tục.
- Nếu không xác thực được, trả 401 DESIGN_AUTHENTICATION_REQUIRED.
- Nếu role/access không đạt, trả 403 DESIGN_ACCESS_DENIED.
- Thứ tự check với resource lookup và anti-enumeration policy cần xác nhận.

## 1. Validate data input

- Canonical input: path content_id:int64!; không có body/query trong catalog.
- Proposed input: published:boolean!, only if approved; non-boolean/missing target maps to 422 DESIGN_VALIDATION_ERROR.
- Path integer bounds, overflow and framework parse behavior need confirmation; do not add a new error code.

## 2. Get thông tin

### 2.1. Query

| Query ID | Target table | Column get | Purpose | Result/branch | Source status |
|---|---|---|---|---|---|
| Q1 | Logical Content relation | id, course_id, content_type, title, payload, status, parent_id, order | Load target and response projection | No Content candidate → 404 | Logical fields DIRECT; physical relation/columns SOURCE_REQUIRED. |
| Q2 | Logical publication/version state | Current approval/publication state and current revision selector | Select eligible state and response | State unknown/not eligible → proposed 422 | Physical version/status model SOURCE_REQUIRED. |
| Q3 | Readiness data | ContentType-specific required content and asset state | Validate before publish=true | Exact checks unknown | SOURCE_REQUIRED; do not invent joins. |
| Q4 | Course access candidate | Course key and owner/assignment | Authorize Mentor against stored course | No permission → 403 | Legacy direct-owner candidate DERIVED; identity/assignment SOURCE_REQUIRED. |

No executable Content SQL is approved. Legacy courses may be inspected only as an explicitly labeled candidate. V1-PILOT content_blocks is UUID/lesson-bound and is not a mapping for the generic BIGINT Content contract.

### 2.2. JOIN

| Target table | Join condition | Join type |
|---|---|---|
| Content to course | Logical Content.course_id references course identity | SOURCE_REQUIRED physical join |
| Content to revision/status | Current revision relation not defined | SOURCE_REQUIRED |
| Content to readiness assets | No approved ContentAsset relation or readiness contract | SOURCE_REQUIRED |

### 2.3. WHERE

- Logical Content identifier equals path content_id.
- Mentor can manage the course stored on Content; exact predicate SOURCE_REQUIRED.
- For publish=true, proposed current status must be APPROVED and all approved readiness checks must pass; state transition DERIVED.
- For publish=false, proposed current status must be PUBLISHED; transition back to APPROVED is DERIVED.
- If the desired state already matches, proposal returns current resource without mutation; DERIVED.
- PENDING_REVIEW and REJECTED are terms in AC-33, not a complete ContentStatus enum.

### 2.4. ORDER BY

Không trả danh sách. Current revision selector/order is SOURCE_REQUIRED; do not invent version number or tie-breaker.

## 3. Insert/Update thông tin

### 3.1. Target table

- Logical target: publication status of the Content/current revision, per AC-22 UPDATE publication status.
- Physical table and publication column: SOURCE_REQUIRED.
- No INSERT or new revision is proposed; API #51 already owns the separate UPDATE Content + version operation.

### 3.2. Conditions

| Condition | Basis | Effect | Status |
|---|---|---|---|
| Authenticated Mentor | Catalog | Continue as Mentor | DIRECT role; identity mapping unresolved |
| Can manage stored course | AC-22 | Allow operation | DIRECT precondition; query SOURCE_REQUIRED |
| Content exists | Path + catalog 404 | Select target | DIRECT error; lookup SOURCE_REQUIRED |
| Ready to publish | Catalog purpose | Allow publish branch | Readiness intent DIRECT; exact criteria SOURCE_REQUIRED |
| Approved state before publishing | AC-33 uses APPROVED/PUBLISHED | Proposed eligibility rule | DERIVED |
| Valid target-state body | Proposed published:boolean | Choose branch | DERIVED; catalog currently omits body |

### 3.3. Items update/insert

| Mutation ID | Logical field | Proposed value/effect | Evidence/status |
|---|---|---|---|
| M1 publish | Publication status | APPROVED → PUBLISHED after readiness passes | AC-22 status update DIRECT; transition DERIVED |
| M1 unpublish | Publication status | PUBLISHED → APPROVED | API title + AC-33 terms; transition DERIVED |
| M1 same target | Publication status | No-op; return current Content | DERIVED idempotency proposal |
| M1 content fields | content_type/title/payload | Preserve unchanged | DERIVED separation from publication-only diagram step |
| M1 tree fields | course_id/parent_id/order | Preserve unchanged | DERIVED; physical mapping SOURCE_REQUIRED |
| M1 version | Content revision | No new revision | DERIVED; confirm with #51 lifecycle |
| M1 audit | Audit actor/time | Not specified | SOURCE_REQUIRED; do not add a column |

### 3.4. Parameters

| Param | Value | Remarks |
|---|---|---|
| content_id | Required path int64 | DIRECT; physical bind/use not defined. |
| published | Proposed JSON boolean | DERIVED; not catalog contract. |
| mentor principal | Bearer JWT context | Role DIRECT; identity mapping SOURCE_REQUIRED. |

### Mutation Matrix

| Branch | Preconditions | Mutation | Failure/result |
|---|---|---|---|
| Publish | Proposed published=true; Content approved; readiness passes | Set publication state to PUBLISHED | Return 200; state/status mapping DERIVED |
| Unpublish | Proposed published=false; current state PUBLISHED | Set publication state to APPROVED | Return 200; state/status mapping DERIVED |
| Already target | Current state equals requested state | No write; return stored Content | 200 no-op proposal DERIVED |
| Not ready or disallowed state | Publish requested but candidate readiness/state fails | No write | 422 DESIGN_VALIDATION_ERROR per catalog |
| Any mutation error | Storage/transaction error | Roll back the status write | 500 DESIGN_INTERNAL_ERROR; transaction mechanism SOURCE_REQUIRED |

### 3.5. Transaction

A single status change should be atomic; this is a DERIVED implementation recommendation. Study database helpers do not commit, but no API #52 view/use-case exists. Physical transaction owner and audit behavior require the selected schema.

## 4. Check kết quả execute query

### 4.1. Thành công

- HTTPStatus = 200.
- businessCode = DESIGN_RESOURCE_UPDATED.
- Map every Content field by 04_Response.md.
- Return the resulting status; do not add is_published or version fields.
- AC-22 client reloads the content tree after the operation.

### 4.2. Lỗi hệ thống

- HTTPStatus = 500; businessCode DESIGN_INTERNAL_ERROR.
- Return safe error envelope; do not expose SQL, schema, stack or provider details.
- Current route is absent; this is expected design behavior only.

### 4.3. Validate lỗi

- HTTPStatus = 422; businessCode DESIGN_VALIDATION_ERROR.
- Candidate reasons: invalid proposed target value, readiness failure, or a state transition not allowed by approved policy.
- Keep these as DERIVED until request body/readiness/state policy is confirmed.

### 4.4. Ngoài trường hợp trên

- Preserve exactly 401/403/404/422/500 and their catalog codes.
- Do not add 409, 400, 423 or 503.
- If the route is wired, add its path to the middleware contract allowlist or implement equivalent mapping; current allowlist excludes it.

## Response Source Matrix

| Response field | Type | Source/candidate | Rule/status |
|---|---|---|---|
| success | boolean | Envelope branch | Study envelope convention; endpoint absent |
| businessCode | string | Catalog | DIRECT DESIGN_RESOURCE_UPDATED |
| message | string | Application | Exact wording unspecified; DERIVED |
| data.id | int64 | Path-selected Content | Physical projection SOURCE_REQUIRED |
| data.course_id | int64 | Stored Content | SOURCE_REQUIRED |
| data.content_type | ContentType | Stored Content | Enum and persistence SOURCE_REQUIRED |
| data.title | string | Stored Content | SOURCE_REQUIRED |
| data.payload | object | Stored Content | Payload schema SOURCE_REQUIRED |
| data.status | ContentStatus | Resulting logical state | Transition DERIVED; complete enum/storage SOURCE_REQUIRED |
| data.parent_id | int64? | Stored Content | Null/omit and persistence SOURCE_REQUIRED |
| data.order | int32 | Stored Content | Persistence SOURCE_REQUIRED |
| meta | object | Envelope | No pagination contract; helper serialization alignment required |
| traceId | uuid | Request trace | Study envelope convention; endpoint absent |

---
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
