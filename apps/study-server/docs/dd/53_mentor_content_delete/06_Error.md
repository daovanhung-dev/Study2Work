---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
dd_id: "53"
api_name: "Xóa nội dung Mentor"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Giữ đúng HTTP status/business code theo catalog API #53. Dependency, published-state và already-deleted branches là DERIVED, chưa phải runtime behavior.

## Error cases

| ID | HTTP status | Business code | Điều kiện | Hành động | Basis |
|---|---:|---|---|---|---|
| E1 | 401 | DESIGN_AUTHENTICATION_REQUIRED | Thiếu hoặc Bearer JWT không hợp lệ | Không mutate Content; trả lỗi | Code DIRECT; auth condition theo convention |
| E2 | 403 | DESIGN_ACCESS_DENIED | Sai role Mentor hoặc không có quyền quản lý course | Không mutate Content | Code/role DIRECT; permission mapping SOURCE_REQUIRED |
| E3 | 404 | DESIGN_RESOURCE_NOT_FOUND | Không có Content khả dụng theo content_id | Không mutate; already-soft-deleted → 404 là DERIVED | Code DIRECT; repeat-delete semantics open |
| E4 | 422 | DESIGN_VALIDATION_ERROR | Path không parse được int64, PUBLISHED theo proposal, hoặc còn direct child dependency | Không mutate; PUBLISHED phải qua #52; child không cascade | Code DIRECT; branches DERIVED |
| E5 | 500 | DESIGN_INTERNAL_ERROR | Lookup hoặc soft-delete operation lỗi ngoài contract | Rollback logical operation nếu có transaction; không lộ chi tiết nội bộ | Code DIRECT; transaction SOURCE_REQUIRED |

Không thêm mã 409, 423 hoặc Content status mới.

## Tích hợp error contract

- Current DESIGN_CONTRACT_PATHS chưa có Mentor Content path vì route chưa được implement.
- Nếu wire route mà thiếu integration mapping, middleware có thể trả fallback thay vì DESIGN_VALIDATION_ERROR/DESIGN_INTERNAL_ERROR.
- Current error_response dùng data={} khi caller không truyền data; API #53 chưa được runtime xác minh.
- Tham chiếu flow: [05_Data_Mapping.md](./05_Data_Mapping.md).

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
