---
title: "Định nghĩa table"
order: 7
dd_id: "createBusinessJob"
api_name: "Create business job"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---
# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `JD` |
| Logical table | JD |
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
| 2 | ten_vi_tri | ten_vi_tri | VARCHAR | 191 | N/A | Y |  | `request["ten_vi_tri"]` if defined | request/form/token | `5.1` |  |
| 3 | phong_ban | phong_ban | VARCHAR | 191 | N/A | N |  | `request["phong_ban"]` if defined | request/form/token | `5.1` |  |
| 4 | cap_bac | cap_bac | VARCHAR | 191 | N/A | N |  | `request["cap_bac"]` if defined | request/form/token | `5.1` |  |
| 5 | bao_cao_cho | bao_cao_cho | VARCHAR | 191 | N/A | N |  | `request["bao_cao_cho"]` if defined | request/form/token | `5.1` |  |
| 6 | nhiem_vu | nhiem_vu | VARCHAR | 191 | N/A | N |  | `request["nhiem_vu"]` if defined | request/form/token | `5.1` |  |
| 7 | trinh_do | trinh_do | VARCHAR | 191 | N/A | N |  | `request["trinh_do"]` if defined | request/form/token | `5.1` |  |
| 8 | kinh_nghiem | kinh_nghiem | VARCHAR | 191 | N/A | N |  | `request["kinh_nghiem"]` if defined | request/form/token | `5.1` |  |
| 9 | ky_nang | ky_nang | VARCHAR | 191 | N/A | N |  | `request["ky_nang"]` if defined | request/form/token | `5.1` |  |
| 10 | ky_nang_mem | ky_nang_mem | VARCHAR | 191 | N/A | N |  | `request["ky_nang_mem"]` if defined | request/form/token | `5.1` |  |
| 11 | uu_tien | uu_tien | VARCHAR | 191 | N/A | N |  | `request["uu_tien"]` if defined | request/form/token | `5.1` |  |
| 12 | muc_luong | muc_luong | VARCHAR | 191 | N/A | N |  | `request["muc_luong"]` if defined | request/form/token | `5.1` |  |
| 13 | phuc_loi | phuc_loi | VARCHAR | 191 | N/A | N |  | `request["phuc_loi"]` if defined | request/form/token | `5.1` |  |
| 14 | moi_truong | moi_truong | VARCHAR | 191 | N/A | N |  | `request["moi_truong"]` if defined | request/form/token | `5.1` |  |
| 15 | dia_diem | dia_diem | VARCHAR | 191 | N/A | N |  | `request["dia_diem"]` if defined | request/form/token | `5.1` |  |
| 16 | thoi_gian | thoi_gian | VARCHAR | 191 | N/A | N |  | `request["thoi_gian"]` if defined | request/form/token | `5.1` |  |
| 17 | han_nop | han_nop | VARCHAR | 191 | N/A | N |  | `request["han_nop"]` if defined | request/form/token | `5.1` |  |
| 18 | cach_ung_tuyen | cach_ung_tuyen | VARCHAR | 191 | N/A | N |  | `request["cach_ung_tuyen"]` if defined | request/form/token | `5.1` |  |
| 19 | mo_ta | mo_ta | VARCHAR | 191 | N/A | N |  | `request["mo_ta"]` if defined | request/form/token | `5.1` |  |
| 20 | ten_cong_ty | ten_cong_ty | VARCHAR | 191 | N/A | N |  | `request["ten_cong_ty"]` if defined | request/form/token | `5.1` |  |
| 21 | nganh | nganh | VARCHAR | 191 | N/A | N |  | `request["nganh"]` if defined | request/form/token | `5.1` |  |
| 22 | avt | avt | VARCHAR | 191 | N/A | N |  | `/uploads/${req.file.filename}` | request/form/token | `5.1` | JD stores `/uploads/` prefix |
| 23 | doanhnghiep_id | Business owner ID | BIGINT | N/A | N/A | N |  | `req.user.id` | JWT claim | `5.1` | FK; request cannot override owner |
| 24 | ngay_tao | Created at | TIMESTAMPTZ | 3 | N/A | N |  | schema default | schema | `5.1` | Default now() |

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
