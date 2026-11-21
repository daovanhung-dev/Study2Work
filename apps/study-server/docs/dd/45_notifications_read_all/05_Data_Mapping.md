---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "05 Data Mapping"
format: markdown
dd_id: "45"
api_name: "Đánh dấu tất cả đã đọc"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

> Draft theo API catalog và nhánh ALL AC-20. Candidate update dùng legacy Study `notifications.is_read` với principal từ Student JWT. AC-20 `NotificationRecipient.read_at` và V1-PILOT UUID schema vẫn là discrepancy; không có runtime API #45.

## Request Usage Matrix

| Request item | Source | Data Mapping step | Validate / normalize | SQL / branch use | Response use | Gap |
|---|---|---|---|---|---|---|
| `Authorization` | HTTP header | 0 | Bearer/JWT; role Student | `principal_id` cho predicate recipient | Không echo token/principal | Current helper returns numeric user ID; pilot DDL uses UUID learner. |
| Empty JSON object | Catalog `body{}` | 1 | Proposal: JSON object with no fields | Không bind parameter vào SQL | Không có field response langsung | Body requiredness/unknown fields and 422 trigger need confirmation. |

## Query Matrix

| Query ID | Purpose | Type | Source | Query item | Rule | Evidence status |
|---|---|---|---|---|---|---|
| M1 | Mark all current Student unread notifications | `UPDATE SET` | `notifications AS n` | `n.is_read = TRUE` | State assignment for each matched unread row. | DERIVED; diagram uses `NotificationRecipient.read_at`. |
| M1 | Same | `WHERE` | `notifications AS n` | `n.user_id = :principal_id` | Restrict to direct-recipient rows for authenticated Student. | DERIVED; recipient model absent in legacy DDL. |
| M1 | Same | `WHERE` | `notifications AS n` | `n.is_read = FALSE` | Update only rows currently unread. | DERIVED from “bulk update unread notifications”. |
| M1 | Same | `RETURNING` | `notifications AS n` | `n.id` | Candidate Notification ID. | Direct legacy column; UUID pilot conflict. |
| M1 | Same | `RETURNING` | `notifications AS n` | `n.title` | Candidate Notification title. | Direct legacy column. |
| M1 | Same | `RETURNING` | `notifications AS n` | `n.content` | Candidate Notification content. | Direct legacy column. |
| M1 | Same | `RETURNING` | `notifications AS n` | `n.created_at` | Candidate Notification creation time. | Direct legacy column; timezone unresolved. |

## Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Changed field | Value source | Transaction / failure |
|---|---|---|---|---|---|---|
| M1 | Mark unread as read | `notifications` legacy candidate | `user_id=:principal_id` AND `is_read=FALSE`; predicates listed separately in Query Matrix | `is_read` | Fixed `TRUE` | One caller-owned atomic statement; empty `RETURNING` means successful no-op; DB/mapping/commit error rolls back. |

No change is proposed for `updated_at`, `read_at`, delivery rows or audit fields because the legacy DDL exposes no agreed mapping for them.

## Response Source Matrix

| Response field | Type | Candidate source | Data Mapping step | Transform / rule | Status |
|---|---|---|---|---|---|
| `success` | boolean | Fixed envelope value | 4 | `true` | Direct convention |
| `businessCode` | string | API catalog | 4 | `DESIGN_RESOURCE_UPDATED` | Direct |
| `message` | string | Safe literal | 4 | Wording not fixed by catalog | Open wording |
| `data.items[].id` | int64 | legacy `notifications.id` | 3 | Direct | Candidate; UUID pilot conflict |
| `data.items[].title` | string | legacy `notifications.title` | 3 | Direct | Candidate |
| `data.items[].content` | string | legacy `notifications.content` | 3 | Direct | Candidate |
| `data.items[].channels` | `NotificationChannel[]` | None approved | 3 | Do not map from `type` | SOURCE_REQUIRED |
| `data.items[].status` | `NotificationStatus` | None approved | 3 | Do not infer from `is_read` or delivery status | SOURCE_REQUIRED |
| `data.items[].read_at` | date-time? | AC-20 recipient concept / V1-PILOT only | 3 | Do not synthesize from boolean | DISCREPANCY / SOURCE_REQUIRED |
| `data.items[].scheduled_at` | date-time? | None in examined DDL | 3 | No mapping | SOURCE_REQUIRED |
| `data.items[].created_at` | date-time | legacy `notifications.created_at` | 3 | ISO-8601 needs timezone | SOURCE_REQUIRED for timezone |
| `data.pagination.page` | int32 | Derived | 3 | Fixed 1 | DERIVED |
| `data.pagination.size` | int32 | M1 returned rows | 3 | `updated_count`; zero when empty | DERIVED |
| `data.pagination.total` | int64 | M1 returned rows | 3 | `updated_count` | DERIVED |
| `data.pagination.total_pages` | int32 | M1 returned rows | 3 | 0 if empty; otherwise 1 | DERIVED; unbounded response |
| `meta` | object | Fixed envelope value | 4 | `{}` | Direct convention |
| `traceId` | uuid | Request trace context | 4 | Current trace convention | Direct convention |

