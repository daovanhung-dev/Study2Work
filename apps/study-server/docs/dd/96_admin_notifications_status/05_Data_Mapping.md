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

## Luồng xử lý thiết kế

1. Xác thực Bearer JWT và yêu cầu Admin cùng notification-management permission theo AC-36.
2. Đọc `notification_id:int64` từ path.
3. Tìm logical Admin Notification theo ID — physical relation/query chưa có nguồn được duyệt.
4. Đọc delivery aggregate theo diagram — relation, grain, status, count rules và consistency chưa được xác định.
5. Ánh xạ đúng các field hiện có của `Notification`; không thêm `NotificationDelivery` fields.
6. Trả 200 `DESIGN_RESOURCE_RETRIEVED` hoặc lỗi thuộc đúng catalog 401/403/404/500.

> Đây là luồng thiết kế; API #96 hiện `UNWIRED / NOT_FOUND`, không phải current runtime trace.

## 0. Xác thực và quyền

| Check | Nguồn | Rule | Status |
|---|---|---|---|
| Bearer JWT | Catalog | Request phải có Bearer JWT hợp lệ. | DIRECT contract; Study Admin guard chưa có. |
| Role Admin | Catalog | Actor là Admin. | DIRECT contract; claim mapping chưa có. |
| Notification-management permission | AC-36 precondition | Chỉ truy cập khi có permission phù hợp. | DIRECT requirement; permission key/scope/policy `SOURCE_REQUIRED`. |
| Thứ tự check | Chưa có source | Không đọc record/aggregate trước authorization. | Security proposal `DERIVED`; 403/404 precedence cần owner xác nhận. |

## 1. Nhận request

| Field | Type | Use | Rule/status |
|---|---|---|---|
| `notification_id` | int64! path | Khóa logic để chọn Notification. | DIRECT type; physical key và parse-error mapping chưa có. |
| Body | Không khai báo | Không dùng. | DIRECT — N/A. |
| Query | Không khai báo | Không dùng filter/pagination. | DIRECT — N/A. |

## 2. Đọc resource và delivery aggregate

### 2.1 Query matrix

| Query | Operation | Relation/source | Field hoặc predicate | Mục đích | Status |
|---|---|---|---|---|---|
| Q1 | SELECT | Chưa có Admin Notification relation được duyệt | Candidate key `id = :notification_id` | Nạp Notification | `SOURCE_REQUIRED`; không phát hành SQL giả định. |
| Q1a | SELECT candidate only | Legacy `notifications` | `id` | BIGINT key candidate | `DERIVED`; legacy row không xác nhận Admin resource grain. |
| Q1b | SELECT candidate only | Legacy `notifications` | `title` | Candidate `data.title` | `DERIVED`; Admin projection chưa được duyệt. |
| Q1c | SELECT candidate only | Legacy `notifications` | `content` | Candidate `data.content` | `DERIVED`; Admin projection chưa được duyệt. |
| Q1d | SELECT candidate only | Legacy `notifications` | `created_at` | Candidate `data.created_at` | `DERIVED`; row ownership/grain chưa được xác nhận. |
| Q2 | SELECT / aggregate | Chưa có Admin delivery relation được duyệt | Relation, join key, group grain, filter status và count expressions chưa xác định | Bước diagram “Đọc delivery aggregate” | `SOURCE_REQUIRED`. |
| Q2 schema reference | Logical schema only | Catalog `NotificationDelivery` | `notification_id`, `status`, `queued`, `sent`, `failed` | Phác thảo aggregate contract tồn tại trong catalog | Không đồng nghĩa với physical table hay response của #96. |
| Q2 pilot candidate | DDL riêng | V1-PILOT `notification_deliveries` | UUID notification ID; delivery `channel`/`status` | Tham khảo schema khác | `DISCREPANCY`; không map sang Admin int64. |
| Q3 | Permission check | Chưa có Admin policy/relation | Principal-to-scope predicate chưa được xác định | Enforce AC-36 permission | `SOURCE_REQUIRED`; không tự dùng `sender_id`. |

### 2.2 Join/filter/order

- Join giữa Notification và deliveries chưa có physical source hoặc cardinality được duyệt.
- Catalog `NotificationDelivery` không có channel field; không thể suy per-channel counts từ schema này.
- Không có `ORDER BY`, pagination, snapshot isolation hoặc cache contract cho #96.
- Nếu ID không tồn tại, catalog cho phép 404; precedence so với permission check chưa xác định.

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
| `data.id` | int64 | No approved Admin relation; legacy `notifications.id` candidate | Preserve integer | SOURCE_REQUIRED / legacy candidate only. |
| `data.title` | string | Legacy `notifications.title` candidate | Preserve text | SOURCE_REQUIRED / legacy candidate only. |
| `data.content` | string | Legacy `notifications.content` candidate | Preserve text | SOURCE_REQUIRED / legacy candidate only. |
| `data.channels[]` | NotificationChannel[] | No approved Admin source; legacy `type` is not equivalent | Preserve exact tokens only after enum decision | SOURCE_REQUIRED. |
| `data.status` | NotificationStatus | No approved Admin lifecycle/aggregate projection | Do not infer from is_read or OperationStatus | SOURCE_REQUIRED; aggregate-to-status proposal is DERIVED only. |
| `data.read_at` | date-time? | No approved Admin source; legacy has boolean `is_read` | No timestamp can be reconstructed from boolean | SOURCE_REQUIRED. |
| `data.scheduled_at` | date-time? | No approved Admin source | Do not map pilot `expires_at` | SOURCE_REQUIRED. |
| `data.created_at` | date-time | Legacy `notifications.created_at` candidate | ISO-8601 serialization | SOURCE_REQUIRED / legacy candidate only. |
| `meta` | object | ApiEnvelope | No pagination keys defined | DIRECT type; contents unspecified. |
| `traceId` | uuid | Request context | Propagate request trace | Envelope convention; route absent. |

## 5. Return/error handling

- Success shape remains `ApiEnvelope<Notification>`; no delivery counts or per-channel records are appended.
- Map only catalog errors: 401, 403, 404 and 500 with exact `DESIGN_*` codes.
- API Guidelines error `data:null` conflicts with current helper default `{}` when omitted; #96 runtime is absent, so record this as conditional integration discrepancy.
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

