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

- Đọc Authorization header theo contract.
- Token thiếu hoặc không hợp lệ ánh xạ sang 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Current Study source chưa có Mentor guard; chưa xác nhận claim/subject mapping.

### 1.2. Nhận trace ID

- Đọc `X-Trace-Id` nếu client gửi theo API Guidelines.
- Khi được wiring, dùng trace ID đã validate hoặc ID do middleware tạo trong envelope/header.
- Hiện API #59 chưa có route, nên đây là convention dự kiến.

## 2. Kiểm tra quyền Mentor

### 2.1. Xác nhận role

- Catalog yêu cầu Bearer JWT với role Mentor.
- Role khác hoặc quyền truy cập bị từ chối ánh xạ 403 `DESIGN_ACCESS_DENIED`.
- Không dùng current Student-only guard như bằng chứng Mentor authorization.

### 2.2. Giới hạn request theo scope

- AC-24 precondition yêu cầu request nằm trong phạm vi phụ trách của Mentor.
- Chủ thể/assignment key và predicate vật lý chưa được xác nhận.
- Không dùng path ID làm bằng chứng ownership; không suy ra quyền qua course/enrollment.
- Thứ tự kiểm tra tồn tại và quyền cần được xác nhận nếu có yêu cầu che giấu sự tồn tại resource.

## 3. Đọc request_id

### 3.1. Path parameter

| Item | Kiểu contract | Candidate source | Điều kiện | Trạng thái |
|---|---|---|---|---|
| `request_id` | required int64 | Chưa có khóa vật lý được duyệt | Dùng làm logical key tra một SupportRequest | DIRECT type; physical mapping `SOURCE_REQUIRED` |

- Catalog không quy định range ngoài int64 hoặc error code 422.
- Pilot `support_tickets.id` là UUID, không cast hoặc đổi định dạng để giả lập int64.
- Path thiếu/sai kiểu/overflow khi route được wiring cần được xác nhận theo đúng error contract.

## 4. Đọc request và conversation

### 4.1. Q1 — SupportRequest detail

| Target | Column/item | Điều kiện | Remarks |
|---|---|---|---|
| SOURCE_REQUIRED; pilot `support_tickets` candidate | id, learner_id, status, created_at, resolved_at, assigned_to_subject_id | Request ID và Mentor scope | UUID IDs; không có course_id; schema chưa được chọn làm runtime model. |

- Logical behavior là đọc đúng một SupportRequest theo request_id và scope Mentor.
- Không có physical SQL được duyệt do contract int64 và candidate UUID không tương thích.
- Không có dòng phù hợp ánh xạ 404 `DESIGN_RESOURCE_NOT_FOUND` theo catalog; trường hợp ngoài scope ánh xạ 403 `DESIGN_ACCESS_DENIED`.
- Không tự chốt check order nếu cần tránh resource enumeration.

### 4.2. Q2 — Conversation/messages

| Target | Column/item | Điều kiện | Remarks |
|---|---|---|---|
| SOURCE_REQUIRED; pilot `support_messages` candidate | id, ticket_id, author_subject_id, author_type, body, attachment_file_ids, is_internal, sent_at | Candidate liên kết ticket ID | UUID keys; message visibility, order, bound và mapping chưa được duyệt. |

- `SupportRequest.messages[]` là field bắt buộc theo catalog.
- Diagram gọi bước này là “Đọc request + conversation”; không định nghĩa thứ tự hay giới hạn.
- Không mặc định loại hoặc đưa `is_internal=true` messages; visibility cần owner xác nhận.
- Không áp dụng sort `sent_at,id` dù pilot có index tương ứng; đó chưa phải contract.

### 4.3. Q3 — Student, author và attachments

| Target | Candidate fields | Mapping need | Status |
|---|---|---|---|
| Identity/profile projection | learner/student ID, author subject ID, full_name, avatar | Numeric UserSummary IDs; non-null name; optional avatar URI | `SOURCE_REQUIRED` |
| File metadata/resolver | file ID, original_name, MIME, size, scan state, storage key | Numeric UploadAsset ID, name, URL, content_type, size_bytes, UploadStatus | `SOURCE_REQUIRED` |

- Không đưa `storage_key` vào trường `url`.
- Không tự chọn declared MIME hay detected MIME.
- Không map scan status thành UploadStatus khi chưa có enum/lifecycle contract.
- Không phát link chưa ký hoặc file chưa đủ điều kiện truy cập theo policy được duyệt.

## 5. Map response

### 5.1. SupportRequest

- `data.id`, `course_id`, `student.id` và `status` cần nguồn/enum khớp contract; pilot UUID/status không được map ngầm.
- `created_at` và optional `resolved_at` có cột candidate trong pilot ticket nhưng chưa phải approved runtime source.
- `messages[]` phải biểu diễn thread theo contract; message visibility, thứ tự, giới hạn và empty array behavior cần chốt.

### 5.2. SupportMessage và UploadAsset

- Map author thành `UserSummary`; ID/profile/avatar resolver cho Learner và Mentor/Staff chưa có source.
- `body → content`, `sent_at → created_at`, `original_name → name` chỉ là candidate aliases, không phải mapping được duyệt.
- Mỗi attachment cần đủ id, name, url, content_type, size_bytes, status; hiện chưa có projection/resolver tương thích.

### 5.3. Envelope

- Success HTTP 200, business code `DESIGN_RESOURCE_RETRIEVED`.
- Envelope gồm success, businessCode, message, data, meta, traceId.
- API Guidelines nêu `data:null` cho error; current helper mặc định `{}` khi không truyền data. Đây là discrepancy có điều kiện cho future wiring.

## 6. Trả envelope

- Trả một `SupportRequest` object, không array/Page.
- Không thêm field ngoài catalog hoặc dữ liệu internal chưa được policy cho phép.
- Response field-by-field được liệt kê tại [04_Response.md](./04_Response.md#response-fields).

## 7. Xử lý lỗi

- Missing/invalid Bearer JWT → 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Sai role hoặc request ngoài scope → 403 `DESIGN_ACCESS_DENIED`.
- Request không tìm thấy → 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Lỗi nội bộ → 500 `DESIGN_INTERNAL_ERROR`.
- Không thêm 409/422/503; catalog #59 không khai báo các code này.
- API read-only nên không có commit/rollback mutation branch.

## Read-only mapping

- [07_table.md](./07_table.md) ghi `N/A — READ-ONLY API`.

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
