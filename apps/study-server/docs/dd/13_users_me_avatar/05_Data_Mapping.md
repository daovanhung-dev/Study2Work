---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

## Request Usage Matrix

| Request field | Source | Data Mapping step | Validate | Storage/mutation usage | Branch/Loop | Response usage | Gap |
|---|---|---|---|---|---|---|---|
| `Authorization` | `header["Authorization"]` | `0.1/0.2` | Bearer JWT validation | Scope/authorization only | `0.3` | Không map trực tiếp | Exact claim names and JWT policy chưa có source. |
| `Content-Type` | `header["Content-Type"]` | `1.1` | Transport validation | Chọn parser theo contract sau khi media type được khóa | `2.2/2.3` | Không map trực tiếp | Media type chưa được đặc tả. |
| `image` | `request["image"]` | `1.2` | Required, encoding, MIME và size theo policy TBD | `M1` gửi vào Object Storage | `2.1/2.2/2.3/3.1` | Có thể là source cho `data.avatar_url` nếu storage result mapping được xác nhận | Không diễn giải string hoặc tự tạo format. |

## Query Matrix

| Query ID | Mục đích | Type | Base table/view | Alias | Columns | JOIN | WHERE | GROUP/HAVING | ORDER | Pagination | Result variable | Branch |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `N/A` | Không có DB query được source xác nhận | `N/A — upload-only` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Không reload user profile. |

## Mutation Matrix

| Mutation ID | Operation | Target table/API | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|---|
| `M1` | `External upload` | `Object Storage` | `storage object key = SOURCE_REQUIRED` | `image payload` | `request["image"]` từ step `1.2` | `TBD — audit contract chưa có` | `07_table.md` ghi N/A vì không phải DB table | `N/A — external operation; transaction/cleanup TBD` | Lỗi upload hoặc storage response không hợp lệ đi tới `500 DESIGN_INTERNAL_ERROR`. |

## Response Source Matrix

| Response field | Type | Source type | Table/column hoặc generator | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| `success` | `boolean` | Branch constant | Processing result | `5.1/5.2/5.3/5.4` | `true` on success; `false` on error | `N/A` | `N/A` |
| `businessCode` | `string` | Branch constant | Design contract | `5.1/5.2/5.3/5.4` | Fixed `DESIGN_*` code | `N/A` | `N/A` |
| `message` | `string` | Branch message | Application | `5.1/5.2/5.3/5.4` | Fixed by branch | Text TBD | Message catalog chưa có. |
| `data.id` | `int64` | Unresolved profile source | `N/A` | `5.1` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | Upload-only flow không reload profile. |
| `data.full_name` | `string` | Unresolved profile source | `N/A` | `5.1` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | Không tự query `users`. |
| `data.email` | `email` | Unresolved profile source | `N/A` | `5.1` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | Không tự query `users`. |
| `data.role` | `string` | Token authorization context | `validated JWT role claim` | `0.2/5.1` | `SOURCE_REQUIRED` for profile response | `SOURCE_REQUIRED` | Role claim dùng auth nhưng chưa đủ làm UserProfile source. |
| `data.avatar_url` | `uri` | External result | `Object Storage result field TBD` | `3.2/5.1` | `SOURCE_REQUIRED` | `TBD` | Storage output URL contract chưa có. |
| `data.bio` | `string` | Unresolved profile source | `N/A` | `5.1` | `SOURCE_REQUIRED` | `Omit when no source` | Optional contract field, không có source trong flow. |
| `data.phone` | `string` | Unresolved profile source | `N/A` | `5.1` | `SOURCE_REQUIRED` | `Omit when no source` | Optional contract field, không có source trong flow. |
| `data.status` | `string` | Unresolved profile source | `N/A` | `5.1` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | Không tự gán `ACTIVE`. |
| `data.created_at` | `date-time` | Unresolved profile source | `N/A` | `5.1` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | Không tự tạo timestamp. |
| `data.updated_at` | `date-time` | Unresolved profile source | `N/A` | `5.1` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | API #13 không update DB. |
| `meta` | `object` | Envelope default | `N/A` | `5.1/5.2/5.3/5.4` | `{}` | `{}` | Không thêm storage metadata. |
| `traceId` | `uuid` | Correlation generator | `N/A` | `5.1/5.2/5.3/5.4` | Request correlation UUID | `TBD` | Generator chưa được source đặc tả. |

