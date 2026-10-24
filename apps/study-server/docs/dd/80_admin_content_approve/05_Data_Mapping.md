---
title: "Data Mapping"
order: 5
dd_id: "80"
api_name: "Phê duyệt nội dung"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

0. Xác thực Bearer JWT và yêu cầu Admin role theo catalog.
1. Đọc content_id từ path; catalog không khai báo body hoặc query.
2. Đọc logical Content và trạng thái/revision cần review. Không có physical Content relation được chọn.
3. Đối chiếu eligibility với AC-33 pending-review precondition; kiểm tra status/revision cụ thể là proposal cần xác nhận.
4. Chọn đúng revision đã hiển thị trong #79. Catalog #80 không truyền revision ID hoặc expected row version nên selector/lock chưa thể xác định.
5. Thực hiện logical status update theo approve branch. AC-33 ghi APPROVED/PUBLISHED, nhưng không tách ý nghĩa hai trạng thái.
6. Ghi logical approval audit theo AC-33. Physical audit relation, fields và transaction atomicity chưa được xác nhận.
7. Trả HTTP 200 DESIGN_RESOURCE_UPDATED với một ApiEnvelope<Content> theo catalog; không thêm version/author fields.

<a id="step-0-check-quyen"></a>
## 0. Check quyền

### 0.1. Thực hiện check quyền

- Bearer JWT là yêu cầu direct từ catalog.
- Role Admin là yêu cầu direct từ catalog.
- Admin claim, identity key và scope policy là SOURCE_REQUIRED.
- Current shared Study guard chỉ xác thực Student; API #80 không có guard source.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| JWT principal | roles | Phải có Admin role | Logical requirement direct; claim parser/role spelling chưa có source cho Admin. |
| Content review target | content_id | Chỉ đọc/ghi sau Admin authorization | Physical Content relation và scope rule SOURCE_REQUIRED. |

### 0.3. Check kết quả

- Nếu Bearer và Admin authorization hợp lệ, tiếp tục.
- Nếu thiếu hoặc token không hợp lệ, catalog code là 401 DESIGN_AUTHENTICATION_REQUIRED.
- Nếu role hoặc access policy không đạt, catalog code là 403 DESIGN_ACCESS_DENIED.
- Thứ tự lookup so với authorization và concealment 403/404 chưa được xác nhận; xem [06_Error.md](./06_Error.md).

<a id="step-1-validate"></a>
## 1. Validate data input

- content_id là path parameter int64! theo [03_Request.md](./03_Request.md).
- Catalog không khai báo body hoặc query; không có request action/status/version field.
- Parse range, overflow và framework mapping cho path ID chưa được xác nhận.
- Catalog khai báo 422 DESIGN_VALIDATION_ERROR, nhưng không chỉ định điều kiện; không tự gắn code này với validation rule cụ thể.

<a id="step-2-get-thong-tin"></a>
## 2. Get thông tin

### 2.1. Query

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| Logical Content | id | Chọn item theo content_id | Logical query; physical table/key SOURCE_REQUIRED. |
| Logical Content | course_id | Course scope của item | Physical relation SOURCE_REQUIRED. |
| Logical Content | content_type | Response projection | Enum and storage SOURCE_REQUIRED. |
| Logical Content | title | Response projection | Physical source SOURCE_REQUIRED. |
| Logical Content | payload | Response projection | Schema/storage SOURCE_REQUIRED. |
| Logical Content | status | Kiểm tra trạng thái hiện hành và response | Enum/transition SOURCE_REQUIRED. |
| Logical Content | parent_id | Response projection | Relation/null behavior SOURCE_REQUIRED. |
| Logical Content | order | Response projection | Physical source SOURCE_REQUIRED. |
| Logical Content revision | revision identity | Giữ cùng revision được Admin review | No identifier in #80 contract; SOURCE_REQUIRED. |
| Admin principal | admin identity | Authorization/audit actor | JWT claim mapping SOURCE_REQUIRED. |

### 2.2. JOIN

| Target table | Join condition | Join type |
|---|---|---|
| Logical Content | N/A — relation/key chưa được chọn | SOURCE_REQUIRED |
| Logical Content revision | N/A — revision relation/key chưa được chọn | SOURCE_REQUIRED |

Không viết SQL hoặc JOIN theo Content/version tables chưa được chọn.

### 2.3. WHERE

- Logical Content identity bằng content_id từ path; physical predicate/column SOURCE_REQUIRED.
- AC-33 queue precondition là status=PENDING_REVIEW; áp dụng lại như guard của #80 là DERIVED cần xác nhận.
- Nếu item đã rời pending hoặc revision đã đổi sau #79, branch/error mapping chưa được định nghĩa.

### 2.4. ORDER BY

- N/A cho một Content được chọn theo ID.
- Không chọn latest version hoặc current version khi chưa có rule.

<a id="step-3-mutation"></a>
## 3. Insert/Update thông tin

### 3.1. Target table

- Logical Content review/publication state — physical relation/column SOURCE_REQUIRED.
- Logical approval audit/decision record — physical relation/columns SOURCE_REQUIRED.
- V1-PILOT content_review_decisions là schema artifact UUID-based, không phải mapping được chọn cho Content ID int64.

### 3.2. Conditions

- AC-33 approve branch là nguồn direct cho status update và audit.
- Exact eligible state, transition target và version-lock condition cần xác nhận.
- Không tự quyết định approve có publish luôn hay chỉ đặt APPROVED.

### 3.3. Items update/insert

- Logical status update và audit gap register: [07_table.md](./07_table.md).

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| content_id | Path content_id | Direct input; physical bind key SOURCE_REQUIRED. |
| admin_actor | Authenticated Admin | Actor identity source/claim mapping SOURCE_REQUIRED. |
| reviewed_revision | Revision shown by #79 | No revision ID in request; selector SOURCE_REQUIRED. |
| target_status | AC-33 text APPROVED/PUBLISHED | Exact target unresolved; do not persist as a fixed value yet. |
| trace_id | Request trace | Envelope/security convention; audit column mapping SOURCE_REQUIRED. |

<a id="step-4-result"></a>
## 4. Check kết quả execute query

### 4.1. Thành công

- HTTP status 200.
- businessCode = DESIGN_RESOURCE_UPDATED.
- Trả một Content object với đúng tám field catalog khai báo theo [04_Response.md](./04_Response.md).
- Không thêm version, author, reviewer, reason hoặc audit fields vào response.

### 4.2. Lỗi hệ thống

- Query/update/audit failure có thể map tới HTTP 500 DESIGN_INTERNAL_ERROR theo catalog.
- Rollback/atomicity giữa status write và audit append là TBD; xem [07_table.md](./07_table.md).

### 4.3. Validate lỗi

- Catalog cho phép HTTP 422 DESIGN_VALIDATION_ERROR.
- Trigger và field-level error projection chưa được định nghĩa; không tự tạo state-transition rule hoặc meta.fieldErrors cụ thể.

### 4.4. Ngoài trường hợp trên

- Không trả business code ngoài contract.
- Error envelope theo API guideline dùng data:null; current helper mặc định {} khi caller không truyền data; endpoint chưa được wire.

## Liên kết nguồn và điểm còn mở

- [AC-33 diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [AC-22 API #52 Overview](../52_mentor_content_publish/02_Overview.md)
- [API #79 version/author questions](../79_admin_content_detail/OPEN_QUESTIONS.md)
- [Open questions #80](./OPEN_QUESTIONS.md)
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
