---
title: "Data Mapping"
order: 5
dd_id: "94"
api_name: "Admin cập nhật notification"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

1. Shared ADMIN JWT guard xác thực role trước path/body parse.
2. Validate path `notification_id` và strict body `{title, content}` theo fallback DERIVED.
3. Khóa một `notifications` row theo ID; không tồn tại trả catalog 404.
4. Khóa các `notification_deliveries` row theo notification ID. Không có row hoặc có status khác QUEUED trả catalog 422.
5. UPDATE duy nhất `title` và `content`; giữ nguyên id, user_id, sender_id, type, is_read, created_at và deliveries.
6. Map response dùng channels từ delivery rows và status QUEUED; validate projection rồi commit.
7. SQL/projection/commit failure rollback và trả catalog 500. Không gọi scheduler/provider.

### Query matrix

| Query | Mục đích | Điều kiện/locking | Bindings |
|---|---|---|---|
| Q1 `LOCK_ADMIN_NOTIFICATION` | Đọc/khóa target | `notifications.id = :notification_id FOR UPDATE` | notification_id |
| Q2 `LOCK_ADMIN_NOTIFICATION_DELIVERIES` | Đọc/khóa delivery state | Filter theo notification ID, order channel, `FOR UPDATE` | notification_id |
| Q3 `UPDATE_ADMIN_NOTIFICATION` | Cập nhật text và đọc lại row | Set title/content; `RETURNING id,title,content,created_at` | notification_id, title, content |

SQL constants nằm trong `api_94_admin_notifications_update/query.py`; transaction orchestration thuộc `view.py`.

## Mutation mapping

| Input/output | Candidate relation/column | Runtime operation | Status |
|---|---|---|---|
| notification_id / data.id | notifications.id | Lock target and return same ID | DERIVED on legacy candidate; live schema unverified. |
| title | notifications.title | Replace with required request value | DERIVED; DDL candidate VARCHAR(200). |
| content | notifications.content | Replace with required request value | DERIVED; DDL candidate TEXT. |
| channels[] | notification_deliveries.channel | Read existing locked rows; never update | DERIVED projection; candidate outbox. |
| status | notification_deliveries.status | Require every row QUEUED; return QUEUED | DERIVED editability/projection; not campaign status. |
| user_id/sender_id/type/is_read | notifications | Preserve; never update | Explicitly outside fallback. |
| created_at | notifications.created_at | Preserve and check UPDATE RETURNING value | Candidate; no timestamp mutation. |
| recipients/segment/scheduled_at | No compatible relation/column | Reject as extra request fields; no mutation | SOURCE_REQUIRED for future support. |

## Transaction and concurrency

- Lock notification first, then its delivery rows; delivery row locks serialize against a worker that changes those rows.
- If no delivery rows exist or any row is SENT/FAILED, rollback and return 422 `DESIGN_VALIDATION_ERROR`.
- The UPDATE and response projection share one transaction. Build and validate the response before commit.
- On SQL, mapping, or commit failure, attempt rollback and return safe 500 `DESIGN_INTERNAL_ERROR`.
- Fake-session tests verify call order/bindings/rollback only. PostgreSQL behavior and deployed schema are not verified.

## Non-effects

- No recipient association replacement, channel mutation, schedule mutation, audit row, Operation bridge, provider dispatch, queue publish, or scheduler action is implemented.
- No migration is required by this fallback because it only targets existing candidate columns; this does not establish that the deployed database has them.

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
