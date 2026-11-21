---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "44"
api_name: "Đánh dấu một thông báo đã đọc"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý `data`

> Proposal design-only dựa trên API catalog, AC-20 và checked-in DB design. Current source không có API #44. Diagram yêu cầu `NotificationRecipient`.`read_at`; câu `UPDATE` bên dưới là candidate dùng `notifications`.`is_read` hiện có, được đánh dấu `DERIVED` và chưa thay thế contract/diagram.

## Request Usage Matrix

| Request field | Source | Data Mapping step | Validate / normalize | SQL or branch use | Response use | Gap |
|---|---|---|---|---|---|---|
| `Authorization` | `HTTP` header | 0 | `Bearer`/`JWT`; role `Student` | Lấy principal ID làm owner predicate | Không echo token hoặc user ID | API #44 chưa gọi current helper. |
| `notification_id` | Path | 1 | Parse `int64`; invalid/out-of-range → catalog 422 | n.id=:`notification_id` | `data`.`items`[0].id từ `UPDATE` `RETURNING` | Physical recipient/`read_at` source chưa khớp. |

## Query Matrix

| Query ID | Purpose | Type | Source | Query item | Rule | Evidence `status` |
|---|---|---|---|---|---|---|
| M1 | Mark current user's notification as read | `UPDATE` | `notifications` AS n | SET `is_read`=`TRUE` | Set logical read flag using existing physical boolean. | `DERIVED`; diagram says `read_at`. |
| M1 | Same | WHERE | `notifications` AS n | n.id=:`notification_id` | Select requested notification. | Direct key/request contract |
| M1 | Same | WHERE | `notifications` AS n | n.`user_id`=:`principal_id` | Limit mutation to authenticated `Student`'s direct-recipient row. | `DERIVED`; logical recipient model absent |
| M1 | Same | `RETURNING` | `notifications` AS n | id | Return notification ID. | Direct candidate |
| M1 | Same | `RETURNING` | `notifications` AS n | `title` | Return `title`. | Direct candidate |
| M1 | Same | `RETURNING` | `notifications` AS n | `content` | Return `content`. | Direct candidate |
| M1 | Same | `RETURNING` | `notifications` AS n | `created_at` | Return creation time. | Candidate; timezone unresolved |

## Mutation Matrix

| Mutation ID | Operation | Target | Changed field | Value source | Transaction / failure |
|---|---|---|---|---|---|
| M1 | Mark read | `notifications` | `is_read` | Fixed `TRUE` | One atomic `UPDATE` in caller-owned transaction; commit on matched row; rollback on DB/commit error. |

**Điều kiện M1** — từng predicate được ghi riêng:

| No | Column | Condition | Source | Rule |
|---:|---|---|---|---|
| 1 | id | id=:`notification_id` | Required path | Chỉ update đúng notification ID. |
| 2 | `user_id` | `user_id`=:`principal_id` | `Student` `JWT` | Không update notification của user khác; row NULL không match. |

## Response Source Matrix

| Response field | Type | Candidate source | Data Mapping step | Transform / rule | Status |
|---|---|---|---|---|---|
| `success` | boolean | Fixed | 5 | true on `success` | Direct envelope |
| `businessCode` | string | API catalog | 5 | `DESIGN_RESOURCE_UPDATED` | Direct |
| `message` | string | Safe `message` | 5 | Literal not specified | Wording open |
| `data`.`items`[] | `Notification`[] | M1 `UPDATE` `RETURNING` | 4 | Exactly one updated row | `DERIVED` singleton |
| `data`.`items`[].id | `int64` | `notifications`.id | 4 | Direct | DIRECT candidate |
| `data`.`items`[].`title` | string | `notifications`.`title` | 4 | Direct | DIRECT candidate |
| `data`.`items`[].`content` | string | `notifications`.`content` | 4 | Direct | DIRECT candidate |
| `data`.`items`[].`channels` | `NotificationChannel`[] | None in physical schema | 4 | Do not map from type | `SOURCE_REQUIRED` |
| `data`.`items`[].`status` | `NotificationStatus` | None in physical schema | 4 | Do not infer from `is_read` | `SOURCE_REQUIRED` |
| `data`.`items`[].`read_at` | date-time? | None in physical schema | 4 | Do not derive from boolean | `SOURCE_REQUIRED` |
| `data`.`items`[].`scheduled_at` | date-time? | None in physical schema | 4 | No column | `SOURCE_REQUIRED` |
| `data`.`items`[].`created_at` | date-time | `notifications`.`created_at` | 4 | ISO-8601 requires timezone rule | `SOURCE_REQUIRED` for timezone |
| `data`.`pagination`.`page` | int32 | Fixed value | 4 | 1 | `DERIVED` |
| `data`.`pagination`.`size` | int32 | Fixed value | 4 | 1 | `DERIVED` |
| `data`.`pagination`.`total` | `int64` | Updated row count | 4 | 1 on `success` | `DERIVED` |
| `data`.`pagination`.`total_pages` | int32 | Fixed value | 4 | 1 on `success` | `DERIVED` |
| `meta` | object | Fixed empty object | 5 | {} | Envelope |
| `traceId` | uuid | Request trace context | 5 | Current trace convention | Shared convention |

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Lấy `Authorization` header từ request.
- Lấy trace ID từ current request context.
- Gọi validate_current_user_request(authorization, trace_id=trace_id).
- Nếu helper trả 401, dừng xử lý và trả `DESIGN_AUTHENTICATION_REQUIRED`.
- Nếu helper trả 403, dừng xử lý và trả `DESIGN_ACCESS_DENIED`.
- Nếu helper thành công, dùng `user_id` từ `JWT` làm `principal_id`.
- Không nhận `user_id` từ request.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| `Bearer` `JWT` | `sub`, `roles` | Numeric user ID và role STUDENT | Current Study helper validates token/principal; #44 chưa wired. |
| `notifications` AS n | `user_id` | n.`user_id`=:`principal_id` | Candidate ownership gate; NULL broadcast row không match. |

