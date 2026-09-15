---
title: "Request"
order: 3
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "1.Request"
format: markdown
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | `POST` |
| URI | `/api/v1/users/me/avatar` |
| Character encoding | `TBD — contract chưa đặc tả encoding của image string` |
| Content-Type | `TBD — contract chưa đặc tả media type; không tự chuyển sang multipart` |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | `Authorization` | `Yes` | `Bearer <jwt>` | Bearer JWT dùng để xác thực và kiểm tra role Student. | `05_Data_Mapping.md`, step `0.1/0.3` |
| 2 | Content type | `Content-Type` | `TBD` | `TBD — media type chưa được contract xác nhận` | Transport metadata cần được khóa trước implementation. | `05_Data_Mapping.md`, step `1.1` |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Endpoint không có path parameter. | `N/A` |

## Query parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Endpoint không có query parameter. | `N/A` |

## Request body

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| 1 | Image | `image` | `string` | `Yes` | `TBD` | `TBD` | `TBD` | `TBD — encoding chưa được source xác nhận` | `TBD — MIME/size/format policy chưa được source xác nhận` | `N/A` | Chuỗi đại diện avatar do Student gửi theo API contract. | `05_Data_Mapping.md`, step `1.2/2.1` |

> `image` được giữ đúng kiểu `string` theo `list_api.md`. Không thêm field `file`, `mime_type`, `size`, `storage_key` hoặc `avatar_url` vào Request.

## Ví dụ Request

```json
{
  "image": "<TBD — image string encoding chưa được source xác nhận>"
}
```

> Placeholder trong ví dụ là chuỗi JSON hợp lệ và chỉ thể hiện gap design; không phải giá trị runtime hoặc format được phê duyệt.

## Form data

- N/A — plan khóa contract body là `image:string`; không đặc tả `multipart/form-data`.

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/03_Request.md`.
- Sheet logic: `1.Request`.
