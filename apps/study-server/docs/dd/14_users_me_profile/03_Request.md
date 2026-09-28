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
| HTTP method | `PUT` |
| URI | `/api/v1/users/me/profile` |
| Character encoding | `UTF-8` |
| Content-Type | `application/json` — derived from current Study JSON API convention; contract không ghi rõ media type. |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | `Authorization` | `Yes` | `Bearer <jwt>` | Bearer JWT dùng để xác thực identity và kiểm tra role Student. | `05_Data_Mapping.md`, step `0.1/0.2/0.3` |
| 2 | Content type | `Content-Type` | `Yes` | `application/json` | Body truyền dưới dạng JSON theo current Study API convention. | `05_Data_Mapping.md`, step `1.1` |
| 3 | Trace ID | `X-Trace-Id` | `No` | UUID string hoặc để middleware tạo | Correlation ID được current Study middleware chuẩn hóa/gắn vào response. | `05_Data_Mapping.md`, step `0.1` |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Endpoint không có path parameter; user identity lấy từ JWT. | `N/A` |

## Query parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Endpoint không có query parameter. | `N/A` |

## Request body

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| 1 | Full name | `full_name` | `string` | `Yes` | `1` | `150` | `UTF-8 string` | `TBD — blank/normalization policy chưa có source` | `TBD — không có enum` | `N/A` | Tên hiển thị của Student; max 150 theo current `users.full_name`. | `05_Data_Mapping.md`, step `1.2/2.1` |
| 2 | Biography | `bio` | `string` | `Yes` | `TBD` | `TBD` | `UTF-8 string` | `TBD — policy blank/length chưa có source` | `TBD — không có enum` | `N/A` | Contract yêu cầu biography; persistence column chưa source-backed. | `05_Data_Mapping.md`, step `1.3/2.2/4.1` |
| 3 | Phone | `phone` | `string` | `Yes` | `TBD` | `20` | `UTF-8 string` | `TBD — phone format chưa có source` | `TBD — không có enum` | `N/A` | Số điện thoại; max 20 theo current `users.phone`, nhưng DB cho phép nullable. | `05_Data_Mapping.md`, step `1.4/2.3/4.1` |
| 4 | Avatar URL | `avatar_url` | `string` | `TBD — contract literal là avatar_url...:uri!` | `TBD` | `TBD` | `UTF-8 string` | `uri` theo contract; requiredness/nullable semantics chưa khóa | `TBD — URI scheme/blank policy chưa có source` | `N/A` | URL avatar sau flow API #13; không tự tạo storage URL hoặc object key. | `05_Data_Mapping.md`, step `1.5/2.4/4.1` |

> `bio` không được map vào SQL column khi chưa có source xác nhận. `avatar_url` giữ physical name chuẩn trong body; dấu `...` chỉ được giữ trong ghi chú contract vì không phải physical field name hợp lệ.

## Ví dụ Request data

```json
{
  "full_name": "Nguyen Van A",
  "bio": "Student profile biography",
  "phone": "+84901234567",
  "avatar_url": "https://storage.example.test/avatars/student-1001.png"
}
```

> Ví dụ chỉ minh họa JSON hợp lệ và format URI; không xác nhận `bio` persistence hoặc avatar requiredness.

## Form data

- `N/A — request body là JSON theo contract body fields; không chuyển sang multipart.`

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/03_Request.md`.
- Sheet logic: `1.Request`.

