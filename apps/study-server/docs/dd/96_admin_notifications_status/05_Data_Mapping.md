---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "96"
api_name: "Xem trạng thái delivery notification Admin"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Luồng hiện tại và contract boundary

1. Route chuyển raw `Authorization` và `notification_id` tới view; view gọi shared `validate_current_user_request(..., role="ADMIN")` trước path parse hoặc DB.
2. Validator chấp nhận số nguyên dương trong miền signed-int64. Path sai/overflow trả catalog 404 theo fallback `DERIVED` vì #96 không khai báo 422.
3. Một SQL query đọc legacy candidate `notifications` theo ID và aggregate delivery rows từ `notification_deliveries` trong cùng query.
4. Map `channels/status` theo cùng projection của API #92; `id/title/content/created_at` đến từ notification row. `read_at` và `scheduled_at` không có trong candidate columns nên field optional bị lược bỏ.
5. Notification không tồn tại hoặc không có delivery rows cho query result rỗng và trả 404; schema-invalid aggregate trả safe 500.
6. Success trả đúng catalog `ApiEnvelope<Notification>`; không thêm counts/per-channel results và không gọi provider.

> Current source is wired and locally HTTP-tested. Physical relation, projection, enum values, invalid-ID mapping and no-delivery 404 are `DERIVED` from APIs #92/#64 and checked-in candidate DDL; this is not owner approval or live-schema evidence.

## 0. Xác thực và quyền

| Check | Nguồn | Rule | Status |
|---|---|---|---|
| Bearer JWT | Catalog + `app/utils/auth.py` | Request phải có Bearer JWT hợp lệ. | DIRECT contract; local shared guard is source-backed. |
| Role Admin | Catalog + `validate_current_user_request` | `role="ADMIN"` | DIRECT contract; local guard runs first. |
| Notification-management permission | AC-36 precondition | Fine-grained permission key/scope is not defined in Study source. | `SOURCE_REQUIRED`; role-only ADMIN is the local fallback, not equivalent proof. |
| Check ordering | API #96 view | Auth before path parsing and query. | Local current behavior; avoids resource lookup before authorization. |

## 1. Nhận request

| Field | Type | Use | Rule/status |
|---|---|---|---|
| `notification_id` | int64! path | Chọn candidate notification. | DIRECT type; local positive signed-int64 parser and 404 malformed mapping are `DERIVED`. |
| Body | Không khai báo | Không dùng. | DIRECT — N/A. |
| Query | Không khai báo | Không dùng filter/pagination. | DIRECT — N/A. |

## 2. Đọc resource và delivery aggregate

### 2.1 Query matrix

| Query | Operation | Relation/source | Field hoặc predicate | Mục đích | Status |
|---|---|---|---|---|---|
| Q1 | SELECT + aggregate | Candidate legacy `notifications` join `notification_deliveries` | `n.id = :notification_id`; group delivery rows by notification ID | Nạp một Notification và delivery summary | `DERIVED` from local #92 pattern and migration 009; not live-schema proof. |
| Q1 fields | SELECT | `notifications` | `id`, `title`, `content`, `created_at` | Base Notification projection | `DERIVED`; legacy schema does not establish approved Admin grain. |
| Q1 channels | `ARRAY_AGG` | `notification_deliveries.channel` | Ordered by channel; candidate DDL restricts `PUSH`/`EMAIL` and unique notification/channel | `data.channels` | `DERIVED` from #92; duplicates/invalid values cause mapping 500. |
| Q1 status counts | `COUNT FILTER` | `notification_deliveries.status` | Count `QUEUED`, `SENT`, `FAILED` rows | Map to `data.status` | `DERIVED` from #92 precedence; attempt/retry grain remains unknown. |
| Q1 filter | INNER JOIN | Notification plus aggregate | Target notification ID; aggregate must contain one or more deliveries | Missing/no-delivery result becomes 404 | `DERIVED` status-resource interpretation; owner semantics remain open. |
| Q2 schema reference | Logical schema only | Catalog `NotificationDelivery` | `notification_id`, `status`, `queued`, `sent`, `failed` | Reusable catalog type | Does not establish a physical table or #96 response type. |
| Q3 pilot candidate | Separate DDL | V1-PILOT `notification_deliveries` | UUID notification ID; distinct learner/pilot grain | Candidate excluded from query | `DISCREPANCY`; do not map UUID to Admin int64. |

