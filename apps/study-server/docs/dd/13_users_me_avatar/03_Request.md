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
| Character encoding | `UTF-8` |
| Content-Type | `application/json` |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | `Authorization` | `Yes` | `Bearer <jwt>` | Bearer JWT dùng để xác thực và kiểm tra role Student. | `05_Data_Mapping.md`, step `0.1/0.3` |
| 2 | Content type | `Content-Type` | `Yes` | `application/json` | Body JSON chứa Data URL; không nhận multipart. | `05_Data_Mapping.md`, step `1.1` |

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
| 1 | Image | `image` | `string` | `Yes` | `1` | `N/A` | `Unicode` | `data:image/<mime>;base64,...` | `image/png`, `image/jpeg`, `image/webp`; decoded bytes `<= 5 MiB`; chữ ký phải khớp MIME | `N/A` | JSON string Data URL; không nhận URL hoặc multipart. | `05_Data_Mapping.md`, step `1.2/2.1-2.4` |

> `image` được giữ đúng kiểu `string` theo `list_api.md`. Không thêm field `file`, `mime_type`, `size`, `storage_key` hoặc `avatar_url` vào Request.

## Ví dụ Request

```json
{
  "image": "data:image/png;base64,iVBORw0KGgo="
}
```

> Ví dụ minh họa cú pháp Data URL và PNG signature; ảnh gửi thật phải có payload hợp lệ và không vượt 5 MiB sau giải mã.

## Form data

- N/A — API chỉ nhận JSON; không nhận `multipart/form-data`.

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/03_Request.md`.
- Sheet logic: `1.Request`.
