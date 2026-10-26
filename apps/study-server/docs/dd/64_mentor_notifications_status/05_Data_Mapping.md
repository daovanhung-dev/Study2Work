---
title: "Data Mapping"
order: 5
dd_id: "64"
api_name: "Theo dõi trạng thái gửi"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---


# Data Mapping

## Luồng xử lý

1. Xác thực Bearer JWT và role MENTOR trước path/database work.
2. Parse raw `notification_id` thành signed int64; parse/range failure trả catalog 404.
3. Đọc `notifications` và aggregate delivery outbox theo notification ID.
4. Không có notification hoặc không có `operation_id`/delivery rows → 404; sender khác JWT `sub` → 403.
5. Validate projection, tổng số delivery và UUID/timestamps; inconsistent projection → 500.
6. Dựng Operation từ rows API #63 tạo và trả HTTP 200 `DESIGN_RESOURCE_RETRIEVED`.
7. Không commit, update, gọi provider hoặc sửa read/delivery state.

### Mục lục

- [0. Auth](#step-0-auth)
- [1. Parse request](#step-1-request)
- [2. Load notification và scope](#step-2-access)
- [3. Aggregate delivery state](#step-3-read-delivery)
- [4. Map Operation response](#step-4-map-response)
- [5. Trả response/lỗi](#step-5-response-errors)

<a id="step-0-auth"></a>

## 0. Auth

- Gọi `validate_current_user_request(..., role="MENTOR")` trước mọi DB query.
- Missing/invalid Bearer/JWT → 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Valid token không có role MENTOR → 403 `DESIGN_ACCESS_DENIED`.
- Numeric JWT `sub` là authenticated sender identity; không nhận owner từ request.

<a id="step-1-request"></a>

## 1. Parse request

| Input | Source | Rule | Error/status |
|---|---|---|---|
| `notification_id` | Raw path text | Parse signed int64 using the current API #48 signed-path pattern. | Malformed/overflow → 404 `DESIGN_RESOURCE_NOT_FOUND` (DERIVED; no 400/422 in catalog). |
| Body/query | None | No request body or query fields. | N/A. |

No positive-only validation is added. Zero, negative and valid nonmatching IDs naturally return 404 from the BIGINT resource lookup.

<a id="step-2-access"></a>

## 2. Load notification và scope

### Q1 — `FIND_NOTIFICATION_STATUS`

- Read one `notifications` row by `id = :notification_id`.
- LEFT JOIN `notification_deliveries` by `notification_id` so the query can distinguish the notification from its delivery state.
- Project `id`, `operation_id`, `sender_id`, `created_at`, delivery row count, status counts, and latest `updated_at`.
- Group only by the notification primary key and its operation/sender/time fields; one result row represents one notification ID.
- Do not filter by `sender_id` in SQL so the handler can return the catalog's 403 for another Mentor after it knows the resource exists.
- If there is no notification row, return 404.
- If `sender_id` differs from authenticated Mentor `sub`, return 403 without returning Operation fields.
- If `operation_id` is NULL or there are zero delivery rows, return 404 because no API #63 dispatch status resource exists.

The local `sender_id` scope is derived from API #63's insert binding. The query/result and authorization behavior do not prove a live schema or approved global policy.

<a id="step-3-read-delivery"></a>

## 3. Aggregate delivery state

| Aggregate | Meaning | Validation |
|---|---|---|
| `delivery_count` | Number of channel outbox rows for this notification. | Must be a positive integer. |
| `queued_count` | Rows with `status='QUEUED'`. | Non-negative and no greater than `delivery_count`. |
| `sent_count` | Rows with `status='SENT'`. | Non-negative and no greater than `delivery_count`. |
| `failed_count` | Rows with `status='FAILED'`. | Non-negative and no greater than `delivery_count`. |
| Status count sum | `queued_count + sent_count + failed_count`. | Must equal `delivery_count`; otherwise the projection is invalid. |
| `updated_at` | Maximum channel delivery update timestamp. | Must be a datetime when delivery rows exist. |

- Any queued channel → Operation status `QUEUED`.
- Otherwise, any failed channel → Operation status `FAILED`; mixed sent/failed is summarized as FAILED because the direct Operation schema has no partial status/count fields.
- Otherwise, all channels sent → Operation status `SENT`.
- The statuses reuse the local API #63 outbox constraint. OperationStatus enum membership is not catalog-defined and remains DERIVED.
- Do not use `notifications.is_read`; read receipt is not delivery state.
- Do not query Push/Email providers or infer delivery from API #63 HTTP 202.

<a id="step-4-map-response"></a>

## 4. Map Operation response

| Response field | Physical/local source | Mapping | Status |
|---|---|---|---|
| `data.id` | `notifications.operation_id` | Preserve UUID shared by API #63 recipient rows. | DERIVED local Operation persistence. |
| `data.kind` | API #63 accepted response | `NOTIFICATION_DISPATCH`. | DERIVED value reused from current producer. |
| `data.status` | Delivery status aggregate | `QUEUED`, `FAILED`, or `SENT` by precedence above. | DERIVED; channel counts/partial-success result are not returned. |
| `data.owner_id` | `notifications.sender_id` | Numeric Mentor owner already checked against JWT `sub`. | DERIVED local ownership mapping. |
| `data.submitted_at` | `notifications.created_at` | Preserve timestamp. | Local DB timestamp. |
| `data.updated_at` | `MAX(notification_deliveries.updated_at)` | Latest persisted channel status update. | DERIVED projection. |
| `data.completed_at` | No source | Omit optional field. | Lifecycle semantics unresolved. |
| `data.result` | Optional Payment schema | Omit; no payment or notification result object is defined. | No synthetic Payment. |
| `meta` | Envelope | `{}`. | No additional fields. |

Validate the complete Operation/envelope before returning; projection/model failure maps to 500 `DESIGN_INTERNAL_ERROR`.

<a id="step-5-response-errors"></a>

## 5. Response and errors

- Success: HTTP 200, `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Operation>`.
- Missing/invalid notification ID, absent Operation ID or absent delivery status rows → 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Another Mentor's notification → 403 `DESIGN_ACCESS_DENIED`.
- Database/query/projection error → safe 500 `DESIGN_INTERNAL_ERROR`; failed read transaction is rolled back.
- All error envelopes use shared `error_response(...)`, `data:null` and trace ID.
- Successful GET is read-only and issues no commit or mutation.

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
