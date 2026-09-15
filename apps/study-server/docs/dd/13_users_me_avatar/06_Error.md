---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
---

# Error

## Giải thích

Các trường hợp lỗi của API #13 theo API contract V1. Contract chỉ khai báo `401`, `403`, `422` và `500`; không tự thêm `404` hoặc `503`. MIME/size và storage failure được giữ ở mức gap khi policy/adapter chưa được source xác nhận.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication error | `Yes` | `Authorization` | Thiếu header. | `401` | `DESIGN_AUTHENTICATION_REQUIRED` | `N/A — envelope message` | [`0.3`](./05_Data_Mapping.md) | `No` | Không trả token hoặc chi tiết verifier. |
| 2 | Authentication error | `Yes` | `Authorization` | Header không có scheme Bearer. | `401` | `DESIGN_AUTHENTICATION_REQUIRED` | `N/A — envelope message` | [`0.3`](./05_Data_Mapping.md) | `No` | Không trả token hoặc chi tiết verifier. |
| 3 | Authentication error | `Yes` | `JWT signature` | Chữ ký JWT không hợp lệ. | `401` | `DESIGN_AUTHENTICATION_REQUIRED` | `N/A — envelope message` | [`0.3`](./05_Data_Mapping.md) | `No` | Không trả token hoặc chi tiết verifier. |
| 4 | Authentication error | `Yes` | `JWT expiry` | Token JWT hết hạn. | `401` | `DESIGN_AUTHENTICATION_REQUIRED` | `N/A — envelope message` | [`0.3`](./05_Data_Mapping.md) | `No` | Không trả token hoặc chi tiết verifier. |
| 5 | Authentication error | `Yes` | `JWT claim` | JWT thiếu claim bắt buộc. | `401` | `DESIGN_AUTHENTICATION_REQUIRED` | `N/A — envelope message` | [`0.3`](./05_Data_Mapping.md) | `No` | Tên claim cụ thể là `SOURCE_REQUIRED`. |
| 6 | Authorization error | `Yes` | `role` | JWT hợp lệ nhưng role không phải `Student`. | `403` | `DESIGN_ACCESS_DENIED` | `N/A — envelope message` | [`0.3`](./05_Data_Mapping.md) | `No` | Không tạo role/business code mới. |
| 7 | Required validation | `Yes` | `image` | Body thiếu `image`. | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — envelope message` | [`2.1`](./05_Data_Mapping.md) | `No` | Giữ đúng body field `image:string!`. |
| 8 | Required validation | `Yes` | `image` | `image = NULL`. | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — envelope message` | [`2.1`](./05_Data_Mapping.md) | `No` | Giữ đúng body field `image:string!`. |
| 9 | Required validation | `Yes` | `image` | `image` là blank khi policy phê duyệt việc từ chối blank. | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — envelope message` | [`2.1`](./05_Data_Mapping.md) | `No` | Blank policy là `TBD`. |
| 10 | Format validation | `Yes` | `image encoding` | Encoding không đạt policy đã phê duyệt. | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — envelope message` | [`2.2`](./05_Data_Mapping.md) | `No` | Không tự chọn encoding. |
| 11 | Format validation | `Yes` | `image MIME` | MIME không đạt policy đã phê duyệt. | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — envelope message` | [`2.3`](./05_Data_Mapping.md) | `No` | Không tự đặt allowlist MIME. |
| 12 | Format validation | `Yes` | `image size` | Size vượt giới hạn đã phê duyệt. | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — envelope message` | [`2.3`](./05_Data_Mapping.md) | `No` | Không tự đặt giới hạn kích thước. |
| 13 | Dependency/system error | `No` | `Object Storage` | Upload thất bại. | `500` | `DESIGN_INTERNAL_ERROR` | `N/A — envelope message` | [`3.2`](./05_Data_Mapping.md) | `TBD` | Contract hiện không có `503`; cleanup/idempotency chưa được đặc tả. |
| 14 | Dependency/system error | `No` | `Object Storage` | Upload timeout. | `500` | `DESIGN_INTERNAL_ERROR` | `N/A — envelope message` | [`3.2`](./05_Data_Mapping.md) | `TBD` | Contract hiện không có `503`; cleanup/idempotency chưa được đặc tả. |
| 15 | Dependency/system error | `No` | `Object Storage response` | Provider response không hợp lệ. | `500` | `DESIGN_INTERNAL_ERROR` | `N/A — envelope message` | [`3.2`](./05_Data_Mapping.md) | `TBD` | Contract hiện không có `503`; cleanup/idempotency chưa được đặc tả. |
| 16 | Dependency/system error | `No` | `Response mapping` | Lỗi mapping response. | `500` | `DESIGN_INTERNAL_ERROR` | `N/A — envelope message` | [`3.2`](./05_Data_Mapping.md) | `TBD` | Contract hiện không có `503`; cleanup/idempotency chưa được đặc tả. |

> Không tạo error row `404` vì API không có path parameter. Không tạo `503` vì API #13 contract hiện chỉ khai báo `500` cho failure ngoài validation/auth.
>
> Mỗi error case nằm trên một row riêng; các policy chưa có nguồn được đánh dấu `TBD`/`SOURCE_REQUIRED`.

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/06_Error.md`.
- Sheet logic: `4.Error`.