## 0. Check quyền

### 0.1. Get request header

- `authorization`: lấy từ `header["Authorization"]`.
- `content_type`: lấy từ `header["Content-Type"]` nếu transport gửi header này.
- Không nhận `user_id`, `storage_key` hoặc `avatar_url` từ header.

### 0.2. Decode token

- Verify Bearer JWT theo auth policy được phê duyệt.
- Kiểm tra chữ ký, expiry và claim cần cho authorization.
- `role`: lấy từ claim role theo policy được phê duyệt; tên claim cụ thể là `SOURCE_REQUIRED`.
- Identity subject dùng để scope upload nếu storage policy yêu cầu; claim name và mapping là `SOURCE_REQUIRED`.

### 0.3. Check role

- Nếu thiếu `Authorization`: đi tới [06_Error.md](./06_Error.md), error case `1`, HTTP `401`.
- Nếu Authorization không có scheme Bearer: đi tới [06_Error.md](./06_Error.md), error case `2`, HTTP `401`.
- Nếu chữ ký JWT không hợp lệ: đi tới [06_Error.md](./06_Error.md), error case `3`, HTTP `401`.
- Nếu token JWT hết hạn: đi tới [06_Error.md](./06_Error.md), error case `4`, HTTP `401`.
- Nếu JWT thiếu claim bắt buộc: đi tới [06_Error.md](./06_Error.md), error case `5`, HTTP `401`.
- Nếu JWT hợp lệ nhưng role khác `Student`: đi tới [06_Error.md](./06_Error.md), error case `6`, HTTP `403`.
- Nếu JWT hợp lệ và role là `Student`: tiếp tục xử lý `1`.

## 1. Get request data

### 1.1. Get transport metadata

- `content_type`: đọc từ request header nếu có.
- Không chọn `application/json`, `multipart/form-data` hoặc media type khác khi contract chưa đặc tả.
- Nếu transport không thể parse body theo contract đã được phê duyệt: đi tới error case validation trong [06_Error.md](./06_Error.md).

### 1.2. Get request body

- `image`: lấy từ `request["image"]`.
- Không nhận `file`.
- Không nhận `mime_type`.
- Không nhận `size`.
- Không nhận `storage_key`.
- Không nhận `avatar_url`.

## 2. Validate data input

### 2.1. Check required image

- Nếu `image` thiếu: đi tới [06_Error.md](./06_Error.md), error case `7`, HTTP `422`.
- Nếu `image` là `NULL`: đi tới [06_Error.md](./06_Error.md), error case `8`, HTTP `422`.
- Nếu `image` là blank: xử lý theo required/blank policy sau khi policy được phê duyệt; nếu policy từ chối blank thì đi tới [06_Error.md](./06_Error.md), error case `9`, HTTP `422`.

### 2.2. Check image encoding

- Xác định image string có đúng encoding được contract phê duyệt hay không.
- Encoding/data URI/base64/URL chưa được source xác nhận; không chọn một loại làm runtime rule.
- Nếu encoding không hợp lệ sau khi policy được khóa: đi tới [06_Error.md](./06_Error.md), error case `10`, HTTP `422`.

### 2.3. Check MIME and size

- Diagram AC-11 yêu cầu validate MIME/size trước khi lưu.
- MIME allowlist chưa được source xác nhận.
- Size limit chưa được source xác nhận.
- Nếu MIME không đạt policy đã phê duyệt: đi tới [06_Error.md](./06_Error.md), error case `11`, HTTP `422`.
- Nếu size vượt giới hạn đã phê duyệt: đi tới [06_Error.md](./06_Error.md), error case `12`, HTTP `422`.

