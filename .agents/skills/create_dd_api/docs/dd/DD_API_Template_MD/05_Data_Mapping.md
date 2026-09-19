---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

## 0. Check quyền

### 0.1. Thực hiện check quyền

- `<MÔ_TẢ_NGUỒN_QUYỀN>`.
- `<MỖI_ROLE_OR_FUNCTION_ID_MỘT_DÒNG>`.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| `<TABLE_OR_API>` | `<FIELD>` | `<CONDITION_OR_VALUE>` | `<REMARKS>` |

### 0.3. Check kết quả

- Nếu kết quả lớn hơn `0`:
  - Tiếp tục xử lý.
- Nếu kết quả bằng `0`:
  - Trả lỗi theo [06_Error.md](./06_Error.md).

## 1. Validate data input

- Validate từng field theo [03_Request.md](./03_Request.md).
- Chi tiết lỗi refer [06_Error.md](./06_Error.md).

## 2. Get thông tin

### 2.1. Query

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `<TABLE> AS <ALIAS>` | `<ALIAS>.<COLUMN_1>` | `<LOGICAL_NAME_1>` | |
| `↑` | `<ALIAS>.<COLUMN_2>` | `<LOGICAL_NAME_2>` | |

### 2.2. JOIN

| Target table | Join condition | Join type |
|---|---|---|
| `<BASE_TABLE> AS a` | `N/A` | `BASE` |
| `<JOIN_TABLE> AS b` | `b.id = a.b_id` | `LEFT JOIN` |

### 2.3. WHERE

- `<CONDITION_1>`.
- `<CONDITION_2>`.

### 2.4. ORDER BY

- `<COLUMN> ASC`.

## 3. Insert/Update thông tin

### 3.1. Target table

- `<TABLE>`.

### 3.2. Conditions

- `<TABLE>.<KEY> = <SOURCE>`.

### 3.3. Items update/insert

- Refer [07_table.md](./07_table.md).

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| `<PARAM_1>` | `<SOURCE_1>` | `<REMARKS_1>` |

## 4. Check kết quả execute query

### 4.1. Thành công

- `HTTPStatus = 200`.
- `status = 1`.
- Map từng response field theo [04_Response.md](./04_Response.md).

### 4.2. Lỗi hệ thống

- `HTTPStatus = 500`.
- `status = 2`.
- Error detail refer [06_Error.md](./06_Error.md).

### 4.3. Validate lỗi

- `HTTPStatus = 400`.
- `status = 2`.
- Error detail refer [06_Error.md](./06_Error.md).

### 4.4. Ngoài trường hợp trên

- `status = 2`.

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
