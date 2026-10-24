---
title: "Data Mapping"
order: 5
dd_id: "81"
api_name: "Từ chối nội dung"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

0. Xác thực Bearer JWT và role Admin theo catalog.
1. Đọc path content_id và body reason; không có query.
2. Đọc logical Content, trạng thái hiện tại và revision được Admin xem trong #79. Không có physical Content/version relation được chọn.
3. Xác định target vẫn thuộc quy trình review. AC-33 precondition là pending review; recheck/stale behavior là proposal cần xác nhận.
4. Bảo đảm reason hiện diện theo body schema. Không thêm giới hạn/trim/blank-only validation chưa có nguồn.
5. Cập nhật logical Content status thành REJECTED và lưu review reason theo AC-33. Physical relation/columns và transaction chưa có nguồn.
6. Không tự thêm một audit append riêng cho #81; AC-33 reject node chỉ ghi status + review reason, còn #80 nêu + audit.
7. Trả HTTP 200 DESIGN_RESOURCE_UPDATED với một ApiEnvelope<Content>; response giữ đúng tám field catalog và không có reason/reviewer/version.

<a id="step-0-check-quyen"></a>
## 0. Check quyền

### 0.1. Thực hiện check quyền

- Bearer JWT là yêu cầu trực tiếp từ catalog.
- Role Admin là yêu cầu trực tiếp từ catalog.
- Admin claim, identity key và moderation scope là SOURCE_REQUIRED.
- Current shared Study guard chỉ xác thực Student; API #81 không có guard source.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| JWT principal | roles | Caller phải có Admin role | Logical requirement direct; claim parser/role spelling chưa có source cho Admin. |
| Content review target | content_id | Chỉ đọc/ghi sau Admin authorization | Physical Content relation và scope rule SOURCE_REQUIRED. |

### 0.3. Check kết quả

- Nếu Bearer và Admin authorization hợp lệ, tiếp tục.
- Nếu thiếu hoặc token không hợp lệ, catalog code là 401 DESIGN_AUTHENTICATION_REQUIRED.
- Nếu role hoặc access policy không đạt, catalog code là 403 DESIGN_ACCESS_DENIED.
- Thứ tự lookup và concealment 403/404 chưa được xác nhận; xem [06_Error.md](./06_Error.md).

<a id="step-1-validate"></a>
## 1. Validate data input

- content_id là required path int64 theo [03_Request.md](./03_Request.md).
- reason là required string trong body theo catalog.
- Missing body hoặc missing required reason là invalid request schema và dùng catalog 422 DESIGN_VALIDATION_ERROR.
- Length, trimming, blank-only, character set và reason taxonomy chưa được quy định.
- Catalog không khai báo query parameters.
- Parse range/overflow của path ID cần xác nhận khi route được wire.

<a id="step-2-get-thong-tin"></a>
## 2. Get thông tin

### 2.1. Query

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| Logical Content | id | Chọn target theo content_id | Logical lookup; physical table/key SOURCE_REQUIRED. |
| Logical Content | course_id | Course scope của target | Physical relation SOURCE_REQUIRED. |
| Logical Content | content_type | Response projection | Enum/storage SOURCE_REQUIRED. |
| Logical Content | title | Response projection | Physical source SOURCE_REQUIRED. |
| Logical Content | payload | Response projection | Schema/storage SOURCE_REQUIRED. |
| Logical Content | status | Review eligibility and result | Enum/state owner SOURCE_REQUIRED. |
| Logical Content | parent_id | Response projection | Relation/null behavior SOURCE_REQUIRED. |
| Logical Content | order | Response projection | Physical source SOURCE_REQUIRED. |
| Logical Content revision | revision identity | Bind rejection to item shown by #79 | No revision ID in #81 request; selector SOURCE_REQUIRED. |
| Admin principal | admin identity | Authorization and review trace | JWT claim mapping SOURCE_REQUIRED. |

### 2.2. JOIN

