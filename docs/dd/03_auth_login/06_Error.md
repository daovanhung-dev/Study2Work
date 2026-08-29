---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
---

# Error

## Giải thích

Normative error cases của API theo `list_api.md`. Các nhánh `401/403` chỉ có trong AC-02 và được ghi riêng ở mục discrepancy.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Validation error | `Yes` | `email` | Field `email` thiếu hoặc blank | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — envelope message` | [`2.1`](./05_Data_Mapping.md#21-validate-email) | `No` | Required validation |
| 2 | Validation error | `Yes` | `email` | Field `email` không đúng type/format `email` | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — envelope message` | [`2.1`](./05_Data_Mapping.md#21-validate-email) | `No` | Không tự đặt min/max/canonicalization |
| 3 | Validation error | `Yes` | `password` | Field `password` thiếu hoặc blank | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — envelope message` | [`2.2`](./05_Data_Mapping.md#22-validate-password) | `No` | Required validation |
| 4 | Validation error | `Yes` | `password` | Field `password` không phải `string` | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — envelope message` | [`2.2`](./05_Data_Mapping.md#22-validate-password) | `No` | Không tự đặt password policy |
| 5 | System error | `No` | Query/hash/session | Lỗi nội bộ khi query, verify hash hoặc hoàn tất flow login | `500` | `DESIGN_INTERNAL_ERROR` | `N/A — envelope message` | [`5.1/6.3`](./05_Data_Mapping.md#51-issue-token-or-session) | `No` | Không trả raw DB/hash/session detail |

> Mỗi error case và mỗi field validation phải nằm trên một row riêng.
>
> Error response dùng `ApiEnvelope`; không tạo `error_code` hoặc `error_message_id` riêng.

## Source discrepancies — non-normative

| No | Source branch | AC-02 status/code | list_api.md contract | Resolution |
|---:|---|---|---|---|
| D1 | Account không tồn tại hoặc sai mật khẩu | `401 DESIGN_AUTHENTICATION_REQUIRED` | Không khai báo cho API #3 | `DISCREPANCY/TBD`; không thêm normative error row |
| D2 | Account bị khóa | `403 DESIGN_ACCESS_DENIED` | Không khai báo cho API #3 | `DISCREPANCY/TBD`; không thêm normative error row |
| D3 | Login thành công | `200 DESIGN_RESOURCE_RETRIEVED` | `201 DESIGN_RESOURCE_CREATED` | Dùng list_api.md làm normative; AC status giữ discrepancy |

> AC-02 cũng nói client nhận token; UserProfile response contract không khai báo token. DD không tự thêm `access_token`.


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

