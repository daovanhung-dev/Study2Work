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
| `Authorization` | `header["Authorization"]` | `0.1/0.2` | Shared Bearer/JWT guard; require `STUDENT` | Scope/authorization only | `0.3` | Không map trực tiếp | Dùng claim `sub`/`roles` hiện hành. |
| `Content-Type` | `header["Content-Type"]` | `1.1` | JSON request body | Chọn parser JSON | `1.2` | Không map trực tiếp | Multipart không được nhận. |
| `image` | `request["image"]` | `1.2` | Data URL, strict Base64, PNG/JPEG/WebP signature, decoded size `<= 5 MiB` | `M1` gửi bytes và MIME vào Object Storage | `2.1-2.4/3.1` | `data.avatar_url` được ghép từ public base URL và object key | Field ngoài schema bị từ chối. |

## Query Matrix

| Query ID | Mục đích | Type | Base table/view | Alias | Columns | JOIN | WHERE | GROUP/HAVING | ORDER | Pagination | Result variable | Branch |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `N/A` | Không có DB query được source xác nhận | `N/A — upload-only` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Không reload user profile. |

## Mutation Matrix

| Mutation ID | Operation | Target table/API | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|---|
| `M1` | `PUT object` | `S3-compatible Object Storage` | `avatars/{user_id}` từ `sub` đã xác thực | `Body`, `ContentType` | Data URL đã giải mã và MIME đã kiểm tra | `N/A — audit chưa được yêu cầu` | `07_table.md` ghi N/A vì không phải DB table | `N/A — external operation; cùng key được ghi đè, không retry/cleanup riêng` | Thiếu config, provider error hoặc timeout đi tới `500 DESIGN_INTERNAL_ERROR`. |

## Response Source Matrix

| Response field | Type | Source type | Table/column hoặc generator | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| `success` | `boolean` | Branch constant | Processing result | `5.1/5.2/5.3/5.4` | `true` on success; `false` on error | `N/A` | `N/A` |
| `businessCode` | `string` | Branch constant | Design contract | `5.1/5.2/5.3/5.4` | Fixed `DESIGN_*` code | `N/A` | `N/A` |
| `message` | `string` | Branch message | Application | `5.1-5.5` | Fixed by branch | Text value by branch | Safe fixed message; no provider detail. |
| `data.avatar_url` | `uri` | External result | `OBJECT_STORAGE_PUBLIC_BASE_URL + /avatars/{user_id}` | `3.2/5.1` | Returned as the only `AvatarUploadResult` field | Present on success | API #14 uses this URL to update profile. |
| `meta` | `object` | Envelope default | `N/A` | `5.1/5.2/5.3/5.4` | `{}` | `{}` | Không thêm storage metadata. |
| `traceId` | `uuid` | Correlation generator | `app/core/trace.py` | `5.1-5.5` | Request correlation UUID | Always present | Middleware supplies the trace ID. |

## 0. Check quyền

### 0.1. Get request header

- `authorization`: lấy từ `header["Authorization"]`.
- `content_type`: lấy từ `header["Content-Type"]` nếu transport gửi header này.
- Không nhận `user_id`, `storage_key` hoặc `avatar_url` từ header.

### 0.2. Decode token

- Dùng `app.utils.auth.validate_current_user_request` để verify Bearer JWT theo cấu hình hiện hành.
- Guard kiểm tra chữ ký, expiry, `sub`, `roles` và yêu cầu role `STUDENT`.
- Lấy `user_id` dạng số dương từ claim `sub` để tạo object key.

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

- Route nhận `Content-Type: application/json`.
- Request parser không nhận `multipart/form-data`.
- Body parse/schema error được map thành `422 DESIGN_VALIDATION_ERROR`.

### 1.2. Get request body

- `image`: lấy từ `request["image"]`.
- Không nhận `file`.
- Không nhận `mime_type`.
- Không nhận `size`.
- Không nhận `storage_key`.
- Không nhận `avatar_url`.
- Field ngoài model bị từ chối.

## 2. Validate data input

### 2.1. Check required image

- Nếu body thiếu field `image`: đi tới [06_Error.md](./06_Error.md), error case `7`, HTTP `422`.
- Nếu `image` bằng `null`: đi tới [06_Error.md](./06_Error.md), error case `8`, HTTP `422`.
- Nếu `image` không phải chuỗi: đi tới [06_Error.md](./06_Error.md), error case `9`, HTTP `422`.
- Nếu `image` rỗng: đi tới [06_Error.md](./06_Error.md), error case `10`, HTTP `422`.

### 2.2. Check Data URL and Base64

- Yêu cầu `image` khớp dạng `data:image/<mime>;base64,...`.
- Giải mã Base64 ở chế độ strict; không nhận URL thường, khoảng trắng hoặc multipart.
- Nếu header/Data URL hoặc Base64 sai: đi tới [06_Error.md](./06_Error.md), error case `11`, HTTP `422`.

### 2.3. Check MIME allowlist and size

- Chỉ cho phép MIME `image/png`, `image/jpeg` và `image/webp`.
- Giới hạn kích thước là 5 MiB tính trên bytes sau giải mã.
- Nếu MIME ngoài allowlist: đi tới [06_Error.md](./06_Error.md), error case `12`, HTTP `422`.
- Nếu decoded bytes vượt giới hạn: đi tới [06_Error.md](./06_Error.md), error case `13`, HTTP `422`.

### 2.4. Check image signature

- So khớp PNG/JPEG/WebP signature với MIME khai báo trong Data URL.
- Nếu chữ ký không khớp: đi tới [06_Error.md](./06_Error.md), error case `14`, HTTP `422`.

## 3. Upload avatar

### 3.1. Send avatar to Object Storage

- Gọi S3-compatible provider bằng payload đã giải mã và MIME đã kiểm tra.
- `image_payload`: bytes từ `image` ở step `1.2`.
- `storage_object_key`: `avatars/{user_id}`, trong đó `user_id` đến từ claim `sub` đã xác thực.
- `Content-Type` của object lấy từ MIME đã kiểm tra.
- Không thực hiện `INSERT`, `UPDATE`, `DELETE` hoặc `SELECT` trên database.
- Không cập nhật `users.avatar_url` trong API #13.

### 3.2. Check storage result

- URL thành công được dựng từ `OBJECT_STORAGE_PUBLIC_BASE_URL` và key `avatars/{user_id}`.
- Connect timeout là 5 giây; read timeout là 30 giây; tổng số attempt là 1.
- Thiếu cấu hình đi tới [06_Error.md](./06_Error.md), error case `16-17`, HTTP `500`.
- Provider error hoặc timeout đi tới [06_Error.md](./06_Error.md), error case `18-19`, HTTP `500`.
- Upload lần mới của cùng user ghi đè object cùng key; không có retry hoặc cleanup riêng.

## 4. Response mapping

### 4.1. Map upload result

- Dùng response type `ApiEnvelope<AvatarUploadResult>`.
- `data.avatar_url`: public URL từ provider, chỉ field nghiệp vụ của `AvatarUploadResult`.
- Không gọi API #4 hoặc API #14 từ API #13.

## 5. Trả về response

### 5.1. Success response

- `HTTPStatus = 201`.
- `success = true`.
- `businessCode = DESIGN_RESOURCE_CREATED`.
- `data = {avatar_url}` theo [04_Response.md](./04_Response.md).
- `meta = {}`.
- `traceId = request correlation UUID` do middleware cấp.

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

- Template: `../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/05_Data_Mapping.md`.
- Sheet logic: `3. Data mapping`.
