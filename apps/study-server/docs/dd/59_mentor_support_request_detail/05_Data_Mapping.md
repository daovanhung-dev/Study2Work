---
title: "Data Mapping"
order: 5
dd_id: "59"
api_name: "Lấy nội dung request/thread"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

## Mục lục

- [1. Nhận request metadata](#1-nhận-request-metadata)
- [2. Kiểm tra quyền Mentor](#2-kiểm-tra-quyền-mentor)
- [3. Đọc request_id](#3-đọc-request_id)
- [4. Đọc request và conversation](#4-đọc-request-và-conversation)
- [5. Map response](#5-map-response)
- [6. Trả envelope](#6-trả-envelope)
- [7. Xử lý lỗi](#7-xử-lý-lỗi)

## 1. Nhận request metadata

### 1.1. Xác thực Bearer JWT

- Dùng `validate_current_user_request(..., role="MENTOR")`.
- Thiếu/invalid token → 401 `DESIGN_AUTHENTICATION_REQUIRED`; role không phù hợp → 403 `DESIGN_ACCESS_DENIED`.
- Guard trả numeric JWT subject `mentor_id` theo current Study auth convention.

### 1.2. Nhận trace ID

- Middleware validate `X-Trace-Id` hoặc tạo UUID khi thiếu/sai.
- `success_response`/`error_response` trả cùng trace trong envelope và header.

## 2. Kiểm tra quyền Mentor

### 2.1. Đọc request và owner

- Q1 tra `support_requests.id = :request_id` và lấy `courses.mentor_id`; view so sánh owner với JWT `sub` sau khi kiểm tra parent projection.
- Không có request → 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Request tồn tại nhưng `course.mentor_id != :mentor_id` → 403 `DESIGN_ACCESS_DENIED`.
- Thứ tự 404 rồi 403 kế thừa API #48/#55; có thể tiết lộ resource existence theo catalog semantics, chưa có privacy override riêng.

### 2.2. Giới hạn mọi query

- Q1 lấy request theo primary key rồi map course owner để check quyền trong view; owner mismatch không kích hoạt Q2.
- Q2 lặp `course.mentor_id = :mentor_id` và cùng `request.id` để chỉ đọc thread trong scope.
- `request_id` không được dùng làm quyền; access luôn gắn với JWT subject/course owner.

## 3. Đọc request_id

### 3.1. Path parameter

| Item | Contract | Parse/mapping | Status |
|---|---|---|---|
| `request_id` | Required signed int64 | Route giữ raw string; strict signed-decimal parser giới hạn `[-2^63, 2^63-1]`. | Type DIRECT; parse fallback theo API #48. |
| Malformed/out-of-range | N/A | Trả 404 `DESIGN_RESOURCE_NOT_FOUND`; không thêm 422. | DERIVED để giữ catalog error set. |
| Negative/zero | Int64 biểu diễn được | Query theo ID; không có positive BIGSERIAL tương ứng nên trả 404. | DERIVED từ khóa local BIGSERIAL. |

## 4. Đọc request và conversation

### 4.1. Q1 — SupportRequest detail và Student

| Target | Column/item | Điều kiện | Remarks |
|---|---|---|---|
| `support_requests AS request` | `id`, `course_id`, `student_id`, `status`, `created_at`, `resolved_at` | `request.id = :request_id` | Legacy BIGINT fallback từ API #58; migration 008. |
| `courses AS course` | `id`, `mentor_id` | `course.id = request.course_id` | LEFT JOIN để nhận biết quan hệ course hỏng; owner check sau khi row tồn tại. |
| `users AS student` | `id`, `full_name`, `avatar_url` | `student.id = request.student_id` | LEFT JOIN; missing/broken required Student projection là 500. |

- Q1 phải trả tối đa một request. Duplicate hoặc sai kiểu/required field trong projection là 500 an toàn.
- SupportRequest IDs, course IDs và Student IDs map BIGINT → int64; V1-PILOT UUID tables không tham gia.
- `status` được trả như string trong contract; enum candidate từ DDL fallback là `OPEN`, `IN_PROGRESS`, `WAITING_LEARNER`, `RESOLVED`, `CANCELLED`.

### 4.2. Q2 — Messages và author

| Target | Column/item | Điều kiện | Remarks |
|---|---|---|---|
| `support_messages AS message` | `id`, `request_id`, `author_id`, `content`, `created_at` | `message.request_id = :request_id` | Read-only; FK đến request/user theo migration 008. |
| `users AS author` | `id`, `role`, `full_name`, `avatar_url` | `author.id = message.author_id` | LEFT JOIN; required author FK/projection lỗi là 500. |
| `support_requests AS request` + `courses AS course` | `request.id`, `request.course_id`, `course.mentor_id` | request ID và `course.mentor_id = :mentor_id` | Lặp scope predicate trong Q2. |

- Trả mọi message theo reusable `messages[]`, order `message.created_at ASC, message.id ASC`.
- Không có message → `messages: []`.
- Fallback `support_messages` không có `is_internal`; không có private-message flag trong selected local model nên mọi row đều được trả.
- Query join có thể nhân dòng khi message có nhiều attachments; chỉ tạo một message theo ID, kiểm tra fields lặp nhất quán rồi append asset theo `asset_position ASC`.

### 4.3. Q3 — UploadAsset links

| Target | Column/item | Join/predicate | Remarks |
|---|---|---|---|
| `support_message_uploads AS message_upload` | `message_id`, `upload_id`, `asset_position` | `message_upload.message_id = message.id` | Ordered relation thêm ở API #58 migration 008. |
| `uploads AS upload` | `id`, `owner_id`, `course_id`, `purpose`, `file_name`, `url`, `content_type`, `size_bytes`, `status` | ID link; owner = message author; course = request course; purpose theo author role; status `UPLOADED` | Reuse API #34 UploadAsset metadata và API #58 resolver. |

- `STUDENT` → `SUBMISSION`; `MENTOR` → `LECTURE`; course phải bằng request course.
- `upload.id` phải bằng `message_upload.upload_id`. Link có metadata thiếu/sai scope không được trả partial; mapping trả 500 an toàn.
- Không trả storage key; response `url` lấy trực tiếp `uploads.url` theo API #34.

## 5. Map response

### 5.1. SupportRequest

- `data.id/course_id/status/created_at/resolved_at` map từ Q1.
- `data.student` map từ `users`; ID numeric, `full_name` required, optional `avatar_url`.
- `data.messages[]` map từ Q2/Q3 với toàn bộ author/content/attachments/time fields theo reusable `SupportRequestResponse` từ API #58.
- Omit optional `avatar_url`/`resolved_at` khi NULL theo `response_model_exclude_none=True`/API #58.

### 5.2. Integrity failures

- Missing required course/student/author, sai typed ID, duplicate inconsistent message, hoặc attachment link không resolve đúng owner/course/purpose/status → 500 `DESIGN_INTERNAL_ERROR`.
- Không trả một phần thread khi projection lỗi.

## 6. Trả envelope

- Success HTTP 200 `DESIGN_RESOURCE_RETRIEVED` với đúng một `SupportRequest` object.
- Message success: `Support request retrieved.`; `meta: {}`; trace ID theo middleware.
- Không commit; đây là GET chỉ đọc.

## 7. Xử lý lỗi

- Bearer/JWT invalid → 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Role sai hoặc request hiện hữu thuộc direct course owner khác → 403 `DESIGN_ACCESS_DENIED`.
- Malformed/out-of-int64 path hoặc request không tồn tại → 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Query/projection/link integrity failure → 500 `DESIGN_INTERNAL_ERROR`; log theo trace, không lộ SQL/row nội bộ.
- Error envelope dùng `data:null` qua shared `error_response(...)`; không thêm 422/409/503.

## Read-only mapping

- [07_table.md](./07_table.md) ghi `N/A — READ-ONLY API`; API #60/#61 sở hữu mutation tương ứng.

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `3. Data mapping`
- Dimension: `B1:BB61`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `63`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Flow xử lý data |  |
| 4 | `D4` | 0. |  |
| 4 | `E4` | Check quyền |  |
| 5 | `E5` | ・ |  |
| 5 | `F5` | Thực hiện check quyền |  |
| 6 | `E6` | ・ |  |
| 6 | `F6` | Get count khi get data từ … |  |
| 7 | `G7` | Table get |  |
| 7 | `K7` | : |  |
| 8 | `G8` | Conditions |  |
| 8 | `K8` | : |  |
| 10 | `E10` | ・ |  |
| 10 | `F10` | Trường hợp giá trị get được lớn hơn 0, thực hiện các xử lý tiếp theo |  |
| 11 | `E11` | ・ |  |
| 11 | `F11` | Trường hợp giá trị get được bằng 0, trả về status 2 |  |
| 13 | `D13` | 1. |  |
| 13 | `E13` | validate data input |  |
| 14 | `F14` | refer sheet [４．Error] |  |
| 16 | `D16` | 2. |  |
| 16 | `E16` | Get thông tin… |  |
| 18 | `F18` | Table get |  |
| 18 | `K18` | Column get |  |
| 18 | `P18` | Chú thích |  |
| 18 | `U18` | Remarks |  |
| 29 | `F29` | Target table / join condition |  |
| 30 | `F30` | Target table |  |
| 30 | `N30` | Join condition |  |
| 30 | `AL30` | 結合種類 |  |
| 31 | `F31` | txn_ams_t0320 AS a |  |
| 32 | `F32` | txn_amm_v0002 AS b |  |
| 32 | `N32` | ON a . chy_typ = b . kbn_typ AND b . dmin_cd = A AND b . kbnknr_cd = 001 |  |
| 32 | `AL32` | LEFT JOIN |  |
| 33 | `F33` | txn_amm_v0002 AS c |  |
| 33 | `N33` | ON a . chy_typ = c . kbn_typ AND c . dmin_cd = A AND c . kbnknr_cd = Z02 |  |
| 33 | `AL33` | LEFT JOIN |  |
| 35 | `F35` | ・ |  |
| 35 | `G35` | Điều kiện get data |  |
| 37 | `F37` | ・ |  |
| 37 | `G37` | Điều kiện sort |  |
| 41 | `D41` | 3. |  |
| 41 | `E41` | Insert/Update thông tin … |  |
| 42 | `E42` | Update table…. |  |
| 43 | `E43` | ・ |  |
| 43 | `F43` | Items update |  |
| 44 | `F44` | ・ |  |
| 44 | `G44` | Refer sheet [xxxx] |  |
| 45 | `E45` | ・ |  |
| 45 | `F45` | Điều kiện get data |  |
| 46 | `F46` | ・ |  |
| 46 | `G46` | auth_user. id = user hiện tại theo token |  |
| 48 | `D48` | 4. |  |
| 48 | `E48` | check kết quả execute query  |  |
| 49 | `E49` | 1. Thành công |  |
| 50 | `F50` | HTTPStatus = 200 |  |
| 51 | `F51` | Trả về kết quả status = 1 |  |
| 52 | `E52` | 2. Lỗi hệ thống phát sinh |  |
| 53 | `F53` | HTTPStatus = 500 |  |
| 54 | `F54` | Trả về kết quả status = 2 |  |
| 55 | `E55` | 3. Validate lỗi |  |
| 56 | `F56` | HTTPStatus = 400 |  |
| 57 | `F57` | Trả về kết quả status = 2 |  |
| 58 | `E58` | 4. Ngoài trường hợp trên |  |
| 59 | `F59` | Trả về kết quả status = 2 |  |

</details>
