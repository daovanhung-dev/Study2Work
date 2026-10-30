---
title: "Data Mapping"
order: 5
dd_id: "61"
api_name: "Đóng yêu cầu hỗ trợ"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

## Mục lục

- [1. Nhận metadata request](#step-1)
- [2. Kiểm tra quyền Mentor](#step-2)
- [3. Đọc và kiểm tra request_id](#step-3)
- [4. Khóa SupportRequest và trạng thái](#step-4)
- [5. Resolve request](#step-5)
- [6. Nạp thread response](#step-6)
- [7. Giao dịch và trả kết quả](#step-7)
- [8. Xử lý lỗi](#step-8)

<a id="step-1"></a>

## 1. Nhận metadata request

### 1.1. Xác thực Bearer JWT

- Dùng `validate_current_user_request(..., role="MENTOR")` trước mọi DB query.
- Guard hiện tại đọc numeric `sub` làm `mentor_id`; JWT thiếu/sai → 401, role khác → 403.
- Cách này tái sử dụng chính xác local pattern của API #58–#60.

### 1.2. Nhận trace ID

- Middleware xác thực `X-Trace-Id` hoặc tạo trace; view truyền trace qua success/error envelope.
- Response trả cùng trace trong `traceId` và `X-Trace-Id`.

<a id="step-2"></a>

## 2. Kiểm tra quyền Mentor

- Mentor scope local là `courses.mentor_id = numeric JWT sub`.
- Request được đọc kèm `course_id`, course parent và student projection; request row được khóa bằng `FOR UPDATE`.
- Request tồn tại nhưng course thuộc Mentor khác → 403 `DESIGN_ACCESS_DENIED`; request không có → 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Đây là fallback `DERIVED` hiện đã dùng trong #58–#60; không dùng `request_id` làm bằng chứng ownership.

<a id="step-3"></a>

## 3. Đọc và kiểm tra `request_id`

| Item | Type contract | Local mapping | Rule | Status |
|---|---|---|---|---|
| `request_id` | required int64 | `support_requests.id BIGINT` | Parse signed-int64 rồi bind parameterized query | Catalog type DIRECT; physical mapping DERIVED from migration 008/#58–#60 |

- Sai format hoặc overflow → 422 `DESIGN_VALIDATION_ERROR`.
- Không thêm minimum/positive constraint; ID không tồn tại → 404.

<a id="step-4"></a>

## 4. Khóa SupportRequest và trạng thái

### 4.1. Request/parent projection

| Target | Table/fields | Điều kiện | Trạng thái |
|---|---|---|---|
| SupportRequest | `support_requests.id`, `course_id`, `student_id`, `status`, `created_at`, `resolved_at` | Match ID và khóa request row | Local checked-in source; live deployment chưa xác minh |
| Owner | `courses.id`, `courses.mentor_id` | `course.id = request.course_id`; compare owner với JWT `sub` | DERIVED local convention from #58–#60 |
| Student | `users.id`, `full_name`, `avatar_url` | `student.id = request.student_id` | Local projection convention |

- `infra/postgres/study-server/migrations/008_support_requests.sql` và `DB.sql` là local artifacts; không phải bằng chứng live schema.
- V1-PILOT UUID `support_tickets` không dùng cho API #61 vì không khớp int64 và không phải model hiện tại của #58–#60.

<a id="step-5"></a>

## 5. Resolve request

### 5.1. State transition matrix

| Current status | Action | Result | Basis/status |
|---|---|---|---|
| `OPEN` | UPDATE `status` | `RESOLVED` | AC-24 status effect DIRECT; allowed pre-state DERIVED |
| `IN_PROGRESS` | UPDATE `status` | `RESOLVED` | DERIVED: active state trong local migration |
| `WAITING_LEARNER` | UPDATE `status` | `RESOLVED` | DERIVED: active state trong local migration |
| `RESOLVED` | Không UPDATE | Success, giữ timestamp hiện tại | DERIVED idempotency |
| `CANCELLED` hoặc state khác | Không UPDATE | 422 `DESIGN_VALIDATION_ERROR` | DERIVED transition guard |

AC-24 YES branch gọi #61 và cập nhật status `RESOLVED`; NO branch không gọi #61 và giữ `OPEN`. Migration 008 liệt kê năm enum local; allowed transition chưa có approval riêng. Ma trận trên là implementation fallback dễ hiểu cho mọi trạng thái đang hoạt động.

### 5.2. Ghi status và timestamp

- UPDATE `support_requests.status = 'RESOLVED'` cho ba active states.
- Set `resolved_at = COALESCE(resolved_at, CURRENT_TIMESTAMP)` để chỉ có một thời điểm resolve.
- Nếu đã `RESOLVED`, không chạy UPDATE và giữ timestamp gốc.
- Không ghi `resolution_code`, `cancelled_at` hoặc message rows.

### 5.3. Đồng thời và transaction

- `SELECT ... FOR UPDATE` tuần tự hóa các lần resolve trên cùng request.
- View sở hữu transaction: lock → check scope/state → update → query thread → validate full response → commit.
- Bất kỳ lỗi query/update/projection/envelope/commit nào trước khi hoàn tất đều rollback và trả lỗi an toàn.

<a id="step-6"></a>

## 6. Nạp thread response

- Dùng `LIST_MENTOR_SUPPORT_REQUEST_MESSAGES` của API #59 với `request_id` và `mentor_id`; query kiểm tra owner ở lần đọc thread.
- Dùng chung `map_support_request` và `append_support_messages` từ Mentor `_shared` để dựng model #58.
- Giữ toàn bộ messages theo `created_at ASC, id ASC`; upload chỉ map khi đúng author, course, purpose và trạng thái `UPLOADED`, theo local #59 resolver.
- Status cuối response phải là `RESOLVED`; #61 không thay đổi nội dung conversation.

<a id="step-7"></a>

## 7. Giao dịch và trả kết quả

- Trả HTTP 200 `DESIGN_RESOURCE_UPDATED`, `ApiEnvelope<SupportRequest>` và `meta: {}`.
- Dựng, validate envelope trước `db.commit()`; commit một lần sau khi projection hợp lệ.
- Lỗi trước commit gọi rollback; lỗi query/commit trả 500 `DESIGN_INTERNAL_ERROR`.
- Error helper hiện serialize `data: null`; lỗi field dùng `meta.fieldErrors`.

<a id="step-8"></a>

## 8. Xử lý lỗi

- Bearer/JWT thiếu hoặc sai → 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Role sai hoặc request ngoài course owner scope → 403 `DESIGN_ACCESS_DENIED`.
- Request không tồn tại → 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Path sai signed-int64 hoặc trạng thái không được resolve → 422 `DESIGN_VALIDATION_ERROR`.
- DB/update/thread projection/envelope failure → 500 `DESIGN_INTERNAL_ERROR`; rollback, không trả nội bộ.
- Không thêm HTTP 409, 503 hoặc business code ngoài catalog.

## Mapping table

- [UPDATE `support_requests`](./07_table.md).
- API #61 không ghi SupportMessage; INSERT message/relation thuộc [API #60](../60_mentor_support_reply/05_Data_Mapping.md).
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
