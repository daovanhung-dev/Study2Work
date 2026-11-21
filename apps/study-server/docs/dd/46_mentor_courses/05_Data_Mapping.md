---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "46"
api_name: "Lấy course Mentor được quản lý"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

### 0. Check quyền

- Yêu cầu Bearer JWT hợp lệ và role `MENTOR` theo catalog.
- Principal lấy từ claim đã xác thực; current Study helper mới có guard Student, vì vậy chưa thể tái sử dụng như Mentor guard.
- Candidate query giới hạn course theo Mentor hiện tại. AC-21 nói owns/assigned; quan hệ assignment chưa có nguồn vật lý.

#### 0.1. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| JWT principal | `roles` | role phải là `MENTOR` | Contract trực tiếp; runtime guard chưa có. |
| `courses` | `mentor_id` | bằng numeric principal ID | Candidate direct ownership; `DERIVED`, không chứng minh course được phân công. |

### 1. Validate data input

- Giữ đúng ba query fields `status`, `page`, `size`.
- `status` chỉ được kiểm tra theo enum sau khi có member list; status không hợp lệ ánh xạ 422 theo catalog.
- Page range và size tối đa 100 là đề xuất `DERIVED` từ API #6.

#### 1.1 Validate status

| Field | Rule | Failure |
|---|---|---|
| `status` | Nếu có giá trị, phải là member CourseStatus đã được phê duyệt. | `422 DESIGN_VALIDATION_ERROR`; enum hiện `SOURCE_REQUIRED`. |

#### 1.2 Validate page

| Field | Rule | Failure |
|---|---|---|
| `page` | int32; đề xuất `>=1`; default `1`. | `422 DESIGN_VALIDATION_ERROR`; range `DERIVED`. |

#### 1.3 Validate size

| Field | Rule | Failure |
|---|---|---|
| `size` | int32; default `20`; đề xuất `1..100`. | `422 DESIGN_VALIDATION_ERROR`; max `DERIVED` từ API #6. |

### 2. Get course page

#### 2.1 Candidate Q1 — page query

| Item | Candidate source/rule | Evidence |
|---|---|---|
| `courses.id` | Chọn `c.id`. | Legacy DDL candidate; pilot ID conflict. |
| `courses.name` | Chọn `c.name AS title`. | API #6 mapping precedent. |
| `courses.description` | Chọn `c.description`. | Legacy candidate; nullable. |
| `courses.thumbnail_url` | Chọn `c.thumbnail_url`. | Legacy candidate; nullable. |
| `courses.price` | Chọn `c.price`; serialize decimal-string. | Required contract; legacy column nullable. |
| `courses.status` | Chọn `c.status`; giữ status source. | Enum values chưa có. |
| `users.id` | Join `m.id = c.mentor_id`; chọn `m.id`. | API #6 UserSummary precedent. |
| `users.full_name` | Chọn `m.full_name`. | Required UserSummary field. |
| `users.avatar_url` | Chọn `m.avatar_url`. | Optional UserSummary field. |
| Ownership predicate | `c.mentor_id = :mentor_id`. | Candidate `DERIVED`; assignment model chưa có. |
| Optional status predicate | Thêm `c.status = :status` chỉ khi status được gửi. | Contract filter; predicate behavior `DERIVED`. |
| Sort field 1 | `c.created_at DESC`. | `DERIVED` theo API #6. |
| Sort field 2 | `c.id ASC`. | Stable tie-breaker `DERIVED` theo API #6. |
| Limit | `:size`. | Query/default contract; max proposal. |
| Offset | `(:page - 1) * :size`. | Pagination formula `DERIVED`. |

```sql
SELECT c.id, c.name AS title, c.description, c.thumbnail_url,
       c.price, c.status, m.id AS mentor_id,
       m.full_name AS mentor_full_name, m.avatar_url AS mentor_avatar_url
FROM courses AS c
LEFT JOIN users AS m ON m.id = c.mentor_id
WHERE c.mentor_id = :mentor_id
-- Nếu query status có giá trị, thêm: AND c.status = :status
ORDER BY c.created_at DESC, c.id ASC
LIMIT :size OFFSET (:page - 1) * :size;
```

> SQL chỉ là candidate legacy mapping. Binding, bảng đang chạy và direct-owner predicate chưa được xác nhận.

#### 2.2 Candidate Q2 — total query

| Item | Candidate source/rule | Evidence |
|---|---|---|
| Count expression | `COUNT(*)`. | API #6 pattern. |
| Owner predicate | Cùng `c.mentor_id = :mentor_id` như Q1. | Candidate `DERIVED`. |
| Optional status predicate | Thêm `c.status = :status` chỉ khi status được gửi. | Phải khớp Q1. |
| Mentor integrity count | `COUNT(*) FILTER (WHERE m.id IS NULL)`. | API #6 precedent; required mentor projection. |

```sql
SELECT COUNT(*) AS total,
       COUNT(*) FILTER (WHERE m.id IS NULL) AS missing_mentor_count
FROM courses AS c
LEFT JOIN users AS m ON m.id = c.mentor_id
WHERE c.mentor_id = :mentor_id
-- Nếu query status có giá trị, thêm: AND c.status = :status
;
```

### 3. Map response

| Contract field | Candidate source | Mapping/rule |
|---|---|---|
| `Course.title` | `courses.name` | Alias physical `name` thành logical `title`. |
| `Course.price` | `courses.price` | Decimal-safe serialization; NULL là integrity gap. |
| `Course.mentor` | `users` | Join theo legacy `mentor_id`; bắt buộc có `id` và `full_name`. |
| `Course.category` | N/A | Omit optional field; không có relation course-category. |
| `Page.total_pages` | `total`, `size` | `ceil(total / size)`; 0 khi total=0 (`DERIVED`). |
| Empty page | Q1/Q2 | Trả 200, `items: []`; out-of-range page là empty (`DERIVED`). |

### 4. Transaction and response

- Read-only; không có INSERT/UPDATE/DELETE.
- Không ghi thêm PUBLISHED predicate khi catalog/AC-21 không yêu cầu.
- Response dùng envelope `ApiEnvelope<Page<Course>>` với HTTP 200 và business code catalog.
- Lỗi dùng đúng catalog 401/403/422/500; xem [06_Error.md](./06_Error.md).
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
