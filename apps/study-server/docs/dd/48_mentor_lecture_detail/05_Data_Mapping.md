---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "48"
api_name: "Tải lại lecture vừa tạo"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
1. Xác thực Bearer JWT và role Mentor.
2. Parse path lecture_id theo int64 contract.
3. Q1 đọc một lessons row và course owner bằng LEFT JOIN.
4. So sánh `courses.mentor_id` với principal Mentor như API #46/#47; ẩn Lesson có tombstone `status='DELETED'` từ API #86.
5. Q2 đọc `lesson_uploads` theo `asset_position` và resolve metadata trong `uploads` theo owner/purpose/course.
6. Map Lecture; SQL NULL content thành JSON null; lỗi parent/link integrity trả 500.
7. Trả 200 hoặc một trong các lỗi catalog 401/403/404/500.
~~~

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Yêu cầu Bearer JWT hợp lệ và role Mentor theo catalog.
- Lấy principal từ token đã xác thực; không nhận mentor_id từ path, query hoặc body.
- Runtime dùng `validate_current_user_request(..., role="MENTOR")`; principal là numeric JWT subject như API #46/#47. Mapping với deployed identity chưa xác minh.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| JWT principal | role | Phải là Mentor | Catalog trực tiếp; runtime guard chưa có. |
| courses | mentor_id | So với principal Mentor hiện tại | Direct owner theo API #46/#47; assigned-course relation chưa có. |
| lessons | id | Bằng lecture_id trong path | Chỉ truy cập lecture được định danh; query Q1 bên dưới. |

### 0.3. Check kết quả

- Token thiếu hoặc không hợp lệ: 401 DESIGN_AUTHENTICATION_REQUIRED.
- Principal không có role Mentor: 403 DESIGN_ACCESS_DENIED.
- Lecture tồn tại nhưng owner không khớp direct owner: 403 DESIGN_ACCESS_DENIED; course assignment chưa được hỗ trợ.
- Không có lecture theo ID: 404 DESIGN_RESOURCE_NOT_FOUND.
- Lecture có course_id NULL hoặc parent course không tồn tại: candidate 500 DESIGN_INTERNAL_ERROR vì response bắt buộc course_id và không thể hoàn tất owner check.

## 1. Validate data input

### Request Usage Matrix

| Request field | Source | Validate/use | Query usage | Response usage | Gap |
|---|---|---|---|---|---|
| Authorization | Header Authorization | Bearer JWT hợp lệ; role Mentor | Cung cấp principal cho access check | Không echo token/claims | Shared guard is wired; deployed identity mapping/assignment remains unresolved. |
| lecture_id | Path | Parse theo int64; không thêm positive-only rule | Q1 lessons.id = :lecture_id | data.id | Mã hóa lỗi path malformed/overflow chưa có trong catalog. |
| Body | N/A | N/A | Không dùng | N/A | Catalog không khai báo body. |
| Query | N/A | N/A | Không dùng | N/A | Catalog không khai báo query. |

- Catalog không có 422 cho API #48. Runtime maps malformed/out-of-range path to 404 DESIGN_RESOURCE_NOT_FOUND as an implementation decision; DD vẫn cần contract owner xác nhận.

## 2. Get thông tin

### 2.1. Query

#### Query Matrix

| Query | Type | Source | Query item | Rule | Evidence status |
|---|---|---|---|---|---|
| Q1 | SELECT | lessons AS l | id, course_id, name, content, sort_order, status | Lecture fields | Checked-in legacy DDL; live schema not verified |
| Q1 | LEFT JOIN | courses AS c | c.id = l.course_id | Parent course and owner | Checked-in legacy relation; live schema not verified |
| Q1 | WHERE | lessons AS l | l.id = :lecture_id | No row → 404 | Runtime/API contract |
| Q1 | CHECK | courses AS c | c.mentor_id = :mentor_id | Owner mismatch → 403 | Runtime matches #46/#47; assigned course unsupported |
| Q1 | FILTER | `lessons.status` | `status IS DISTINCT FROM 'DELETED'` | Hide API #86 tombstone; return other stored status values | Local DERIVED visibility |
| Q2 | SELECT | lesson_uploads AS lu | upload_id ordered by asset_position | Linked upload IDs in request order | Migration 005; live schema not verified |
| Q2 | LEFT JOIN | uploads AS u | u.id = lu.upload_id | Resolve persisted UploadAsset metadata | API #34 model and legacy DDL |
| Q2 | SCOPE | uploads AS u | owner_id, purpose='LECTURE', course_id | Ensure same Mentor/course and lecture purpose | Runtime; unresolved link metadata becomes 500 |

Current local SQL projection for the checked-in legacy schema:

~~~sql
SELECT l.id, l.course_id, l.name, l.content, l.sort_order, l.status,
       c.id AS parent_course_id, c.mentor_id
FROM lessons AS l
LEFT JOIN courses AS c ON c.id = l.course_id
WHERE l.id = :lecture_id;
~~~

Q2 reads the ordered association and scoped metadata:

~~~sql
SELECT lu.upload_id, u.id, u.file_name AS name, u.url, u.content_type,
       u.size_bytes, u.status
FROM lesson_uploads AS lu
LEFT JOIN uploads AS u
  ON u.id = lu.upload_id
 AND u.owner_id = :mentor_id
 AND u.purpose = 'LECTURE'
 AND u.course_id = :course_id
WHERE lu.lesson_id = :lecture_id
ORDER BY lu.asset_position ASC, lu.upload_id ASC;
~~~