## 0. Lấy principal

### 0.1. Get request header

- `authorization`: lấy từ HTTP `Authorization` header.
- `trace_id`: lấy từ request trace context.

### 0.2. Xác thực Student

- Gọi helper theo pattern hiện tại: `validate_current_user_request(authorization, trace_id=trace_id)`.
- Nếu helper trả 401: dừng xử lý và trả `DESIGN_AUTHENTICATION_REQUIRED`.
- Nếu helper trả 403: dừng xử lý và trả `DESIGN_ACCESS_DENIED`.
- Nếu helper trả (`user_id`, roles): đặt `principal_id = user_id`.
- Không nhận user ID từ request body hoặc query.
- API #45 hiện chưa gọi helper này; đây là đề xuất reuse.

## 1. Validate body

- Catalog ghi `body{}` và không định nghĩa property.
- Đề xuất chỉ nhận JSON object rỗng `{}`; đây là `DERIVED`.
- Nếu JSON sai cú pháp, body không phải object hoặc object có property: đề xuất 422 `DESIGN_VALIDATION_ERROR` theo code có sẵn trong catalog.
- Requiredness của body và cách xử lý request không có body chưa được contract xác nhận.
- Không tạo validation cho `user_id`, `read_at`, `is_read`, page hoặc size vì request không khai báo các field này.

## 2. Bulk update

### 2.1. Candidate query M1

~~~sql
UPDATE notifications AS n
SET is_read = TRUE
WHERE n.user_id = :principal_id
  AND n.is_read = FALSE
RETURNING n.id, n.title, n.content, n.created_at;
~~~

- Mỗi predicate được liệt kê riêng trong Query Matrix.
- Dùng bound parameters; không nối chuỗi SQL.
- Chỉ direct-recipient unread rows được cập nhật.
- Row có `user_id IS NULL` không được cập nhật vì chưa có read state theo từng Student.
- Row có `is_read IS NULL` cũng không match `is_read = FALSE`; xử lý null legacy rows cần xác nhận.
- Không lọc theo `expires_at`, vì cột chỉ tồn tại trong alternative V1-PILOT schema và không có policy thống nhất.

### 2.2. Check kết quả

- Với mỗi row trong `RETURNING`: thêm candidate Notification vào `updated_rows`.
- Nếu `updated_rows` rỗng: tiếp tục trả HTTP 200 no-op; không trả 404 hoặc 409.
- Nếu SQL/DB operation lỗi: rollback transaction và trả 500 `DESIGN_INTERNAL_ERROR`.

## 3. Map response Page

- `data.items` = toàn bộ `updated_rows` theo thứ tự `RETURNING`; ordering của `UPDATE RETURNING` chưa được DB guarantee và không ảnh hưởng state.
- `updated_count = length(updated_rows)`.
- `data.pagination.page = 1`.
- `data.pagination.size = updated_count` — `DERIVED` để mô tả một page chứa toàn bộ rows vừa đổi.
- `data.pagination.total = updated_count`.
- `data.pagination.total_pages = 0` nếu `updated_count=0`; ngược lại bằng 1.
- Không có giới hạn response size trong catalog; full changed-row Page là proposal cần xác nhận.
- `channels`, `status`, `read_at`, `scheduled_at` remain `SOURCE_REQUIRED`; không dựng response đầy đủ từ legacy DDL.

## 4. Trả success response

- HTTP `status` = 200.
- `success` = true.
- `businessCode` = `DESIGN_RESOURCE_UPDATED`.
- `data` = `Page<Notification>` theo candidate mapping ở bước 3.
- `meta` = `{}` khi không có endpoint-specific metadata.
- `traceId` theo trace convention.
- Không trả principal ID hoặc token.

## 5. Error handling

- 401 `DESIGN_AUTHENTICATION_REQUIRED`: thiếu/sai Bearer/JWT.
- 403 `DESIGN_ACCESS_DENIED`: token hợp lệ nhưng không có role Student.
- 422 `DESIGN_VALIDATION_ERROR`: body validation theo empty-object proposal; trigger cần xác nhận.
- 500 `DESIGN_INTERNAL_ERROR`: DB/update/response mapping/commit failure.
- Không thêm 404/409 vì API #45 không nhắm một resource và update lặp lại là no-op idempotent.
- Không trả raw SQL, token, stack trace hoặc secret.
- Error body guideline `data:null` khác current helper fallback `data:{}`; xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

## 6. Transaction và side effect

- Một bulk `UPDATE` trong caller-owned transaction.
- Map `RETURNING` rows trước khi commit; commit ngay trước khi trả response.
- Rollback khi query, mapping hoặc commit thất bại.
- Không gọi delivery provider; không cập nhật `notification_deliveries` trong legacy-schema candidate.
- Assignment `is_read=TRUE` là state-idempotent; không thêm `Idempotency-Key` ngoài catalog.
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
