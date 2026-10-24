---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "43"
api_name: "Lấy notification list"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

> Draft theo API catalog và AC-20. Candidate query dùng notifications; chưa có route/query runtime hoặc bảng `NotificationRecipient`. Paging/order và một số predicate là DERIVED. Các source gap được ghi trong OPEN_QUESTIONS.md.

## Request Usage Matrix

| Request field | Source | Validate / normalize | Query usage | Response usage | Gap |
|---|---|---|---|---|---|
| `Authorization` | HTTP header | Bearer/`JWT`; role `Student` | Principal filter notifications.user_id | Không trả token/user ID | API #43 chưa wire shared helper. |
| `unread_only` | Query | Optional boolean; omitted mặc định false — DERIVED | true → candidate `n.is_read = FALSE`; false/omitted → không thêm filter | Không có field `is_read` trong Notification response schema | Chưa có `read_at`/`status` mapping. |
| page | Query | Optional int32; omitted mặc định 1 — DERIVED | `LIMIT`/`OFFSET` với size 20 — DERIVED | `data.pagination.page` | page < 1/`type`-error behavior chưa có lỗi tương ứng trong catalog. |

## Query Matrix

| Query ID | Type | Source | Query item | Rule | Evidence `status` |
|---|---|---|---|---|---|
| Q1 | `SELECT` | notifications AS n | n.id | Select notification identifier. | Direct candidate |
| Q1 | `SELECT` | notifications AS n | n.title | Select notification `title`. | Direct candidate |
| Q1 | `SELECT` | notifications AS n | n.content | Select notification `content`. | Direct candidate |
| Q1 | `SELECT` | notifications AS n | n.created_at | Select creation time. | Timezone unresolved |
| Q1 | `WHERE` | notifications AS n | `n.user_id = :principal_id` | Scope to authenticated `Student`. | DERIVED |
| Q1 | `WHERE` | notifications AS n | `n.is_read = FALSE` | Add only when `unread_only` is true. | DERIVED |
| Q1 | `ORDER BY` | notifications AS n | `n.created_at DESC` | Newest first. | DERIVED |
| Q1 | `ORDER BY` | notifications AS n | `n.id DESC` | Stable tie-breaker. | DERIVED |
| Q1 | `LIMIT` | N/A | 20 | Fixed page size; no size input. | DERIVED |
| Q1 | `OFFSET` | N/A | (`effective_page` - 1) * 20 | Page `offset`. | DERIVED |
| Q2 | `SELECT` | notifications AS n | `COUNT(*)` | Count all rows matching Q1 filters. | DERIVED |
| Q2 | `WHERE` | notifications AS n | `n.user_id = :principal_id` | Same owner predicate as Q1. | DERIVED |
| Q2 | `WHERE` | notifications AS n | `n.is_read = FALSE` | Add only when `unread_only` is true. | DERIVED |


## Mutation Matrix

| Mutation ID | Operation | Target | Condition | Fields | Mapping / transaction |
|---|---|---|---|---|---|
| — | N/A — READ-ONLY API | N/A | N/A | N/A | API #43 không insert/update/delete; xem [07_table.md](./07_table.md). |

## Response Source Matrix

