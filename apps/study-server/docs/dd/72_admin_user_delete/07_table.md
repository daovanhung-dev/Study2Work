---
title: "Định nghĩa table"
order: 7
dd_id: "72"
api_name: "Xóa user theo policy AC-31"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table mapping

| Table/Relation | Loại | Vai trò | Trạng thái |
|---|---|---|---|
| Physical target | Chưa xác định | Soft-delete/anonymize theo policy AC-31 | SOURCE_REQUIRED; không tạo SQL hoặc column giả. |
| Legacy users | Candidate lookup only | Định danh BIGINT trong DDL artifact | Không có deleted_at/anonymized_at; live schema chưa xác minh. |
| Legacy user-linked relations | Dependency context only | Các quan hệ được liệt kê trong 05_Data_Mapping.md | Không phải bảng bị xóa/cascade; policy/constraint chưa xác minh. |
| V1-PILOT identity_projections/learner_profiles | Không dùng làm target | UUID identity/profile lifecycle khác legacy | Không có mapping approved sang user_id:int64. |

## Mapping fields

| Logical field/operation | Physical relation | Column | Operation | Mapping/status |
|---|---|---|---|---|
| Target ID | Physical target chưa xác định | SOURCE_REQUIRED | Lookup/mutation | Không suy ra physical id mapping từ contract int64 một mình. |
| Soft-delete/anonymization state | SOURCE_REQUIRED | SOURCE_REQUIRED | UPDATE candidate chỉ sau khi policy/schema được duyệt | Không dùng DELETE vật lý hoặc cột mới do DD tự tạo. |
| Deletion timestamp | SOURCE_REQUIRED | SOURCE_REQUIRED | Source cho DeleteResult.deleted_at | Legacy users không có deletion timestamp. |
| DeleteResult.status | Response constant | N/A | Response | Literal deleted theo catalog; không phải DB column. |

Không có DDL, migration hoặc index nào được tạo bởi DD này. DDL legacy/pilot chỉ được dẫn làm evidence của gap và dependency, không phải schema đã deploy.

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
