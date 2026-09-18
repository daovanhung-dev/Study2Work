---
title: "Định nghĩa table"
order: 7
dd_id: "createCv"
api_name: "Create CV"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---
# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `Cv` |
| Logical table | Cv |
| Operation | INSERT |
| Data Mapping step | `5.1` |

## Update mapping

**Áp dụng khi**

- N/A — operation hiện tại không phải UPDATE.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

## Insert mapping

**Áp dụng khi**

- Validation/duplicate branch đã pass.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | id | ID | BIGINT | N/A | N/A | N | ● | autoincrement/no change | schema default | `5.1` | Generated or existing key |
| 2 | hoten | hoten | VARCHAR | 191 | N/A | Y |  | `request["hoten"]` if defined | request/form/token | `5.1` | Source maps only defined fields |
| 3 | ngaysinh | ngaysinh | TIMESTAMPTZ | 3 | N/A | N |  | `new Date(request["ngaysinh"])` if truthy; null if key exists but falsy | request/form/token | `5.1` | Source maps only defined fields |
| 4 | gioitinh | gioitinh | VARCHAR | 191 | N/A | N |  | `request["gioitinh"]` if defined | request/form/token | `5.1` | Source maps only defined fields |
| 5 | email | email | VARCHAR | 191 | N/A | Y |  | `request["email"]` if defined | request/form/token | `5.1` | Source maps only defined fields |
| 6 | sdt | sdt | VARCHAR | 191 | N/A | N |  | `request["sdt"]` if defined | request/form/token | `5.1` | Source maps only defined fields |
| 7 | diachi | diachi | VARCHAR | 191 | N/A | N |  | `request["diachi"]` if defined | request/form/token | `5.1` | Source maps only defined fields |
| 8 | vitri | vitri | VARCHAR | 191 | N/A | N |  | `request["vitri"]` if defined | request/form/token | `5.1` | Source maps only defined fields |
| 9 | nganh | nganh | VARCHAR | 191 | N/A | N |  | `request["nganh"]` if defined | request/form/token | `5.1` | Source maps only defined fields |
| 10 | muctieunghiep | muctieunghiep | VARCHAR | 191 | N/A | N |  | `request["muctieunghiep"]` if defined | request/form/token | `5.1` | Source maps only defined fields |
| 11 | hocvan | hocvan | VARCHAR | 191 | N/A | N |  | `request["hocvan"]` if defined | request/form/token | `5.1` | Source maps only defined fields |
| 12 | kinhnghiem | kinhnghiem | VARCHAR | 191 | N/A | N |  | `request["kinhnghiem"]` if defined | request/form/token | `5.1` | Source maps only defined fields |
| 13 | kynang | kynang | VARCHAR | 191 | N/A | N |  | `request["kynang"]` if defined | request/form/token | `5.1` | Source maps only defined fields |
| 14 | ngoaingu | ngoaingu | VARCHAR | 191 | N/A | N |  | `request["ngoaingu"]` if defined | request/form/token | `5.1` | Source maps only defined fields |
| 15 | chungchi | chungchi | VARCHAR | 191 | N/A | N |  | `request["chungchi"]` if defined | request/form/token | `5.1` | Source maps only defined fields |
| 16 | duan | duan | VARCHAR | 191 | N/A | N |  | `request["duan"]` if defined | request/form/token | `5.1` | Source maps only defined fields |
| 17 | giaithuong | giaithuong | VARCHAR | 191 | N/A | N |  | `request["giaithuong"]` if defined | request/form/token | `5.1` | Source maps only defined fields |
| 18 | hoatdong | hoatdong | VARCHAR | 191 | N/A | N |  | `request["hoatdong"]` if defined | request/form/token | `5.1` | Source maps only defined fields |
| 19 | social | social | JSONB | N/A | N/A | N |  | `JSON.parse(request["social"])` if parse succeeds; otherwise original value | request/form/token | `5.1` | Source maps only defined fields |
| 20 | portfolio | portfolio | VARCHAR | 191 | N/A | N |  | `request["portfolio"]` if defined | request/form/token | `5.1` | Source maps only defined fields |
| 21 | luongmongmuon | luongmongmuon | VARCHAR | 191 | N/A | N |  | `request["luongmongmuon"]` if defined | request/form/token | `5.1` | Source maps only defined fields |
| 22 | avt | avt | VARCHAR | 191 | N/A | N |  | `req.file?.filename` if file exists | request/form/token | `5.1` | Source maps only defined fields |
| 23 | sinhvien_id | Student owner | BIGINT | N/A | N/A | N |  | `req.user.id` | JWT claim | `5.1` | Unique FK |

## Delete mapping

**Áp dụng khi**

- N/A — operation hiện tại không phải DELETE.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---|---|---|---|---|---|
| 1 | N/A | N/A | N/A | N/A | N/A |
---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `table`
- Dimension: `A1:BA35`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `19`
- Số vùng merge: `5`

<details>
<summary>Danh sách vùng merge</summary>

- `W34:BA34`
- `W14:BA14`
- `W15:BA15`
- `W19:BA19`
- `W32:BA32`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `A2` | № |  |
| 2 | `B2` | Tên table |  |
| 3 | `B3` | SB |  |
| 3 | `S3` | Độ dài |  |
| 3 | `T3` | Dấu phẩy thập phân |  |
| 3 | `U3` | Bắt buộc |  |
| 3 | `V3` | Main key |  |
| 3 | `W3` | Nội dung setting |  |
| 4 | `B4` | № |  |
| 4 | `C4` | Item ID |  |
| 4 | `I4` | Item name |  |
| 4 | `O4` | Kiểu |  |
| 5 | `A5` | 1 |  |
| 5 | `B5` | table id |  |
| 5 | `I5` | table name |  |
| 6 | `B6` | Update |  |
| 6 | `I6` | Trường hợp số record get được từ xử lý 3. của sheet [３．Data mapping]  > 0 |  |
| 21 | `B21` | Insert |  |
| 21 | `I21` | Trường hợp số record get được từ xử lý 3. của sheet [３．Data mapping]  = 0 |  |

</details>