| Response field | Type | Candidate source | Data Mapping step | Transform / rule | Status |
|---|---|---|---|---|---|
| `data.items[].id` | int64 | notifications.id | 5.1 | Direct | DIRECT candidate |
| `data.items[].title` | string | notifications.title | 5.1 | Direct | DIRECT candidate |
| `data.items[].content` | string | notifications.content | 5.1 | Direct | DIRECT candidate |
| `data.items[].channels` | `NotificationChannel[]` | Chưa có source | 5.1 | Không suy từ `type` | SOURCE_REQUIRED |
| `data.items[].status` | `NotificationStatus` | Chưa có source | 5.1 | Không suy từ `type` hoặc `is_read` | SOURCE_REQUIRED |
| `data.items[].read_at` | date-time? | Chưa có source | 5.1 | Không tính từ boolean | SOURCE_REQUIRED |
| `data.items[].scheduled_at` | date-time? | Chưa có source | 5.1 | Không có physical column | SOURCE_REQUIRED |
| `data.items[].created_at` | date-time | notifications.created_at | 5.1 | Cần chốt timezone serialization | SOURCE_REQUIRED for timezone |
| `data.pagination.page` | int32 | page input | 5.2 | Omitted dùng 1 | DERIVED |
| `data.pagination.size` | int32 | Fixed constant | 5.2 | 20 | DERIVED |
| `data.pagination.total` | int64 | Q2 `COUNT(*)` | 5.2 | Cùng filters như Q1 | DERIVED |
| `data.pagination.total_pages` | int32 | `total` + size | 5.2 | ceil(`total`/20); 0 when `total`=0 | DERIVED |


## 0. Lấy principal

### 0.1. Get request header

- authorization: lấy từ HTTP `Authorization` header.
- trace_id: lấy từ request trace context; current middleware gắn X-Trace-Id.

### 0.2. Xác thực `Student`

- Gọi shared helper theo pattern hiện có: validate_current_user_request(authorization, trace_id=trace_id).
- Nếu helper trả 401: đi tới lỗi `DESIGN_AUTHENTICATION_REQUIRED`.
- Nếu helper trả 403: đi tới lỗi `DESIGN_ACCESS_DENIED`.
- Nếu helper trả (`user_id`, roles): đặt `principal_id` = `user_id`.
- Không nhận `user_id` từ query, path hoặc body.
- Đây là đề xuất reuse current auth helper; API #43 chưa được triển khai.

## 1. Lấy request data

- `unread_only`: lấy từ query parameter `unread_only`.
- page: lấy từ query parameter page.

## 2. Validate và chuẩn hóa query

### 2.1. Chuẩn hóa `unread_only`

- Nếu `unread_only` omitted: đặt `effective_unread_only` = FALSE — DERIVED.
- Nếu `unread_only` = true: đặt `effective_unread_only` = TRUE.
- Nếu `unread_only` = false: đặt `effective_unread_only` = FALSE.
- Invalid boolean encoding: contract không khai báo 422; không thêm error code trong DD này.

### 2.2. Chuẩn hóa page

- Nếu page omitted: đặt `effective_page` = 1 — DERIVED.
- Nếu page có giá trị int32 dương: dùng giá trị đó.
- Nếu page < 1: chưa khóa response vì catalog không khai báo 422.
- Nếu giá trị không parse được thành int32: current framework behavior chưa được kiểm chứng cho API #43.

### 2.3. Tính `offset`

- `page_size` = 20 — DERIVED, không nhận từ client.
- `offset` = (`effective_page` - 1) * `page_size`.

## 3. Xây dựng predicate notification

- Bắt buộc thêm n.user_id = `principal_id` để scope dữ liệu theo `Student` hiện tại — DERIVED từ /me và mục đích đọc recipient.
- Không thêm notification có n.user_id IS NULL; DB design nói field này có thể đại diện broadcast/segment nhưng không có recipient/read-state model theo user.
- Nếu `effective_unread_only` = TRUE, thêm `n.is_read = FALSE`.
- Nếu `effective_unread_only` = FALSE, không thêm read-state predicate.
- Không suy luận `type`, `channels`, `status` hoặc delivery channel filter từ request; API #43 không nhận các query này.

## 4. Đọc page và count

### 4.1. Query page — Q1

| Target table | Column / expression | Purpose | Remarks |
|---|---|---|---|
| notifications AS n | n.id | Notification ID | Q1 |
| notifications AS n | n.title | Title | Q1 |
| notifications AS n | n.content | Content | Q1 |
| notifications AS n | n.created_at | Creation time | Q1 |
| notifications AS n | `n.user_id = :principal_id` | Owner predicate | DERIVED; principal from step 0. |
| notifications AS n | `n.is_read = FALSE` | Optional unread predicate | Only when `effective_unread_only` = TRUE. |