- No lesson row maps to 404.
- A lesson row with NULL or missing parent course cannot satisfy required course_id or access check; candidate maps to 500 integrity failure.
- If the course exists, compare its mentor_id with the authenticated numeric Mentor principal. Assigned-course membership remains unsupported pending an assignment source.
- Exclude only `lessons.status='DELETED'`; return all other stored lesson statuses. Course status behavior is unchanged.

### 2.2. JOIN

| Table | Join type | Join condition | Purpose | Evidence |
|---|---|---|---|---|
| courses AS c | LEFT JOIN | c.id = lessons.course_id | Keep an existing lesson visible to the handler so missing/null parent integrity can be distinguished from a missing lesson. | Legacy DDL candidate; FK/nullability/live schema unresolved |
| uploads AS u | LEFT JOIN | u.id = lesson_uploads.upload_id plus owner/purpose/course scope | Preserve link row visibility when metadata does not satisfy scope; handler treats unresolved link as integrity failure. | Migration 005 and API #34 source; live schema unresolved |

No JOIN to resources or V1-PILOT file_objects is used.

### 2.3. WHERE

| Condition | Value source | Purpose | Evidence |
|---|---|---|---|
| lessons.id = :lecture_id | Required path lecture_id | Resolve one lecture | Contract direct; table mapping candidate |
| Parent `courses.mentor_id` comparison | Authenticated principal | Direct-owner access, after Q1 | Runtime matches #46/#47; assigned courses cannot be resolved |

No PUBLISHED condition is applied. API #48 must remain consistent with the AC-21 #47 create-and-reload sequence.

### 2.4. ORDER BY

Q2 orders assets by `lesson_uploads.asset_position`, then upload ID; Q1 resolves at most one lecture and needs no ordering.

## 3. Insert/Update thông tin

### 3.1. Target table

N/A — API #48 is read-only.

### 3.2. Conditions

N/A — không có điều kiện ghi dữ liệu.

### 3.3. Items update/insert

N/A — không có INSERT/UPDATE/DELETE. API #47 owns the preceding candidate lesson insert.

### 3.4. Parameters

N/A — không có mutation parameters.

#### Mutation Matrix

| Mutation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | API is read-only | No INSERT/UPDATE/DELETE | N/A — READ-ONLY API |

## Response Source Matrix

| Response field | Contract type | Source | Transform/null rule | Status |
|---|---|---|---|---|
| data.id | int64 | lessons.id | Direct | Legacy DDL; live schema unknown |
| data.course_id | int64 | lessons.course_id | Required; NULL blocks response | DDL/guide discrepancy; runtime returns 500 |
| data.title | string | lessons.name | Alias name to title | Checked-in legacy mapping |
| data.content | string? | lessons.content | Preserve text; SQL NULL serializes as JSON null | Runtime model and response |
| data.assets[] | UploadAsset[] | lesson_uploads + uploads | Resolve linked rows in asset_position order; no links → `[]` | Checked-in migration/source; live schema unknown |
| data.assets[].id | int64 | uploads.id | Direct | API #34 persisted metadata |
| data.assets[].name | string | uploads.file_name | Alias file_name to name | API #34 persisted metadata |
| data.assets[].url | uri | uploads.url | Direct | API #34 persisted metadata |
| data.assets[].content_type | string | uploads.content_type | Direct | API #34 persisted metadata |
| data.assets[].size_bytes | int64 | uploads.size_bytes | Direct | API #34 persisted metadata |
| data.assets[].status | UploadStatus | uploads.status | Return stored value | Runtime string model; enum members unspecified |
| data.order | int32 | lessons.sort_order | Alias sort_order to order | Checked-in legacy mapping |
| data.status | LessonStatus | lessons.status | Return stored value for non-DELETED Lesson | Runtime string model; enum members unspecified |
| success | boolean | Branch result | true for success, false for error | Envelope convention |
| businessCode | string | API catalog | Exact code for branch | DIRECT |
| message | string | Application | Safe localized text | Exact message unspecified |
| meta | object | API Guidelines/helper | {} | Runtime helper |
| traceId | uuid | Request trace | Propagate trace ID | API Guidelines |

## 4. Check kết quả execute query

### 4.1. Thành công

- Trả 200 DESIGN_RESOURCE_RETRIEVED khi lesson row, parent course và mọi linked upload metadata ánh xạ hợp lệ.
- Assets lấy từ lesson_uploads/uploads; không có link thì trả `[]`.
- SQL NULL content được serialize thành JSON null.

### 4.2. Lỗi hệ thống

- DB query lỗi, parent thiếu, upload link không resolve được trong scope, hoặc row không đủ dữ liệu bắt buộc: 500 DESIGN_INTERNAL_ERROR.
- Không trả chi tiết SQL, exception hoặc schema nội bộ.

### 4.3. Validate lỗi

- Catalog API #48 không khai báo 422 hoặc DESIGN_VALIDATION_ERROR.
- Runtime maps malformed/out-of-range lecture_id to 404 DESIGN_RESOURCE_NOT_FOUND; this remains an implementation decision for confirmation.

### 4.4. Ngoài trường hợp trên

- Không dùng thêm 409, 503 hoặc business code khác catalog.
- Lỗi không thuộc các nhánh đã định nghĩa phải được xử lý an toàn thành 500 DESIGN_INTERNAL_ERROR nếu được xác nhận bởi implementation owner.

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
