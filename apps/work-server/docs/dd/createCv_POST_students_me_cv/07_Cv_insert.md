---
title: "Định nghĩa table"
order: 7
dd_id: "createCv"
api_name: "cv.view.createCv"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
status: "Draft — Ready for Review"
---
# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
| ---: | --- |
| Prisma model | Cv |
| Operation | INSERT |
| Transaction | Prisma $transaction |
| Status | Draft — Ready for Review |

## Field mapping

| No | DB column | Operation | Value source | Prisma/schema type |
| ---: | --- | --- | --- | --- |
| 1 | avt | INSERT | normalized body/file value | VARCHAR(191) |
| 2 | hoten | INSERT | normalized body/file value | VARCHAR(191) |
| 3 | ngaysinh | INSERT | normalized body/file value | TIMESTAMPTZ(3) |
| 4 | gioitinh | INSERT | normalized body/file value | VARCHAR(191) |
| 5 | email | INSERT | normalized body/file value | VARCHAR(191) |
| 6 | sdt | INSERT | normalized body/file value | VARCHAR(191) |
| 7 | diachi | INSERT | normalized body/file value | VARCHAR(191) |
| 8 | vitri | INSERT | normalized body/file value | VARCHAR(191) |
| 9 | nganh | INSERT | normalized body/file value | VARCHAR(191) |
| 10 | muctieunghiep | INSERT | normalized body/file value | VARCHAR(191) |
| 11 | hocvan | INSERT | normalized body/file value | VARCHAR(191) |
| 12 | kinhnghiem | INSERT | normalized body/file value | VARCHAR(191) |
| 13 | kynang | INSERT | normalized body/file value | VARCHAR(191) |
| 14 | ngoaingu | INSERT | normalized body/file value | VARCHAR(191) |
| 15 | chungchi | INSERT | normalized body/file value | VARCHAR(191) |
| 16 | duan | INSERT | normalized body/file value | VARCHAR(191) |
| 17 | giaithuong | INSERT | normalized body/file value | VARCHAR(191) |
| 18 | hoatdong | INSERT | normalized body/file value | VARCHAR(191) |
| 19 | social | INSERT | normalized body/file value | JSONB |
| 20 | portfolio | INSERT | normalized body/file value | VARCHAR(191) |
| 21 | luongmongmuon | INSERT | normalized body/file value | VARCHAR(191) |
| 22 | sinhvien_id | INSERT | BigInt(token.id) | BigInt UNIQUE |

## Insert/Update/Delete behavior

- create requires hoten and email.
- Prisma defaults id and created_at.


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