## 3. Upload avatar

### 3.1. Send avatar to Object Storage

- Gọi Object Storage adapter/service theo interface được phê duyệt.
- `image_payload`: lấy từ `image` ở step `1.2`.
- `storage_object_key`: `SOURCE_REQUIRED`; không tự tạo naming hoặc namespace rule.
- Không thực hiện `INSERT`, `UPDATE`, `DELETE` hoặc `SELECT` trên database.
- Không cập nhật `users.avatar_url` trong API #13.

### 3.2. Check storage result

- Nếu Object Storage trả kết quả upload thành công nhưng không có output mapping được contract xác nhận: giữ response field `data.avatar_url` ở trạng thái `SOURCE_REQUIRED`.
- Nếu Object Storage upload thất bại: đi tới [06_Error.md](./06_Error.md), error case `13`, HTTP `500` theo status contract hiện có.
- Nếu Object Storage timeout: đi tới [06_Error.md](./06_Error.md), error case `14`, HTTP `500` theo status contract hiện có.
- Nếu Object Storage response không hợp lệ: đi tới [06_Error.md](./06_Error.md), error case `15`, HTTP `500` theo status contract hiện có.
- Nếu response mapping thất bại: đi tới [06_Error.md](./06_Error.md), error case `16`, HTTP `500` theo status contract hiện có.
- Retry, idempotency và cleanup object đã upload khi downstream response thất bại là `SOURCE_REQUIRED`.

## 4. Response mapping

### 4.1. Preserve UserProfile contract

- Giữ response type `ApiEnvelope<UserProfile>` theo `list_api.md`.
- Không tự gọi API #4 để reload profile.
- Không tự gọi API #14 để cập nhật profile.
- `data.avatar_url`: chỉ có thể map từ Object Storage result sau khi output field được source xác nhận; hiện ghi `SOURCE_REQUIRED`.
- `data.id`, `data.full_name`, `data.email`, `data.role`, `data.status`, `data.created_at` và `data.updated_at`: ghi `SOURCE_REQUIRED` vì upload-only flow không có profile source.
- `data.bio` và `data.phone`: omit khi không có source, không tạo cột hoặc query mới.

## 5. Trả về response

### 5.1. Success response

- `HTTPStatus = 201`.
- `success = true`.
- `businessCode = DESIGN_RESOURCE_CREATED`.
- `data = UserProfile` theo [04_Response.md](./04_Response.md); các mapping chưa có source vẫn là gap design.
- `meta = {}`.
- `traceId = request correlation UUID`; generator là `TBD`.

### 5.2. Authentication error

- `HTTPStatus = 401`.
- `success = false`.
- `businessCode = DESIGN_AUTHENTICATION_REQUIRED`.
- `data = {}`.
- Chi tiết: [06_Error.md](./06_Error.md).

### 5.3. Authorization error

- `HTTPStatus = 403`.
- `success = false`.
- `businessCode = DESIGN_ACCESS_DENIED`.
- `data = {}`.
- Chi tiết: [06_Error.md](./06_Error.md).

### 5.4. Validation error

- `HTTPStatus = 422`.
- `success = false`.
- `businessCode = DESIGN_VALIDATION_ERROR`.
- `data = {}`.
- Chi tiết: [06_Error.md](./06_Error.md).

### 5.5. System/storage error

- `HTTPStatus = 500`.
- `success = false`.
- `businessCode = DESIGN_INTERNAL_ERROR`.
- `data = {}`.
- Không trả storage credential, object key, raw provider body, SQL hoặc stack trace.
- Chi tiết: [06_Error.md](./06_Error.md).

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/05_Data_Mapping.md`.
- Sheet logic: `3. Data mapping`.
