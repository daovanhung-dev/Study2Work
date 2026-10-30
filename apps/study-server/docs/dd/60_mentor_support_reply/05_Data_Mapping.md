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

- [1. Nhận metadata và xác thực](#1-nhận-metadata-và-xác-thực)
- [2. Parse request](#2-parse-request)
- [3. Lock và kiểm tra SupportRequest](#3-lock-và-kiểm-tra-supportrequest)
- [4. Resolve UploadAsset references](#4-resolve-uploadasset-references)
- [5. Insert SupportMessage](#5-insert-supportmessage)
- [6. Insert message-upload links](#6-insert-message-upload-links)
- [7. Rehydrate response và commit](#7-rehydrate-response-và-commit)
- [8. Xử lý lỗi](#8-xử-lý-lỗi)

## 1. Nhận metadata và xác thực

### 1.1. Bearer JWT

- Gọi validate_current_user_request(..., role="MENTOR") trước DB access.
- JWT sub phải ánh xạ numeric users.id theo current Study auth guard.
- Thiếu/invalid token → 401 DESIGN_AUTHENTICATION_REQUIRED; role sai → 403 DESIGN_ACCESS_DENIED.

### 1.2. Trace ID

- Middleware validate X-Trace-Id hoặc tạo UUID.
- Shared response helper trả cùng trace trong envelope và header.

## 2. Parse request

### 2.1. Path request_id

- Route giữ raw path string; parser chấp nhận signed decimal nằm trong miền [-2^63, 2^63-1].
- Sai format/overflow → 422 DESIGN_VALIDATION_ERROR, field request_id.
- Không áp dụng positive constraint vì catalog không khai báo minimum; zero/negative không khớp BIGSERIAL row và sẽ 404.

### 2.2. Body message

- Body strict model yêu cầu message:string và attachment_refs:string; extra fields bị từ chối.
- message.strip() rỗng → 422; khi hợp lệ lưu chính xác chuỗi gốc.
- Không thêm min/max length, trim nội dung, markdown policy hoặc sanitizer chưa có nguồn.

### 2.3. Body attachment_refs

- Decode JSON string thành list; chỉ nhận JSON integer thật trong miền signed int64.
- [] là không có attachment; reject malformed JSON, list sai kiểu, float, boolean, duplicate ID bằng 422.
- Wire key attachment_refs và JSON encoding là DERIVED từ current API #47 asset_refs source; không thay đổi API #35/#47.

## 3. Lock và kiểm tra SupportRequest

### 3.1. Q1 — request + course + learner

| Target | Columns | Join/predicate | Mapping |
|---|---|---|---|
| support_requests AS request | id, course_id, student_id, status, created_at, resolved_at | request.id = :request_id; FOR UPDATE OF request | Local BIGINT fallback from migration 008. |
| courses AS course | id, mentor_id | LEFT JOIN course.id = request.course_id | Required parent projection; direct owner check. |
| users AS student | id, full_name, avatar_url | LEFT JOIN student.id = request.student_id | Required learner projection. |

- No row → 404 DESIGN_RESOURCE_NOT_FOUND.
- Broken course/student projection → 500 DESIGN_INTERNAL_ERROR; do not treat corrupt parent as missing request.
- Existing row with course.mentor_id != JWT sub → 403 DESIGN_ACCESS_DENIED.
- Scope uses direct course owner; no assigned-Mentor relation is source-backed in this fallback.
- The request row lock serializes reply inserts with a future resolve implementation that locks the same row; API #60 itself does not gate on status.

## 4. Resolve UploadAsset references

### 4.1. Q2 — metadata lookup

| Target | Columns | Predicate | Status |
|---|---|---|---|
| uploads AS upload | id, owner_id, course_id, purpose, file_name, url, content_type, size_bytes, status | upload.id = ANY(:asset_ids); owner_id=:mentor_id; course_id=:request_course_id; purpose='LECTURE'; status='UPLOADED' | Reuse API #34 metadata and API #47 query pattern. |

- [] skips Q2.
- Compare resolved ID set/count with requested IDs and restore request order in memory.
- Any syntactically valid ID not resolvable under all scope predicates → generic 404 DESIGN_RESOURCE_NOT_FOUND; do not reveal cross-owner existence.
- Query failure → rollback and safe 500.

## 5. Insert SupportMessage

### 5.1. M1 — INSERT

| Table | Columns | Values | Source/status |
|---|---|---|---|
| support_messages | request_id | Locked request ID | Q1; local migration 008. |
| support_messages | author_id | JWT sub | Shared MENTOR guard; local numeric user ID. |
| support_messages | content | Request message | Original nonblank text. |
| support_messages | created_at | Omitted; database CURRENT_TIMESTAMP | Migration 008 default; local fallback. |
| support_messages | id | Omitted; BIGSERIAL | Migration 008 generator. |

- INSERT ... RETURNING id, created_at must return one valid row.
- No is_internal/author_type field exists in the selected local table; replies appear in the shared visible thread under the #58/#59 fallback.
- Do not update support_requests.status, resolved_at or timestamps at API #60.

## 6. Insert message-upload links

### 6.1. M2 — ordered INSERT

| Table | Column | Value | Rule |
|---|---|---|---|
| support_message_uploads | message_id | M1 returned id | FK to inserted support_messages.id. |
| support_message_uploads | upload_id | Resolved UploadAsset IDs | Preserve attachment_refs order. |
| support_message_uploads | asset_position | Array ordinal - 1 | Zero-based integer; unique per message. |

- Use UNNEST(... WITH ORDINALITY) so each accepted upload gets its request position.
- Skip M2 for []. Any insert/link count or position mismatch → rollback and 500.
- Storage bytes/object and uploads metadata are not written by this endpoint; API #34 owns upload.

## 7. Rehydrate response và commit

### 7.1. Q3 — current request/thread

- Re-read request/course/student and full message thread using API #59 predicates and projection.
- Keep direct course.mentor_id=:mentor_id in the thread query.
- Thread order is message.created_at ASC, message.id ASC; assets order by asset_position ASC. No pagination/limit exists in the contract or #59 fallback.
- Shared pure support-request projection is used by APIs #59 and #60 to validate parents, users, message consistency and scoped asset rows.
- Verify the newly inserted message is present and attachments match the inserted link rows; any projection failure rolls back the whole transaction.

### 7.2. Response/transaction

- Validate ApiEnvelope<SupportRequest> with success=true, businessCode=DESIGN_RESOURCE_UPDATED and meta={} before commit.
- Commit once after the complete data projection is valid.
- SQL, link, projection or commit failure → safe 500; attempt rollback and do not return partial thread.

## 8. Xử lý lỗi

- Bearer/JWT invalid → 401 DESIGN_AUTHENTICATION_REQUIRED.
- Role mismatch or request owned by another Mentor → 403 DESIGN_ACCESS_DENIED.
- Missing request or unresolved/out-of-scope upload refs → 404 DESIGN_RESOURCE_NOT_FOUND.
- Invalid int64 path, missing/wrong body fields, blank message, malformed/duplicate/non-int64 ref array → 422 DESIGN_VALIDATION_ERROR.
- DB, required-parent, write/link, projection or commit failure → 500 DESIGN_INTERNAL_ERROR; log only trace, never SQL or raw exception to client.
- No status mutation, reopen, notification, 409 or 503.

## Mapping files

- SupportMessage insert: [07_support_messages_insert.md](./07_support_messages_insert.md).
- Ordered attachment relation insert: [08_support_message_uploads_insert.md](./08_support_message_uploads_insert.md).
- API #61 owns SupportRequest resolve/status mutation.

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