**JOIN**

| Target table | Join condition | Join `type` |
|---|---|---|
| notifications AS n | N/A | BASE |

**`ORDER BY`**

- `n.created_at DESC` — DERIVED, newest first.
- `n.id DESC` — DERIVED, stable tie-breaker.

**Pagination**

- `LIMIT` = 20 — DERIVED.
- `OFFSET` = (`effective_page` - 1) * 20 — DERIVED.

### 4.2. Query count — Q2

- Chạy `COUNT(*)` trên cùng tập candidate notification.
- Dùng `n.user_id = :principal_id`.
- Chỉ khi `effective_unread_only` = TRUE, dùng thêm `n.is_read = FALSE`.
- Không dùng `LIMIT` hoặc `OFFSET`.
- Lưu kết quả vào total_notifications.

### 4.3. Check query result

- Nếu notification_rows rỗng: tiếp tục dựng `items` = []; list rỗng không phải lỗi — DERIVED.
- Nếu `effective_page` vượt trang cuối: trả page rỗng cùng total_notifications — DERIVED.
- Nếu Q1 hoặc Q2 gặp lỗi database ngoài dự kiến: đi tới lỗi 500 `DESIGN_INTERNAL_ERROR`.
- Required response mapping `channels`/`status` đang SOURCE_REQUIRED; không thể hoàn thiện projection bằng các cột hiện có nếu chưa có quyết định schema/contract.

## 5. Map response

### 5.1. Map từng notification

- `data.items[].id` = notification_rows[].id.
- `data.items[].title` = notification_rows[].title.
- `data.items[].content` = notification_rows[].content.
- `data.items[].created_at` = notification_rows[].created_at sau khi timezone serialization được xác nhận.
- `data.items[].channels` = SOURCE_REQUIRED.
- `data.items[].status` = SOURCE_REQUIRED.
- `data.items[].read_at` = SOURCE_REQUIRED nếu field được trả.
- `data.items[].scheduled_at` = SOURCE_REQUIRED nếu field được trả.
- Không map notifications.type thành `channels`.
- Không map notifications.is_read thành `status`.
- Không biến notifications.is_read thành thời điểm `read_at`.

### 5.2. Map `PageMeta`

- `data.pagination.page` = `effective_page`.
- `data.pagination.size` = 20 — DERIVED.
- `data.pagination.total` = total_notifications.
- `data.pagination.total_pages` = 0 nếu total_notifications = 0.
- Nếu total_notifications > 0, `data.pagination.total_pages` = ceil(total_notifications / 20).
- Nếu page vượt trang cuối, giữ page yêu cầu và trả `items` = [] — DERIVED.

## 6. Trả `success` response

- HTTP `status` = 200.
- `success` = true.
- `businessCode` = `DESIGN_RESOURCE_RETRIEVED`.
- data = `Page<Notification>` theo catalog.
- `meta` = {} khi không có metadata riêng.
- `traceId` theo trace convention.
- Không trả `user_id` hoặc thông tin `JWT` trong data.

## 7. Error handling

- 401 `DESIGN_AUTHENTICATION_REQUIRED`: thiếu/sai Bearer/`JWT`.
- 403 `DESIGN_ACCESS_DENIED`: token hợp lệ nhưng không có `Student` role.
- 500 `DESIGN_INTERNAL_ERROR`: lỗi database hoặc lỗi nội bộ không dự kiến.
- Không thêm 404 hoặc 422 vì API #43 không khai báo các lỗi này.
- Không trả raw SQL error, stack trace, token hoặc secret.
- Error helper response-body discrepancy được ghi tại [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

## 8. Transaction và side effect

- Transaction: N/A.
- Database mutation: N/A.
- External API/provider call: N/A.
- API #44/#45 là các mutation riêng; chỉ macro-review sau khi cả hai DD đó được tạo.
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
