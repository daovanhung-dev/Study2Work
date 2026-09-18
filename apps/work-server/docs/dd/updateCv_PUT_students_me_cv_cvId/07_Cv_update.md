---
title: "Định nghĩa table"
order: 7
dd_id: "updateCv"
api_name: "cv.view.updateCv"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
status: "Draft — Ready for Review"
---
# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
| ---: | --- |
| Prisma model | Cv |
| Operation | UPDATE |
| Transaction | Prisma $transaction |
| Status | Draft — Ready for Review |

## Field mapping

| No | DB column | Operation | Value source | Prisma/schema type |
| ---: | --- | --- | --- | --- |
| 1 | avt | UPDATE | normalized input when present | VARCHAR(191) |
| 2 | hoten | UPDATE | normalized input when present | VARCHAR(191) |
| 3 | ngaysinh | UPDATE | normalized input when present | TIMESTAMPTZ(3) |
| 4 | gioitinh | UPDATE | normalized input when present | VARCHAR(191) |
| 5 | email | UPDATE | normalized input when present | VARCHAR(191) |
| 6 | sdt | UPDATE | normalized input when present | VARCHAR(191) |
| 7 | diachi | UPDATE | normalized input when present | VARCHAR(191) |
| 8 | vitri | UPDATE | normalized input when present | VARCHAR(191) |
| 9 | nganh | UPDATE | normalized input when present | VARCHAR(191) |
| 10 | muctieunghiep | UPDATE | normalized input when present | VARCHAR(191) |
| 11 | hocvan | UPDATE | normalized input when present | VARCHAR(191) |
| 12 | kinhnghiem | UPDATE | normalized input when present | VARCHAR(191) |
| 13 | kynang | UPDATE | normalized input when present | VARCHAR(191) |
| 14 | ngoaingu | UPDATE | normalized input when present | VARCHAR(191) |
| 15 | chungchi | UPDATE | normalized input when present | VARCHAR(191) |
| 16 | duan | UPDATE | normalized input when present | VARCHAR(191) |
| 17 | giaithuong | UPDATE | normalized input when present | VARCHAR(191) |
| 18 | hoatdong | UPDATE | normalized input when present | VARCHAR(191) |
| 19 | social | UPDATE | normalized input when present | JSONB |
| 20 | portfolio | UPDATE | normalized input when present | VARCHAR(191) |
| 21 | luongmongmuon | UPDATE | normalized input when present | VARCHAR(191) |

## Insert/Update/Delete behavior

- Partial update does not update unspecified fields.
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
