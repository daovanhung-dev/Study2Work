---
title: "Data Mapping"
order: 5
dd_id: "75"
api_name: "Cập nhật metadata khóa học Admin"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Xác thực Bearer JWT và yêu cầu role Admin cùng course-management permission theo catalog/AC-32.
- Study runtime hiện chỉ có guard Student; claim mapping và permission policy của Admin là `SOURCE_REQUIRED`.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Admin auth provider/guard | JWT claims and permission | `Admin` + course-management permission | No Study source; do not reuse Student guard. |

### 0.3. Check kết quả

- Nếu token hợp lệ và có quyền: tiếp tục bước 1.
- Thiếu/sai token: trả 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Token hợp lệ nhưng không có role/permission: trả 403 `DESIGN_ACCESS_DENIED`.

## 1. Validate data input

- Validate `course_id` theo required int64 của catalog; positive/range boundary ngoài int64 chưa được chỉ định thêm.
- Body full replacement với bốn field là proposal `DERIVED`, chưa thuộc direct catalog contract.
- Validate từng body field chỉ theo rules được duyệt; catalog cung cấp nhánh 422 nhưng không nêu field constraints.
- Chi tiết lỗi refer [06_Error.md](./06_Error.md).

## 2. Get thông tin

### 2.1. Q1 — Update metadata

Q1 là candidate trên legacy BIGINT `courses`; live schema chưa xác minh.

| Target table | Column get/update | Chú thích | Remarks |
|---|---|---|---|
| `courses AS c` | `c.name` | Set từ request `title`. | Legacy candidate. |
| `courses AS c` | `c.description` | Set từ request `description`; null clears in proposal. | Legacy candidate. |
| `courses AS c` | `c.thumbnail_url` | Set từ request `thumbnail_url`; null clears in proposal. | Legacy candidate. |
| `courses AS c` | `c.price` | Set từ request decimal-string `price`. | Legacy candidate; column nullable. |
| `courses AS c` | `c.updated_at` | Set server timestamp. | DERIVED; current DB writer pattern needs approval. |
| `courses AS c` | `c.status` | Not changed. | Owned by #76. |
| `courses AS c` | `c.mentor_id` | Not changed. | Owner transfer absent from #75 contract. |

### 2.2. JOIN / Q2 — Response projection

| Target table | Join condition | Join type |
|---|---|---|
| `courses AS c` | `c.id = :course_id` | BASE / ID predicate |
| `users AS m` | `m.id = c.mentor_id` | LEFT JOIN candidate |

### 2.3. WHERE

- Q1 updates only where `c.id = :course_id`.
- Q2 selects only the row returned by Q1 / matching `c.id = :course_id`.
- No `status = 'PUBLISHED'` predicate; Admin path manages all statuses.
- No category or counter join/query is defined.

### 2.4. ORDER BY

- N/A — key lookup returns at most one course.

## 3. Insert/Update thông tin

### 3.1. Target table

- Candidate: legacy `courses`; legacy DDL is design artifact and does not establish live schema.

### 3.2. Conditions

- `courses.id = :course_id`.

### 3.3. Items update

- Refer [07_table.md](./07_table.md).
- Do not set `status`, `mentor_id`, `category_id` or counters.

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| `:course_id` | path `course_id` | Required int64; direct contract. |
| `:title` | body `title` | Metadata field proposal `DERIVED`. |
| `:description` | body `description` | Full-replacement proposal; null clears. |
| `:thumbnail_url` | body `thumbnail_url` | Full-replacement proposal; null clears. |
| `:price` | body `price` as exact decimal | Preserve decimal precision; limits unresolved. |
| `:updated_at` | server current timestamp | Proposal; legacy column candidate. |

### 3.5. Check kết quả

- Nếu Q1 không update row: rollback transaction và trả 404 `DESIGN_RESOURCE_NOT_FOUND` (candidate branch).
- Nếu Q1 update được row: đọc Q2 và map Course fields cùng UserSummary.
- Nếu owner không map được vào required `Course.mentor`: trả candidate 500; orphan policy cần chốt.
- Nếu mapping hợp lệ: tạo `Page<Course>` singleton proposal, commit transaction và trả success envelope.
- Nếu DB, mapping hoặc commit lỗi sau khi bắt đầu transaction: rollback và trả 500 `DESIGN_INTERNAL_ERROR`.

## 4. Check kết quả execute query

### 4.1. Thành công

- `HTTPStatus = 200`.
- `businessCode = DESIGN_RESOURCE_UPDATED`.
- `data.items` chứa một Course vừa cập nhật; singleton cardinality là `DERIVED` theo API #74.
- `data.pagination = {page: 1, size: 1, total: 1, total_pages: 1}` là `DERIVED`.
- Map từng field theo [04_Response.md](./04_Response.md).
- Commit sau khi response projection được xác thực; transaction design là proposal.

### 4.2. Lỗi

- 401/403 theo bước 0; không truy vấn hoặc mutate course khi chưa được authorize.
- 422 theo bước 1; không bắt đầu mutation khi validation fail.
- 404 khi Q1 không tìm thấy row; rollback transaction candidate.
- 500 khi query, projection, transaction hoặc commit thất bại; rollback nếu transaction đã mở.
- Mỗi business code và data mapping xem [06_Error.md](./06_Error.md).
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
