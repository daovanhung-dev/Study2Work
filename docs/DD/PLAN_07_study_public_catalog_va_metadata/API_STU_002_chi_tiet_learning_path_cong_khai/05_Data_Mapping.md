---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "API-STU-002"
status: "PARTIALLY COMPLETED — SOURCE GAPS"
---

# Data Mapping

## Flow xử lý data

## 0. Check quyền

### 0.1. Thực hiện check quyền

- `N/A — Public/Anonymous`; vẫn áp dụng rate limit, validation và anti-enumeration theo contract.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| `study_db` | `principal/resource scope` | `Public` | Không dùng frontend guard làm hàng rào bảo mật |

### 0.3. Check kết quả

- Nếu authentication/authorization hợp lệ: tiếp tục xử lý.
- Nếu không hợp lệ: trả error branch tương ứng trong [06_Error.md](./06_Error.md).

## 1. Validate data input

- `Path.slug`: required=`Yes`, type=`string`, format=`lowercase kebab-case`, valid=`N/A`; basis=`DIRECT`.

## 2. Get thông tin

### 2.1. Query `TBL-STU-009 — learning_paths`

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `learning_paths AS t_learning` | `t_learning.id` | `id` | `DIRECT` |
| `learning_paths AS t_learning` | `t_learning.slug` | `slug` | `DIRECT` |
| `learning_paths AS t_learning` | `t_learning.latest_published_version_id` | `latest_published_version_id` | `DIRECT` |
| `learning_paths AS t_learning` | `t_learning.archived_at` | `archived_at` | `DIRECT` |

**WHERE / predicate cho `learning_paths`**

- `slug = request.path.slug`.

### 2.2. Query `TBL-STU-010 — learning_path_versions`

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `learning_path_versions AS t_learning` | `t_learning.id` | `id` | `DIRECT` |
| `learning_path_versions AS t_learning` | `t_learning.path_id` | `path_id` | `DIRECT` |
| `learning_path_versions AS t_learning` | `t_learning.version_no` | `version_no` | `DIRECT` |
| `learning_path_versions AS t_learning` | `t_learning.status` | `status` | `DIRECT` |
| `learning_path_versions AS t_learning` | `t_learning.title` | `title` | `DIRECT` |
| `learning_path_versions AS t_learning` | `t_learning.summary` | `summary` | `DIRECT` |
| `learning_path_versions AS t_learning` | `t_learning.estimated_hours` | `estimated_hours` | `DIRECT` |
| `learning_path_versions AS t_learning` | `t_learning.published_at` | `published_at` | `DIRECT` |
| `learning_path_versions AS t_learning` | `t_learning.content_hash` | `content_hash` | `DIRECT` |

**WHERE / predicate cho `learning_path_versions`**

- `status = PUBLISHED` khi API public/chọn version yêu cầu published.

### 2.3. Query `TBL-STU-013 — path_course_items`

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `path_course_items AS t_pathcour` | `t_pathcour.path_version_id` | `path_version_id` | `DIRECT` |
| `path_course_items AS t_pathcour` | `t_pathcour.course_version_id` | `course_version_id` | `DIRECT` |
| `path_course_items AS t_pathcour` | `t_pathcour.position` | `position` | `DIRECT` |
| `path_course_items AS t_pathcour` | `t_pathcour.is_required` | `is_required` | `DIRECT` |
| `path_course_items AS t_pathcour` | `t_pathcour.unlock_rule` | `unlock_rule` | `DIRECT` |

**WHERE / predicate cho `path_course_items`**

- Điều kiện cụ thể theo endpoint summary và khóa/index canonical; exact SQL giữ `DERIVED` nếu catalog không nêu field-level.

### 2.4. Query `TBL-STU-012 — course_versions`

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `course_versions AS t_courseve` | `t_courseve.id` | `id` | `DIRECT` |
| `course_versions AS t_courseve` | `t_courseve.course_id` | `course_id` | `DIRECT` |
| `course_versions AS t_courseve` | `t_courseve.version_no` | `version_no` | `DIRECT` |
| `course_versions AS t_courseve` | `t_courseve.status` | `status` | `DIRECT` |
| `course_versions AS t_courseve` | `t_courseve.title` | `title` | `DIRECT` |
| `course_versions AS t_courseve` | `t_courseve.summary` | `summary` | `DIRECT` |
| `course_versions AS t_courseve` | `t_courseve.level` | `level` | `DIRECT` |
| `course_versions AS t_courseve` | `t_courseve.estimated_minutes` | `estimated_minutes` | `DIRECT` |
| `course_versions AS t_courseve` | `t_courseve.published_at` | `published_at` | `DIRECT` |
| `course_versions AS t_courseve` | `t_courseve.content_hash` | `content_hash` | `DIRECT` |

**WHERE / predicate cho `course_versions`**

- `status = PUBLISHED` khi API public/chọn version yêu cầu published.

### 2.5. Query `TBL-STU-058 — course_prerequisites`

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `course_prerequisites AS t_coursepr` | `t_coursepr.course_version_id` | `course_version_id` | `DIRECT` |

**WHERE / predicate cho `course_prerequisites`**

- Điều kiện cụ thể theo endpoint summary và khóa/index canonical; exact SQL giữ `DERIVED` nếu catalog không nêu field-level.

<a id="3-insertupdate-thong-tin"></a>
## 3. Insert/Update thông tin

### 3.1. Target table

- `N/A — READ-ONLY API`.

### 3.2. Conditions

- `N/A — READ-ONLY API`.

### 3.3. Items update/insert

- Refer [07_table.md](./07_table.md): `N/A — READ-ONLY API`.

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| `N/A` | `N/A` | READ-ONLY |

## 4. Check kết quả execute query

### 4.1. Thành công

- `HTTPStatus = 200`.
- `success = true`.
- `businessCode = SOURCE_REQUIRED` nếu success catalog chưa định nghĩa.
- Map từng response path theo [04_Response.md](./04_Response.md).
- `meta` luôn là object.
- `traceId` lấy từ request context.

### 4.2. Lỗi hệ thống

- `ROLLBACK` nếu transaction đã bắt đầu.
- `HTTPStatus = 500`.
- Không trả stack trace, SQL, token, secret hoặc private key reference.
- Refer [06_Error.md](./06_Error.md).

### 4.3. Validate lỗi

- Trả HTTP status/business code theo từng row trong [06_Error.md](./06_Error.md).
- Field-level error đặt tại `meta.fieldErrors` khi source định nghĩa field cụ thể.

### 4.4. Ngoài trường hợp trên

- Không silently ignore filter/field không được hỗ trợ.
- Gap `SOURCE_REQUIRED`, `CONFLICT` hoặc `NEEDS USER DECISION` không được biến thành runtime contract.

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
