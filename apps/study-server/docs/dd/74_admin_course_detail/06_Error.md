---
title: "Error"
order: 6
dd_id: "74"
api_name: "Lấy chi tiết course quản trị"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Catalog #74 chỉ cho phép các business code dưới đây. Không thêm 422/409 hoặc code khác. Endpoint chưa wired nên các lỗi là expected contract/proposal, không phải runtime result.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | Bearer/JWT validation | `Authorization` | Header thiếu, token sai/hết hạn hoặc principal không hợp lệ | `401` | `DESIGN_AUTHENTICATION_REQUIRED` | `N/A — Catalog không định nghĩa message ID riêng.` | [05_Data_Mapping.md#step-0-check-quyen](./05_Data_Mapping.md#step-0-check-quyen) | No | DIRECT catalog; auth mechanism chưa có Admin guard. |
| 2 | Authorization | Admin/course permission | Principal | Không phải Admin hoặc không có quyền course management | `403` | `DESIGN_ACCESS_DENIED` | `N/A — Catalog không định nghĩa message ID riêng.` | [05_Data_Mapping.md#step-0-check-quyen](./05_Data_Mapping.md#step-0-check-quyen) | No | DIRECT catalog/AC-32; permission source chưa xác định. |
| 3 | Not found | Parse path / Q1 result | `course_id` | ID không parse được (DERIVED theo #08) hoặc Q1 không tìm thấy course | `404` | `DESIGN_RESOURCE_NOT_FOUND` | `N/A — Catalog không định nghĩa message ID riêng.` | [05_Data_Mapping.md#step-1-validate-data-input](./05_Data_Mapping.md#step-1-validate-data-input) / [#step-2-get-thong-tin](./05_Data_Mapping.md#step-2-get-thong-tin) | No | Không thêm status=PUBLISHED; DRAFT vẫn là Admin-visible. |
| 4 | System/data integrity | Query/mapping | Course/UserSummary | DB error, thiếu required price hoặc mentor projection không đầy đủ | `500` | `DESIGN_INTERNAL_ERROR` | `N/A — Catalog không định nghĩa message ID riêng.` | [05_Data_Mapping.md#step-4-check-ket-qua-query](./05_Data_Mapping.md#step-4-check-ket-qua-query) | Rollback query exception only, per #08 precedent | Safe message; orphan mentor behavior là candidate cần xác nhận. |

> `data:null` theo API guideline là expected error envelope. Current helper trả `{}` khi không truyền data; chưa có API #74 runtime để xác nhận behavior.
---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `4.Error`
- Dimension: `A1:BR13`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `30`
- Số vùng merge: `10`

<details>
<summary>Danh sách vùng merge</summary>

- `C10:F10`
- `G10:I10`
- `J10:N10`
- `O10:X10`
- `Y10:AA10`
- `G11:I11`
- `G12:I12`
- `G13:I13`
- `AB10:AF10`
- `AG10:BA10`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Giải thích |  |
| 4 | `C4` | Các trường hợp lỗi của API |  |
| 10 | `B10` | № |  |
| 10 | `C10` | Category |  |
| 10 | `G10` | Verify check |  |
| 10 | `J10` | Tên item |  |
| 10 | `O10` | Nội dung check |  |
| 10 | `Y10` | Error code |  |
| 10 | `AB10` | Error message ID |  |
| 10 | `AG10` | Remarks |  |
| 11 | `B11` | 1 |  |
| 11 | `C11` | system error |  |
| 11 | `G11` | - |  |
| 11 | `J11` | - |  |
| 11 | `O11` | Trường hợp lỗi truy cập DB |  |
| 11 | `Y11` | 9999 |  |
| 11 | `AB11` | DLG000000 |  |
| 12 | `B12` | 2 |  |
| 12 | `C12` | Check quyền |  |
| 12 | `G12` | - |  |
| 12 | `O12` | Trường hợp không có thông tin quyền tương ứng với user_id trong token |  |
| 12 | `Y12` | 1000 |  |
| 12 | `AB12` | STOCKERR1 |  |
| 12 | `AG12` | Trường hợp số record get được từ xử lý 0. của sheet [3.Data mapping] = 0 |  |
| 13 | `B13` | 3 |  |
| 13 | `C13` | check tồn tại |  |
| 13 | `G13` | 〇 |  |
| 13 | `O13` | Trường hợp không có thông tin parameter trong request data |  |
| 13 | `Y13` | 1001 |  |
| 13 | `AB13` | DLG000093 |  |

</details>
