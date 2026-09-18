---
title: "Định nghĩa table"
order: 7
dd_id: "createBusinessJob"
api_name: "jobs.view.createBusinessJob"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
status: "Draft — Ready for Review"
---
# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
| ---: | --- |
| Prisma model | JD |
| Operation | INSERT |
| Transaction | Prisma $transaction |
| Status | Draft — Ready for Review |

## Field mapping

| No | DB column | Operation | Value source | Prisma/schema type |
| ---: | --- | --- | --- | --- |
| 1 | ten_vi_tri | INSERT | normalized request field when present | VARCHAR(191) |
| 2 | phong_ban | INSERT | normalized request field when present | VARCHAR(191) |
| 3 | cap_bac | INSERT | normalized request field when present | VARCHAR(191) |
| 4 | bao_cao_cho | INSERT | normalized request field when present | VARCHAR(191) |
| 5 | nhiem_vu | INSERT | normalized request field when present | VARCHAR(191) |
| 6 | trinh_do | INSERT | normalized request field when present | VARCHAR(191) |
| 7 | kinh_nghiem | INSERT | normalized request field when present | VARCHAR(191) |
| 8 | ky_nang | INSERT | normalized request field when present | VARCHAR(191) |
| 9 | ky_nang_mem | INSERT | normalized request field when present | VARCHAR(191) |
| 10 | uu_tien | INSERT | normalized request field when present | VARCHAR(191) |
| 11 | muc_luong | INSERT | normalized request field when present | VARCHAR(191) |
| 12 | phuc_loi | INSERT | normalized request field when present | VARCHAR(191) |
| 13 | moi_truong | INSERT | normalized request field when present | VARCHAR(191) |
| 14 | dia_diem | INSERT | normalized request field when present | VARCHAR(191) |
| 15 | thoi_gian | INSERT | normalized request field when present | VARCHAR(191) |
| 16 | han_nop | INSERT | normalized request field when present | VARCHAR(191) |
| 17 | cach_ung_tuyen | INSERT | normalized request field when present | VARCHAR(191) |
| 18 | mo_ta | INSERT | normalized request field when present | VARCHAR(191) |
| 19 | ten_cong_ty | INSERT | normalized request field when present | VARCHAR(191) |
| 20 | nganh | INSERT | normalized request field when present | VARCHAR(191) |
| 21 | avt | INSERT | `/uploads/` + file filename | VARCHAR(191) |
| 22 | doanhnghiep_id | INSERT | BigInt(token.id) | BigInt |

## Insert/Update/Delete behavior

- ten_cong_ty uses input value or business.hoten.
- Prisma default supplies id and ngay_tao.


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