### 2.2 Join/filter/order

- Query uses one grouped delivery aggregate joined by candidate `notification_id`; SQL text is in `app/modules/admin/api_96_admin_notifications_status/query.py`.
- Local projection orders channel names and computes `QUEUED` if any queued row exists, else `FAILED` if any failed row exists, else `SENT` if all rows are sent. This reuses #92; catalog does not define this precedence or retry grain.
- There is no pagination, mutation, cache contract or provider call. Database snapshot behavior follows the one-query local implementation only.
- Auth runs before lookup. The catalog permits 403/404; local ADMIN guard and 404 fallback order is wired, while fine-grained permission policy remains open.

## 3. Mutation

| Operation | Target | Effect | Status |
|---|---|---|---|
| INSERT | N/A | Không tạo record. | N/A — READ-ONLY API. |
| UPDATE | N/A | Không cập nhật status hoặc delivery. | N/A — READ-ONLY API. |
| DELETE | N/A | Không xóa notification/delivery. | N/A — READ-ONLY API. |
| Provider call | N/A | GET không gửi lại Push/Email. | Không có side effect được diagram/catalog khai báo. |

## 4. Response source matrix

| Response field | Type | Candidate source | Transform/null rule | Evidence/status |
|---|---|---|---|---|
| `success` | boolean | ApiEnvelope | true khi success branch | DIRECT envelope schema. |
| `businessCode` | string | Catalog | `DESIGN_RESOURCE_RETRIEVED` | DIRECT. |
| `message` | string | Application | Safe message | Wording unspecified; SOURCE_REQUIRED. |
| `data.id` | int64 | Candidate `notifications.id` | Preserve positive int64 | Local mapping `DERIVED`; Admin grain is unapproved. |
| `data.title` | string | Candidate `notifications.title` | Preserve text | Local #92 model mapping `DERIVED`. |
| `data.content` | string | Candidate `notifications.content` | Preserve text | Local #92 model mapping `DERIVED`. |
| `data.channels[]` | NotificationChannel[] | Aggregate `notification_deliveries.channel` | Sorted names, validate allowed response tokens and no duplicate | `DERIVED` from #92/local candidate DDL. |
| `data.status` | NotificationStatus | Delivery status aggregate | `QUEUED` > `FAILED` > all-`SENT` | `DERIVED` from #92; enum/priority/attempt grain need approval. |
| `data.read_at` | date-time? | Not selected; legacy has boolean `is_read` only | Omit; do not convert boolean to timestamp | Optional schema field; source absent. |
| `data.scheduled_at` | date-time? | Not selected; no candidate column | Omit | Optional schema field; source absent. |
| `data.created_at` | date-time | Candidate `notifications.created_at` | ISO-8601 serialization | Local mapping `DERIVED`; live schema unverified. |
| `meta` | object | ApiEnvelope | No pagination keys defined | DIRECT type; contents unspecified. |
| `traceId` | uuid | Request context | Propagate request trace | Envelope convention; route absent. |

## 5. Return/error handling

- Success shape remains `ApiEnvelope<Notification>`; no delivery counts or per-channel records are appended.
- Map only catalog errors: 401, 403, 404 and 500 with exact `DESIGN_*` codes. Local `error_response` uses `data:null`.
- SQL/projection errors return safe 500 and rollback; no 503 is added. Missing notification/no-delivery and invalid path return 404 under the documented local fallback.
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