| Target table | Join condition | Join type |
|---|---|---|
| Logical Content | N/A — relation/key not selected | SOURCE_REQUIRED |
| Logical Content revision | N/A — revision relation/key not selected | SOURCE_REQUIRED |

Không viết SQL hoặc JOIN theo Content/version table chưa được chọn.

### 2.3. WHERE

- Logical Content identity bằng content_id từ path; physical predicate/column SOURCE_REQUIRED.
- AC-33 queue precondition là status=PENDING_REVIEW; áp dụng lại như #81 guard là DERIVED.
- Nếu target không tồn tại, catalog có 404 DESIGN_RESOURCE_NOT_FOUND.
- Nếu target đã rời pending hoặc revision đổi sau #79, error/status behavior chưa được AC-33/catalog xác định.

### 2.4. ORDER BY

- N/A cho một Content được chọn theo ID.
- Không chọn latest/current revision khi chưa có rule.

<a id="step-3-mutation"></a>
## 3. Insert/Update thông tin

### 3.1. Target table

- Logical Content status — physical relation/column SOURCE_REQUIRED.
- Logical rejection reason — storage field/relation SOURCE_REQUIRED.
- V1-PILOT content_review_decisions có comment/reason_codes nhưng UUID version identity; đây không phải mapping được chọn cho Content ID int64.

### 3.2. Conditions

- AC-33 reject branch là nguồn direct cho status REJECTED và review reason.
- Exact eligible state, revision selector và status-column ownership cần xác nhận.
- Chưa ghi một audit append riêng vì diagram reject node không nêu; parity với #80 vẫn là open question.

### 3.3. Items update/insert

- Logical status/reason update và physical gap register: [07_table.md](./07_table.md).

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| content_id | Path content_id | Direct input; physical bind key SOURCE_REQUIRED. |
| reason | Body reason | Required string direct; storage target/constraints SOURCE_REQUIRED. |
| admin_actor | Authenticated Admin | Identity source/claim mapping SOURCE_REQUIRED. |
| reviewed_revision | Revision shown by #79 | No revision ID in request; selector SOURCE_REQUIRED. |
| trace_id | Request trace | Envelope convention; audit column mapping not selected. |

<a id="step-4-result"></a>
## 4. Check kết quả execute query

### 4.1. Thành công

- HTTP status 200.
- businessCode = DESIGN_RESOURCE_UPDATED.
- Trả một Content object với đúng tám field catalog theo [04_Response.md](./04_Response.md).
- data.status phản ánh REJECTED theo logical diagram outcome.
- Không thêm reason, reviewer, version hoặc audit fields vào response.
- Vì #78 predicate là PENDING_REVIEW, target REJECTED không còn khớp queue predicate sau reload; đây là hệ quả logic của các bước direct.

### 4.2. Lỗi hệ thống

- Query/update/reason persistence failure có thể map tới HTTP 500 DESIGN_INTERNAL_ERROR theo catalog.
- Rollback và transaction giữa status/reason writes là TBD; xem [07_table.md](./07_table.md).

### 4.3. Validate lỗi

- Request schema thiếu body/required reason dùng HTTP 422 DESIGN_VALIDATION_ERROR theo catalog.
- Không tự thêm blank-only, length, format hoặc state-transition trigger.
- Field error details cần theo error guideline khi implementation được wire.

### 4.4. Ngoài trường hợp trên

- Không trả business code ngoài catalog.
- Error envelope theo API guideline dùng data:null; current helper mặc định {} khi caller không truyền data; endpoint chưa được wire.

## Liên kết nguồn và điểm còn mở

- [AC-33 diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [API #78 queue predicate](../78_admin_content_pending/05_Data_Mapping.md)
- [API #79 revision questions](../79_admin_content_detail/OPEN_QUESTIONS.md)
- [API #80 approval and audit questions](../80_admin_content_approve/OPEN_QUESTIONS.md)
- [API #52 publish status](../52_mentor_content_publish/OPEN_QUESTIONS.md)
- [Open questions #81](./OPEN_QUESTIONS.md)
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
