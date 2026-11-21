---
title: "Data Mapping"
order: 5
dd_id: "58"
api_name: "Lấy support requests"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

## Mục lục

- [1. Nhận request metadata](#1-nhận-request-metadata)
- [2. Kiểm tra quyền Mentor](#2-kiểm-tra-quyền-mentor)
- [3. Nhận và xử lý query filter](#3-nhận-và-xử-lý-query-filter)
- [4. Đọc support requests](#4-đọc-support-requests)
- [5. Map response](#5-map-response)
- [6. Trả envelope](#6-trả-envelope)
- [7. Xử lý lỗi](#7-xử-lý-lỗi)

## 1. Nhận request metadata

### 1.1. Nhận Authorization

- Đọc Bearer JWT qua shared auth helper.
- Yêu cầu role `MENTOR` trước mọi truy vấn DB.
- `sub` phải là positive numeric user ID theo Study Server token convention.

### 1.2. Nhận trace ID

- Đọc `X-Trace-Id` nếu request gửi theo API Guidelines.
- Nếu header không có hoặc không hợp lệ, middleware tạo UUID trace ID.
- Shared response helper đưa trace ID vào envelope và response header.

## 2. Kiểm tra quyền Mentor

### 2.1. Xác nhận actor

- Gọi `validate_current_user_request(..., role="MENTOR")`.
- Thiếu/sai token → 401; token không có role Mentor → 403.

### 2.2. Giới hạn dữ liệu theo Mentor

- Mỗi request được scope qua `support_requests.course_id = courses.id` và `courses.mentor_id = :mentor_id`.
- Nếu có `course_id` và course tồn tại nhưng thuộc Mentor khác, trả 403.
- Nếu `course_id` không tồn tại, truy vấn list không có hàng và trả 200 `data: []` vì catalog không khai báo 404.
- `course_id` query chỉ là filter; không được dùng làm bằng chứng quyền.
- Đây là fallback `DERIVED`, nhất quán với API #46/#49/#54 direct-owner scope.

## 3. Nhận và xử lý query filter

### 3.1. Đọc `course_id`

- Optional positive int64; miền `1..9223372036854775807`.
- Nếu có, truyền parameterized predicate `support_requests.course_id = :course_id`.
- Sai kiểu, số âm/0 hoặc vượt BIGINT → 422 `DESIGN_VALIDATION_ERROR`.

### 3.2. Đọc `status`

- Optional string, không trim hoặc đổi casing.
- Exact match với `support_requests.status`; nếu không có hàng khớp thì trả collection rỗng.
- Query `course_id` và `status` kết hợp bằng AND.
- DDL fallback giới hạn status ở `OPEN`, `IN_PROGRESS`, `WAITING_LEARNER`, `RESOLVED`, `CANCELLED`; status lạ không bị enum-validate ở HTTP layer.

## 4. Đọc support requests

### 4.1. Query logic Q1 — request và student

| Target | Column/item | Điều kiện | Remarks |
|---|---|---|---|
| `support_requests` | `id`, `course_id`, `student_id`, `status`, `created_at`, `resolved_at` | Filter `course_id`/`status` nếu được gửi | Legacy BIGINT fallback; migration 008. |
| `courses` | `id`, `mentor_id` | `courses.id = support_requests.course_id`; `mentor_id = :mentor_id` | Direct-owner predicate; mọi row đều scoped trong SQL. |
| `users` | `id`, `full_name`, `avatar_url` | `users.id = support_requests.student_id` | Numeric UserSummary projection. |

- Stable request order: `support_requests.created_at DESC, support_requests.id DESC`.
- Không có page/size/count; trả toàn bộ các request khớp filter.
- Course precheck chỉ cần khi `course_id` được gửi; list query vẫn giữ predicate owner.

### 4.2. Query logic Q2 — messages và UploadAsset

| Target | Column/item | Điều kiện | Remarks |
|---|---|---|---|
| `support_messages` | `id`, `request_id`, `author_id`, `content`, `created_at` | Join theo request; giữ cùng owner/course/status predicates | Một bulk query, không N+1. |
| `users` | `id`, `full_name`, `avatar_url`, `role` | `users.id = support_messages.author_id` | UserSummary của tác giả. |
| `support_message_uploads` | `message_id`, `upload_id`, `asset_position` | Link message-upload có thứ tự | Bảng nối fallback phục vụ UploadAsset[]. |
| `uploads` | `id`, `owner_id`, `purpose`, `course_id`, `file_name`, `url`, `content_type`, `size_bytes`, `status` | Link ID phải khớp author/course/purpose và `UPLOADED` | `STUDENT`→`SUBMISSION`; `MENTOR`→`LECTURE`. |

- Message order trong mỗi request: `created_at ASC, id ASC`.
- Attachment order: `asset_position ASC`.
- Không có message thì `messages: []`; không có attachment thì `attachments: []`.
- Link tồn tại nhưng metadata không thỏa owner/course/purpose/status hoặc projection bị thiếu thì mapping lỗi an toàn thành 500, không trả asset một phần.

### 4.3. Cardinality và result set

- Collection response: `SupportRequest[]`, chọn từ list path/action của AC-24.
- Không lấy row đầu, không phân trang và không cắt thread vì request schema không khai báo page/size/message limit.
- Không có kết quả → HTTP 200, `data: []`, message `No support requests found.`.

## 5. Map response

### 5.1. `SupportRequest`

- `id`, `course_id`, `status`, `created_at`, `resolved_at` lấy từ `support_requests`.
- `student` map từ `users` theo `student_id`; `full_name` là required theo legacy DDL, `avatar_url` optional.
- `messages` được khởi tạo rỗng cho mọi request rồi được group từ Q2.
- `resolved_at` NULL bị omit theo `response_model_exclude_none=True`.

### 5.2. `SupportMessage`

- Map `id`, `content`, `created_at` từ `support_messages`.
- `author` map từ `users` theo `author_id`.
- Tạo đúng một message cho mỗi `message_id`, dù query có nhiều attachment rows.
- Dữ liệu lặp giữa các attachment rows phải nhất quán; projection mâu thuẫn → 500.

### 5.3. `UploadAsset`

- Map `id`, `name`, `url`, `content_type`, `size_bytes`, `status` từ `uploads`.
- Kiểm tra owner trùng tác giả, course trùng request, purpose khớp vai trò tác giả và status là `UPLOADED`.
- Không trả `storage_key`; URL lấy từ metadata API #34.

## 6. Trả envelope

- Success dùng HTTP 200 và `DESIGN_RESOURCE_RETRIEVED`.
- Envelope gồm `success`, `businessCode`, `message`, `data`, `meta`, `traceId`; `meta` là `{}` vì endpoint không phân trang.
- Empty collection vẫn là success với `data: []`.
- Error envelope dùng shared helper; error `data` serialize thành `null`.

## 7. Xử lý lỗi

- Missing/invalid Bearer JWT → 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Sai role hoặc course thuộc Mentor khác → 403 `DESIGN_ACCESS_DENIED`.
- Query `course_id` không parse/range hợp lệ → 422 `DESIGN_VALIDATION_ERROR`.
- DB, row mapping, required relation hoặc asset-link integrity lỗi → 500 `DESIGN_INTERNAL_ERROR`.
- Read-only API không commit; rollback transaction an toàn trên DB/mapping error.

## Read-only mapping

- [07_table.md](./07_table.md) ghi `N/A — READ-ONLY API`.
- DDL/migration là source artifact; API source tests không chứng minh live database đã áp dụng migration 008.

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
