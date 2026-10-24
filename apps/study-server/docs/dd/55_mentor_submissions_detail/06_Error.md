---
title: "Error"
order: 6
dd_id: "55"
api_name: "Lấy bài làm và rubric Mentor"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các error code dưới đây giữ nguyên API catalog #55. Nhánh authorization/query là flow đề xuất; API #55 chưa có route để xác minh behavior. Xem [05_Data_Mapping.md](./05_Data_Mapping.md) để đối chiếu thứ tự xử lý.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Token verification | Authorization | Header thiếu/sai Bearer, JWT invalid/expired hoặc claims không hợp lệ | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | N/A — catalog không khai message ID | [05_Data_Mapping.md](./05_Data_Mapping.md) | N/A — no mutation | Catalog DIRECT; auth source pattern current Study |
| 2 | Authorization | Role/course permission | Mentor access | JWT hợp lệ nhưng không có role Mentor hoặc candidate course owner không khớp | 403 | `DESIGN_ACCESS_DENIED` | N/A — catalog không khai message ID | [05_Data_Mapping.md](./05_Data_Mapping.md) | N/A — no mutation | Direct-owner predicate và 403/masking là DERIVED, cần xác nhận |
| 3 | Check tồn tại | Submission lookup | `submission_id` | Không tìm thấy submission với ID hợp lệ | 404 | `DESIGN_RESOURCE_NOT_FOUND` | N/A — catalog không khai message ID | [05_Data_Mapping.md](./05_Data_Mapping.md) | N/A — no mutation | Catalog DIRECT; malformed path behavior chưa định nghĩa |
| 4 | System error | Query/mapping/integrity | Database/result | DB/query lỗi hoặc required relation/field candidate bị hỏng | 500 | `DESIGN_INTERNAL_ERROR` | N/A — catalog không khai message ID | [05_Data_Mapping.md](./05_Data_Mapping.md) | N/A — no mutation | DB error DIRECT; orphan/null integrity branch là DERIVED |

## Error envelope discrepancy

- API Guidelines kỳ vọng `data:null` và field errors trong `meta.fieldErrors`.
- Current `error_response()` trả `{}` khi caller truyền `data=None`.
- `DESIGN_CONTRACT_PATHS` chưa có API #55; nếu middleware xử lý validation/unhandled error trước khi path allowlist được cập nhật, code fallback có thể khác catalog.
- Đây là current shared-source discrepancy, không phải kết quả runtime đã đo cho API #55.

## Không khai báo

- Không thêm `400`, `409`, `422` hoặc business code ngoài catalog.
- Rubric/file resolver chưa có source nên DD không tự tạo HTTP branch riêng cho chúng.

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