### 0.3. Check kết quả

- Role không phải `Student`: trả 403.
- Không query DB trước khi có principal đã xác thực.
- Owner check diễn ra trong M1; không dùng SELECT trước mutation để tránh race.

## 1. Validate `data` input

- `notification_id` là path parameter required `int64` theo catalog.
- Không có request body hoặc query parameter.
- Nếu path không parse thành `int64` hoặc vượt miền `int64`, trả 422 `DESIGN_VALIDATION_ERROR`.
- Không tự thêm giới hạn positivity; ID `int64` hợp lệ nhưng không match row trả 404.
- Error response tham chiếu [06_Error.md](./06_Error.md#error-cases).

## 2. Chuẩn bị mutation

- `principal_id` chỉ lấy từ bước 0.
- Target row được xác định đồng thời bằng ID và principal.
- Không thêm điều kiện `is_read`=`FALSE`; request lặp lại vẫn có thể trả resource thành công sau khi state đã là `TRUE`.
- Gán state `TRUE` lặp lại không đổi kết quả trạng thái; mutation candidate idempotent theo state.
- Không có cột updated_at hoặc audit column trong `notifications` DDL để cập nhật thêm.

## 3. Update read state

### 3.1. Query M1

~~~sql
UPDATE notifications AS n
SET is_read = TRUE
WHERE n.id = :notification_id
  AND n.user_id = :principal_id
RETURNING n.id, n.title, n.content, n.created_at;
~~~

- `is_read`=`TRUE` là candidate physical fallback; AC-20 diagram yêu cầu `NotificationRecipient`.`read_at`. Không ghi timestamp giả và không tạo schema.
- Mỗi predicate của M1 được liệt kê trong Query Matrix và 07_notifications_mark_read.md.
- `RETURNING` lấy cột có physical source để dựng candidate response; required `channels`/`status` chưa có mapping.
- Dùng một statement atomic; bind values bằng parameter, không nối chuỗi SQL.
- Transaction boundary đề xuất thuộc caller/use-case theo Study DB convention.

### 3.2. Check mutation result

- Nếu `RETURNING` trả đúng một row: giữ row trong transaction, map response thành công, rồi commit trước khi trả response.
- Nếu không có row: trả 404 `DESIGN_RESOURCE_NOT_FOUND`; cùng xử lý cho ID không tồn tại, row thuộc `Student` khác hoặc broadcast row `user_id` IS NULL.
- Nếu `UPDATE`, `RETURNING`, response mapping hoặc commit lỗi: rollback transaction và trả 500 `DESIGN_INTERNAL_ERROR`.

## 4. Build updated-resource `Page`

- Map row `RETURNING` thành một `Notification` candidate.
- `data`.`items` có đúng một item.
- `pagination`.`page`=1, `pagination`.`size`=1, `pagination`.`total`=1, `pagination`.`total_pages`=1 — `DERIVED` theo API #42 singleton `Page` precedent.
- Không trả tổng unread count vì response schema không khai báo field đó.
- `channels`/`status`/`read_at` remain `SOURCE_REQUIRED`; không thể dựng response đầy đủ từ DDL hiện có.
- API #43 refresh sau mutation cần loại item khỏi unread filter qua `is_read`=`TRUE`, nhưng cách trả read state trong `Notification` vẫn cần quyết định.

## 5. Return `success` envelope

- `HTTP` 200.
- `success`=true.
- `businessCode`=`DESIGN_RESOURCE_UPDATED`.
- `data` theo candidate `Page` ở bước 4.
- `meta`={} khi không có metadata riêng.
- `traceId` lấy theo trace convention.
- Không trả token, `principal_id` hoặc raw SQL.

## 6. Error handling

- 401: thiếu/sai `Bearer`/`JWT`.
- 403: token hợp lệ nhưng không có `Student` role.
- 404: không có notification khớp cả ID và principal.
- 422: path `notification_id` không parse được thành `int64`.
- 500: DB/update/commit/mapping failure.
- Dùng error code đúng catalog; mỗi case chi tiết tại [06_Error.md](./06_Error.md).
- Error guideline `data`:null và current helper `data`:{} là discrepancy ghi tại [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

## 7. Transaction và side effect

- Một câu `UPDATE` trong caller-owned transaction.
- Commit sau khi có row và response mapping thành công, ngay trước khi trả response.
- Rollback nếu mutation/query/mapping/commit fail.
- Nếu không có row, trả 404; không tác dụng lên notification khác.
- Không gọi email/push/provider và không phát sinh mutation khác.
- `Idempotency-Key` không nằm trong contract; state assignment là idempotent, applicability của guideline cần xác nhận.

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
