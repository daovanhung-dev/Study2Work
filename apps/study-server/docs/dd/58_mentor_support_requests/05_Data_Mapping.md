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

### 1.1. Nhận request metadata

- Đọc Authorization header theo Bearer JWT.
- Nếu thiếu hoặc token không hợp lệ, trả 401 DESIGN_AUTHENTICATION_REQUIRED theo [06_Error.md](./06_Error.md#error-cases).

### 1.2. Nhận trace ID

- Đọc X-Trace-Id nếu request gửi theo API Guidelines.
- Nếu header không có, sử dụng trace ID do middleware tạo khi route được wiring.
- Gắn trace ID vào envelope traceId và response header theo convention chung.

## 2. Kiểm tra quyền Mentor

### 2.1. Xác nhận actor

- Yêu cầu role Mentor theo catalog và AC-24.
- Nếu role không được phép, trả 403 DESIGN_ACCESS_DENIED.
- Current shared current-user guard chỉ chấp nhận STUDENT; không dùng guard này cho API #58.

### 2.2. Giới hạn dữ liệu theo Mentor

- AC-24 yêu cầu chỉ đọc request hỗ trợ thuộc phạm vi Mentor.
- V1-PILOT assigned_to_subject_id là nullable UUID candidate; không có source nối Mentor principal với subject ID.
- Không suy ra quyền sở hữu ticket từ course_id query hoặc student enrollment.
- Predicate vật lý chưa chốt cho đến khi identity và assignment semantics được xác nhận.

## 3. Nhận và xử lý query filter

### 3.1. Đọc course_id

- Nếu query có course_id, giữ giá trị int64 làm filter dự kiến.
- Catalog không quy định default, min/max hoặc behavior với course không tồn tại.
- Candidate support_tickets không có course_id/course_version_id; không thêm JOIN qua course_enrollments khi chưa có nguồn.

### 3.2. Đọc status

- Nếu query có status, giữ nguyên chuỗi làm filter candidate.
- Enum values, default, casing và blank behavior chưa được xác nhận.
- Exact equality và kết hợp filter bằng AND là DERIVED, cần xác nhận.
- Catalog không có 422; malformed query/type behavior phải được chốt trước khi wiring.

## 4. Đọc support requests

### 4.1. Query logic Q1

| Target | Column/item | Điều kiện | Remarks |
|---|---|---|---|
| SOURCE_REQUIRED; pilot support_tickets candidate | id, learner_id, status, created_at, resolved_at, assigned_to_subject_id | Scope Mentor; status nếu được gửi | UUID IDs và principal mapping chưa tương thích. |
| SOURCE_REQUIRED | course_id | Filter nếu được gửi | Không có course_id hoặc course relation trên support_tickets. |

- Không viết SQL production cho đến khi chủ model chọn schema và ID contract.
- Không thêm pagination, count, sort hoặc limit vì catalog không khai báo.
- Không suy thứ tự API từ index pilot.

### 4.2. Query logic Q2 — messages

| Target | Column/item | Điều kiện | Remarks |
|---|---|---|---|
| pilot support_messages candidate | id, ticket_id, author_subject_id, author_type, body, attachment_file_ids, sent_at | Candidate ticket_id = support_tickets.id | UUID; không khớp int64 message/author IDs. |

- SupportRequest.messages là field bắt buộc; chưa rõ #58 tải toàn bộ thread hay để #59 tải thread.
- Nếu pilot được duyệt, sent_at ASC, id ASC là thứ tự chronologic DERIVED, không phải contract.

### 4.3. Query logic Q3 — student và attachment

| Target | Column/item | Điều kiện | Remarks |
|---|---|---|---|
| pilot learner_profiles candidate | id, full_name, avatar_file_id | Candidate id = support_tickets.learner_id | UUID; full_name nullable; không có numeric UserSummary mapping. |
| pilot file_objects candidate | id, original_name, declared_mime, detected_mime, size_bytes, scan_status, storage_key | Candidate IDs nằm trong file references | UUID; purpose/status/URL resolver chưa chốt. |

### 4.4. Check cardinality

- Catalog/diagram trả một SupportRequest, trong khi URI/name và AC-24 action là list.
- Nếu Q1 trả 0 hoặc nhiều record, chưa có contract duyệt để mã hóa empty result hoặc danh sách.
- Không lấy bản ghi đầu tiên, cắt kết quả hoặc tự đổi response thành SupportRequest[]/Page.
- Cần chốt response shape trước khi implementation xác định branch trả dữ liệu.

## 5. Map response

### 5.1. SupportRequest

- data.id cần nguồn int64 được xác nhận; pilot ticket ID là UUID, không map trực tiếp.
- data.course_id cần quan hệ hỗ trợ tới course đã được xác nhận; hiện SOURCE_REQUIRED.
- data.student.id/full_name/avatar_url cần identity projection được xác nhận; pilot profile không tương thích trực tiếp.
- data.status cần enum SupportStatus được xác nhận; không tự coi pilot values là enum API.
- data.created_at/resolved_at lấy từ model được chốt; resolved_at optional, null-versus-omit chưa rõ.

### 5.2. SupportMessage

- Map từng message id, author, content, attachments, created_at theo [04_Response.md](./04_Response.md#response-fields).
- Pilot body là candidate cho content; ID và author projection còn SOURCE_REQUIRED.
- Nếu model có is_internal, visibility rule phải được xác nhận trước khi dùng pilot schema.

### 5.3. UploadAsset

- Mỗi attachment phải map đủ id, name, url, content_type, size_bytes, status.
- Không trả storage_key làm URL.
- Không phát URL chưa ký; signer, file purpose và scan eligibility cần nguồn/contract được duyệt.
- Không bịa giá trị hoặc trả asset thiếu field required như mapping đầy đủ.

## 6. Trả envelope

- Success dùng HTTP 200 và DESIGN_RESOURCE_RETRIEVED.
- Envelope gồm success, businessCode, message, data, meta, traceId.
- API Guidelines yêu cầu error data=null; current error_response mặc định {} nếu data không truyền. Đây là discrepancy cần xử lý khi wiring, không tự đổi code trong DD.
- Response paths và JSON example nằm trong [04_Response.md](./04_Response.md#response-fields).

## 7. Xử lý lỗi

- Missing/invalid Bearer JWT → [401 DESIGN_AUTHENTICATION_REQUIRED](./06_Error.md).
- Role hoặc scope không hợp lệ → [403 DESIGN_ACCESS_DENIED](./06_Error.md).
- Lỗi hệ thống ngoài dự kiến → [500 DESIGN_INTERNAL_ERROR](./06_Error.md).
- Không thêm 404, 409, 422 hoặc 503 vì catalog API #58 không khai báo các code đó.
- API read-only nên không có transaction/rollback mutation branch.

## Read-only mapping

- [07_table.md](./07_table.md) giữ theo baseline và ghi N/A — READ-ONLY API.
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
