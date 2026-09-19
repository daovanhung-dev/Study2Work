---
title: "Định nghĩa table"
order: 7
dd_id: "updateBusinessJob"
api_name: "jobs.view.updateBusinessJob"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
status: "Draft — Ready for Review"
---
# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
| ---: | --- |
| Prisma model | JD |
| Operation | UPDATE |
| Transaction | Prisma $transaction |
| Status | Draft — Ready for Review |

## Field mapping

| No | DB column | Operation | Value source | Prisma/schema type |
| ---: | --- | --- | --- | --- |
| 1 | ten_vi_tri | UPDATE | normalized input when present | VARCHAR(191) |
| 2 | phong_ban | UPDATE | normalized input when present | VARCHAR(191) |
| 3 | cap_bac | UPDATE | normalized input when present | VARCHAR(191) |
| 4 | bao_cao_cho | UPDATE | normalized input when present | VARCHAR(191) |
| 5 | nhiem_vu | UPDATE | normalized input when present | VARCHAR(191) |
| 6 | trinh_do | UPDATE | normalized input when present | VARCHAR(191) |
| 7 | kinh_nghiem | UPDATE | normalized input when present | VARCHAR(191) |
| 8 | ky_nang | UPDATE | normalized input when present | VARCHAR(191) |
| 9 | ky_nang_mem | UPDATE | normalized input when present | VARCHAR(191) |
| 10 | uu_tien | UPDATE | normalized input when present | VARCHAR(191) |
| 11 | muc_luong | UPDATE | normalized input when present | VARCHAR(191) |
| 12 | phuc_loi | UPDATE | normalized input when present | VARCHAR(191) |
| 13 | moi_truong | UPDATE | normalized input when present | VARCHAR(191) |
| 14 | dia_diem | UPDATE | normalized input when present | VARCHAR(191) |
| 15 | thoi_gian | UPDATE | normalized input when present | VARCHAR(191) |
| 16 | han_nop | UPDATE | normalized input when present | VARCHAR(191) |
| 17 | cach_ung_tuyen | UPDATE | normalized input when present | VARCHAR(191) |
| 18 | mo_ta | UPDATE | normalized input when present | VARCHAR(191) |
| 19 | ten_cong_ty | UPDATE | normalized input when present | VARCHAR(191) |
| 20 | nganh | UPDATE | normalized input when present | VARCHAR(191) |
| 21 | avt | UPDATE | `/uploads/` + file filename | VARCHAR(191) |

## Insert/Update/Delete behavior

- Only normalized fields present in request are updated.
- Ownership check and update share the transaction.


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
