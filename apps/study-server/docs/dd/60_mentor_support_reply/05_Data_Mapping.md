---
title: "Data Mapping"
order: 5
dd_id: "60"
api_name: "Gửi phản hồi"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

## Mục lục

- [1. Nhận request metadata](#1-nhận-request-metadata)
- [2. Kiểm tra quyền Mentor](#2-kiểm-tra-quyền-mentor)
- [3. Validate request](#3-validate-request)
- [4. Đọc request và resolve attachment refs](#4-đọc-request-và-resolve-attachment-refs)
- [5. Ghi SupportMessage](#5-ghi-supportmessage)
- [6. Rehydrate SupportRequest](#6-rehydrate-supportrequest)
- [7. Transaction và lỗi](#7-transaction-và-lỗi)
- [8. Trả envelope](#8-trả-envelope)

## 1. Nhận request metadata

### 1.1. Xác thực Bearer JWT

- Đọc Authorization header.
- Token thiếu hoặc không hợp lệ → 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Catalog yêu cầu Mentor; current Student guard không được dùng thay Mentor guard.

### 1.2. Trace ID

- Đọc `X-Trace-Id` nếu có theo API Guidelines.
- Khi route được wiring, propagate trace đã validate hoặc trace do middleware tạo vào envelope/header.

## 2. Kiểm tra quyền Mentor

### 2.1. Xác nhận role

- Role phải là Mentor theo catalog và AC-24.
- Sai role hoặc request ngoài quyền → 403 `DESIGN_ACCESS_DENIED`.
- Claim shape và subject-to-database key mapping chưa có current source.

### 2.2. Giới hạn SupportRequest

- AC-24 precondition: request thuộc phạm vi phụ trách của Mentor.
- Không dùng path ID, `attachment_refs` hoặc course value do client gửi làm bằng chứng quyền.
- Pilot `assigned_to_subject_id` nullable UUID là candidate, không phải approved predicate.
- Quy tắc 404 khi không tồn tại và 403 khi ngoài scope đúng catalog; thứ tự check/privacy policy cần xác nhận.

## 3. Validate request

### 3.1. Path `request_id`

| Item | Type | Use | Status |
|---|---|---|---|
| `request_id` | required int64 | Logical lookup một support request | Type DIRECT; pilot key UUID không tương thích; no SQL finalized |

- Không thêm range/positive constraint ngoài int64 vì catalog không quy định.
- Parse error behavior khi route được wiring phải giữ error contract đã khai báo; không tự thêm 400/409.

### 3.2. Body `message`

- Catalog yêu cầu string.
- Proposal đơn giản: dùng `message.strip()` chỉ để kiểm tra; nếu rỗng/whitespace-only trả 422 `DESIGN_VALIDATION_ERROR`; lưu nguyên chuỗi gốc để giữ xuống dòng/format.
- Không thêm min/max length hoặc loại bỏ ký tự vì contract chưa quy định.
- Đây là `DERIVED`; cần API owner xác nhận trước implementation.

### 3.3. Body attachment references

- Catalog notation là required `attachment refs:string!`.
- Proposed wire field: `attachment_refs` (`DERIVED` theo precedent #47 `asset_refs`).
- Proposed representation: comma-separated int64 `UploadAsset.id`; empty string `""` nghĩa là không đính kèm. Cần harmonize với #35 `file refs` và #47 `asset refs`.
- Không parse, cast, deduplicate hay query `file_objects` theo proposal trước khi #34 ID/registry được duyệt.
- Missing/wrong type/format invalid sau khi proposal được duyệt → 422 `DESIGN_VALIDATION_ERROR`.

## 4. Đọc request và resolve attachment refs

### 4.1. Q1 — Request scope/existence

| Target | Field | Predicate/purpose | Remarks |
|---|---|---|---|
| SOURCE_REQUIRED; V1-PILOT `support_tickets` candidate | id, learner_id, status, assigned_to_subject_id | Locate request by path ID and scope it to authenticated Mentor | Ticket ID UUID, no course relation; no production SQL. |

- Không tìm thấy request theo access rule được duyệt → 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Request ngoài phạm vi Mentor → 403 `DESIGN_ACCESS_DENIED`.
- Không chốt check order nếu privacy policy chưa xác nhận.

### 4.2. Q2 — Resolve attachment refs

| Target | Candidate fields | Check required before insert | Status |
|---|---|---|---|
| API #34 UploadAsset registry (not established); V1-PILOT `file_objects` candidate | id, owner_subject_id, purpose, scan_status, storage_key, original_name, MIME, size_bytes | Resolve every ref; validate allowed uploader/purpose/state and build UploadAsset response projection | `SOURCE_REQUIRED`; pilot IDs UUID |

- API #34 has no approved metadata persistence/lookup in its DD; do not treat the storage URL or ref string as safe metadata.
- `attachment_file_ids` in pilot support_messages is UUID[]; a direct int64 list cannot populate it without an approved identity mapping.
- If the proposal is approved, malformed/missing asset reference may map to 422; cross-user/cross-purpose access may map to 403. Exact branch mapping remains open.

## 5. Ghi SupportMessage

### 5.1. M1 — Logical INSERT

| Logical field | Pilot candidate column | Candidate value | Status |
|---|---|---|---|
| Message ID | `id` | Generated ID | pilot UUID, no DB default; contract int64; `SOURCE_REQUIRED` |
| Support request ID | `ticket_id` | Related request key | pilot UUID vs path int64; `SOURCE_REQUIRED` |
| Mentor author | `author_subject_id` | Authenticated Mentor subject | identity mapping `SOURCE_REQUIRED` |
| Author type | `author_type` | `STAFF` | Candidate enum; Mentor→STAFF `DERIVED` |
| Message body | `body` | `message` request value | Alias candidate; no length limit |
| Attachment refs | `attachment_file_ids` | Resolved file IDs | pilot UUID[] vs UploadAsset int64; `SOURCE_REQUIRED` |
| Learner visibility | `is_internal` | `false` | pilot default; public reply interpretation `DERIVED` |
| Message time | `sent_at` | Server-generated time | pilot required/no default; clock/timezone `SOURCE_REQUIRED` |

- Diagram xác nhận effect `INSERT SupportMessage`; không xác nhận table/columns.
- Không update status/ticket timestamp tại API #60. Diagram để API #61 ghi `status=RESOLVED`; nhánh NO giữ OPEN.
- Đây là candidate mapping, không phải SQL đã duyệt.

## 6. Rehydrate SupportRequest

- Sau logical insert, đọc lại SupportRequest/thread và map reply mới vào `messages[]`; contract yêu cầu response object `ApiEnvelope<SupportRequest>`.
- Response phải giữ status request hiện tại; API #60 không giải quyết request.
- SupportRequest/course/student/status, author UserSummary, attachments UploadAsset[] và message ordering cần approved source/resolver.
- Nếu API #34 asset resolver không thể trả đủ fields, không tạo UploadAsset giả hoặc storage URL từ ref.

## 7. Transaction và lỗi

### 7.1. Candidate transaction boundary

- Sau auth, request-scope và attachment checks, insert và rehydrate trong một transaction do caller/use case sở hữu.
- Chỉ commit sau khi đầy đủ response mapping; lỗi DB/projection trước commit → rollback insert.
- Current `get_db()` chỉ yield/close Session; `execute_query` không commit. Đây là current helper convention, không phải API #60 runtime.

### 7.2. Error mapping

- Missing/invalid Bearer → 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Wrong role/request scope/file access bị từ chối → 403 `DESIGN_ACCESS_DENIED` (file branch là proposal cần confirm).
- Request không tồn tại → 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Body validation/reference format → 422 `DESIGN_VALIDATION_ERROR`.
- Query, insert, asset projection hoặc unexpected mapping failure → 500 `DESIGN_INTERNAL_ERROR`.
- Không thêm 409 hoặc 503; catalog #60 không khai báo các code đó.

## 8. Trả envelope

- HTTP 200, business code `DESIGN_RESOURCE_UPDATED`, data là SupportRequest có reply mới.
- Envelope gồm success, businessCode, message, data, meta, traceId.
- API Guidelines error `data:null` và current helper default `{}` là conditional discrepancy khi route được wiring.
- Xem field-level projection tại [04_Response.md](./04_Response.md).

## Mapping table

- [07_table.md](./07_table.md) ghi pilot `support_messages` columns dưới nhãn candidate và liệt kê ID/schema mismatch.

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
