---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
---

# Error

## Giải thích

Các trường hợp lỗi API #13 theo contract đã cập nhật. API chỉ trả `401`, `403`, `422` hoặc `500`; không thêm `404`/`503`. Lỗi provider và cấu hình được trả bằng message an toàn, không lộ chi tiết nội bộ.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication error | `Yes` | `Authorization` | Thiếu header. | `401` | `DESIGN_AUTHENTICATION_REQUIRED` | `N/A — envelope message` | [`0.3`](./05_Data_Mapping.md) | `No` | Không trả token hoặc chi tiết verifier. |
| 2 | Authentication error | `Yes` | `Authorization` | Header không có scheme Bearer. | `401` | `DESIGN_AUTHENTICATION_REQUIRED` | `N/A — envelope message` | [`0.3`](./05_Data_Mapping.md) | `No` | Không trả token hoặc chi tiết verifier. |
| 3 | Authentication error | `Yes` | `JWT signature` | Chữ ký JWT không hợp lệ. | `401` | `DESIGN_AUTHENTICATION_REQUIRED` | `N/A — envelope message` | [`0.3`](./05_Data_Mapping.md) | `No` | Không trả token hoặc chi tiết verifier. |
| 4 | Authentication error | `Yes` | `JWT expiry` | Token JWT hết hạn. | `401` | `DESIGN_AUTHENTICATION_REQUIRED` | `N/A — envelope message` | [`0.3`](./05_Data_Mapping.md) | `No` | Không trả token hoặc chi tiết verifier. |
| 5 | Authentication error | `Yes` | `JWT claims` | JWT thiếu hoặc sai `sub`/`roles`. | `401` | `DESIGN_AUTHENTICATION_REQUIRED` | `Authentication required.` | [`0.3`](./05_Data_Mapping.md) | `No` | Không trả token hoặc chi tiết verifier. |
| 6 | Authorization error | `Yes` | `role` | JWT hợp lệ nhưng role không phải `Student`. | `403` | `DESIGN_ACCESS_DENIED` | `N/A — envelope message` | [`0.3`](./05_Data_Mapping.md) | `No` | Không tạo role/business code mới. |
| 7 | Required validation | `Yes` | `image` | Body thiếu field `image`. | `422` | `DESIGN_VALIDATION_ERROR` | `Dữ liệu đầu vào không hợp lệ.` | [`2.1`](./05_Data_Mapping.md) | `No` | Request schema yêu cầu field. |
| 8 | Required validation | `Yes` | `image` | `image` bằng null. | `422` | `DESIGN_VALIDATION_ERROR` | `Dữ liệu đầu vào không hợp lệ.` | [`2.1`](./05_Data_Mapping.md) | `No` | Request model từ chối null. |
| 9 | Type validation | `Yes` | `image` | `image` không phải string. | `422` | `DESIGN_VALIDATION_ERROR` | `Dữ liệu đầu vào không hợp lệ.` | [`2.1`](./05_Data_Mapping.md) | `No` | Strict string model. |
| 10 | Required validation | `Yes` | `image` | `image` rỗng. | `422` | `DESIGN_VALIDATION_ERROR` | `Avatar input is invalid.` | [`2.1`](./05_Data_Mapping.md) | `No` | Field error `EMPTY_IMAGE`. |
| 11 | Format validation | `Yes` | `image` | Data URL header hoặc Base64 sai format. | `422` | `DESIGN_VALIDATION_ERROR` | `Avatar input is invalid.` | [`2.2`](./05_Data_Mapping.md) | `No` | Field error `INVALID_DATA_URL` hoặc `INVALID_BASE64`. |
| 12 | Format validation | `Yes` | `image MIME` | MIME không thuộc `image/png`, `image/jpeg`, `image/webp`. | `422` | `DESIGN_VALIDATION_ERROR` | `Avatar input is invalid.` | [`2.3`](./05_Data_Mapping.md) | `No` | Unsupported MIME không được upload. |
| 13 | Format validation | `Yes` | `image size` | Payload giải mã lớn hơn 5 MiB. | `422` | `DESIGN_VALIDATION_ERROR` | `Avatar input is invalid.` | [`2.3`](./05_Data_Mapping.md) | `No` | Field error `IMAGE_TOO_LARGE`. |
| 14 | Format validation | `Yes` | `image signature` | Chữ ký ảnh không khớp MIME khai báo. | `422` | `DESIGN_VALIDATION_ERROR` | `Avatar input is invalid.` | [`2.4`](./05_Data_Mapping.md) | `No` | Field error `IMAGE_SIGNATURE_MISMATCH`. |
| 15 | Format validation | `Yes` | `request body` | Body có field ngoài contract. | `422` | `DESIGN_VALIDATION_ERROR` | `Dữ liệu đầu vào không hợp lệ.` | [`1.2`](./05_Data_Mapping.md) | `No` | `extra=forbid`. |
| 16 | Dependency/system error | `No` | `Object Storage configuration` | Thiếu cấu hình bắt buộc. | `500` | `DESIGN_INTERNAL_ERROR` | `Avatar could not be uploaded.` | [`3.2`](./05_Data_Mapping.md) | `No` | Không chặn app startup; response không lộ tên/value config. |
| 17 | Dependency/system error | `No` | `Object Storage configuration` | Public base URL sai format. | `500` | `DESIGN_INTERNAL_ERROR` | `Avatar could not be uploaded.` | [`3.2`](./05_Data_Mapping.md) | `No` | Không đưa giá trị config vào response. |
| 18 | Dependency/system error | `No` | `Object Storage` | Upload provider thất bại. | `500` | `DESIGN_INTERNAL_ERROR` | `Avatar could not be uploaded.` | [`3.2`](./05_Data_Mapping.md) | `No` | Không lộ provider detail hoặc stack trace. |
| 19 | Dependency/system error | `No` | `Object Storage` | Upload vượt timeout. | `500` | `DESIGN_INTERNAL_ERROR` | `Avatar could not be uploaded.` | [`3.2`](./05_Data_Mapping.md) | `No` | Connect 5s, read 30s, một attempt. |

> Không tạo error row `404` vì API không có path parameter. Không tạo `503` vì API #13 contract hiện chỉ khai báo `500` cho failure ngoài validation/auth.
>
> Mỗi điều kiện lỗi nằm trên một row riêng. API contract không khai báo `404` hoặc `503`.

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/06_Error.md`.
- Sheet logic: `4.Error`.
