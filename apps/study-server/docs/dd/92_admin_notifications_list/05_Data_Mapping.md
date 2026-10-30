---
title: "Data Mapping"
order: 5
dd_id: "92"
api_name: "Lấy notification list"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

### Mục lục

1. [Step 0 — Xác thực và phân quyền](#step-0-xác-thực-và-phân-quyền)
2. [Step 1 — Kiểm tra request](#step-1-kiểm-tra-request)
3. [Step 2 — Đọc Notification và delivery aggregate](#step-2-đọc-notification-và-delivery-aggregate)
4. [Step 3 — Ánh xạ response](#step-3-ánh-xạ-response)
5. [Step 4 — Trả kết quả hoặc lỗi](#step-4-trả-kết-quả-hoặc-lỗi)

<a id="step-0-xác-thực-và-phân-quyền"></a>

## Step 0 — Xác thực và phân quyền

| Check | Source | Rule | Basis/status |
|---|---|---|---|
| Bearer token | Catalog #92 | Request dùng Bearer JWT | DIRECT |
| Role | Catalog #92 | Actor là Admin | DIRECT |
| Notification-management permission | AC-36 | Admin cần permission chuyên biệt | DIRECT intent; key/policy SOURCE_REQUIRED |
| Runtime guard | `app/utils/auth.py` | `validate_current_user_request(..., role="ADMIN")` trước query | DERIVED fallback; không chứng minh permission riêng |

- Không nhận role, actor ID hoặc permission từ query/body.
- Nếu guard trả 401/403, dừng trước query và chuyển lỗi theo catalog.

<a id="step-1-kiểm-tra-request"></a>

## Step 1 — Kiểm tra request

### Request usage matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Header | Authenticate Bearer; authorize Admin | Role DIRECT; specialized permission SOURCE_REQUIRED |
| `status` | Optional query string | Exact predicate trên aggregate status | String DIRECT; aggregate mapping DERIVED |
| `channel` | Optional query string | Membership predicate trên channels array | String DIRECT; channel source DERIVED |
| `page` | Optional int32 | Limit/offset và `pagination.page` | Page 1..INT32_MAX, default 1 DERIVED |
| Body/path | None | None | DIRECT |

- Status/channel giữ nguyên text; không trim, lower/upper-case hoặc tự áp enum allowlist.
- Page size cố định 20 và `offset = (page - 1) * 20` là DERIVED.
- Invalid/non-positive/out-of-int32 page trả 422 `DESIGN_VALIDATION_ERROR`, ngoài error set catalog.

<a id="step-2-đọc-notification-và-delivery-aggregate"></a>

## Step 2 — Đọc Notification và delivery aggregate

### Q1 — Legacy notification page/count candidate

`DERIVED`: dùng checked-in legacy BIGINT `notifications` cùng migration-009/API #63 `notification_deliveries`. Đây là candidate local, không xác nhận live relation/migration deployment hoặc Admin campaign grain.

### Query Matrix

| Query ID | Type | Source | Query item | Rule | Evidence status |
|---|---|---|---|---|---|
| Q1-CTE | `GROUP BY` | `notification_deliveries AS d` | `notification_id`, `channel`, `status` | Aggregate distinct-by-DDL delivery rows per notification; channels order `channel ASC` | DERIVED from API #63/DDL |
| Q1-CTE | `COUNT FILTER` | `notification_deliveries AS d` | `delivery_count`, `queued_count`, `failed_count`, `sent_count` | Count each stored state; reuse API #64 precedence | DERIVED |
| Q1 | `JOIN` | `notifications AS n` + delivery summary | `n.id = d.notification_id` | Include only notifications with at least one delivery row | DERIVED; excludes rows without channel/status projection |
| Q1 | `SELECT` | `notifications AS n` | `id`, `title`, `content`, `created_at` | Do not select recipient/sender/read/type/operation IDs | Candidate fields |
| Q1 | `WHERE` | Notification result | `status` | Optional exact match to aggregate `QUEUED`/`FAILED`/`SENT` | DERIVED |
| Q1 | `WHERE` | Notification result | `channel` | Optional exact membership in aggregate channels | DERIVED |
| Q1 | `ORDER BY` | Notification result | `created_at DESC, id DESC` | Newest first with stable tie-breaker | DERIVED |
| Q1 | `LIMIT` | N/A | 20 | Fixed page size | DERIVED |
| Q1 | `OFFSET` | N/A | `(page - 1) * 20` | Page is 1-based | DERIVED |
| Q2 | `COUNT` | Same notification result | `COUNT(*)` | Exact same status/channel predicates as Q1 | DERIVED |

### Delivery aggregate status mapping

- Nếu `queued_count > 0`, status = `QUEUED`.
- Nếu không còn queued và `failed_count > 0`, status = `FAILED`.
- Nếu `sent_count = delivery_count`, status = `SENT`.
- Aggregate không thuộc các nhánh trên không tạo Notification projection hợp lệ; trả 500 an toàn.
- Thứ tự trên lấy từ API #64 Operation status; ánh xạ sang Notification.status của Admin vẫn DERIVED.

### Query result handling

| Outcome | Runtime behavior | Status |
|---|---|---|
| Count hợp lệ, rows hợp lệ | Map Page | Local source-backed |
| Không có row/page ngoài phạm vi | HTTP 200, `items: []` | DERIVED |
| Row không có delivery | Không thuộc query result | DERIVED |
| SQL connection unavailable | Rollback và 503 `DESIGN_DEPENDENCY_UNAVAILABLE` | DERIVED trigger for direct code |
| SQL/mapping/projection failure khác | Rollback và 500 `DESIGN_INTERNAL_ERROR` | 500 code DIRECT; branch mapping current source |

<a id="step-3-ánh-xạ-response"></a>

## Step 3 — Ánh xạ response

### Response Source Matrix

| Response field | Type | Candidate source | Data Mapping step | Transform / rule | Status |
|---|---|---|---|---|---|
| `data.items[].id` | int64 | `notifications.id` | 3.1 | Positive signed-int64 | Legacy candidate |
| `data.items[].title` | string | `notifications.title` | 3.1 | Direct string | Legacy candidate |
| `data.items[].content` | string | `notifications.content` | 3.1 | Direct string | Legacy candidate |
| `data.items[].channels[]` | `NotificationChannel[]` | `notification_deliveries.channel` | 3.1 | Ordered array; only `EMAIL`/`PUSH` accepted | DERIVED from #63/DDL |
| `data.items[].status` | `NotificationStatus` | Delivery counts | 3.1 | QUEUED → FAILED → SENT precedence | DERIVED from #64 |
| `data.items[].read_at` | date-time? | None | 3.1 | Omit | SOURCE_REQUIRED if required later |
| `data.items[].scheduled_at` | date-time? | None | 3.1 | Omit | SOURCE_REQUIRED if required later |
| `data.items[].created_at` | date-time | `notifications.created_at` | 3.1 | Preserve DB datetime serialization | Legacy candidate; live type unverified |
| `data.pagination.page` | int32 | validated query | 3.2 | Requested page; default 1 | DERIVED |
| `data.pagination.size` | int32 | local constant | 3.2 | 20 | DERIVED |
| `data.pagination.total` | int64 | Q2 | 3.2 | Exact Q1 predicates | DERIVED |
| `data.pagination.total_pages` | int32 | Q2 + size | 3.2 | ceil(total/20), zero when total is zero | DERIVED |

- Không map `notifications.type` thành `channels`.
- Không map `notifications.is_read` thành status hoặc `read_at`.
- Không map `notification_deliveries.status` thành `read_at` hoặc provider state.
- Không trả `user_id`, `sender_id`, `operation_id`, provider message IDs hoặc raw error.

<a id="step-4-trả-kết-quả-hoặc-lỗi"></a>

## Step 4 — Trả kết quả hoặc lỗi

- Success: HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, runtime `ApiEnvelope<Page<Notification>>`.
- Exact catalog errors: 401, 403, 503, 500 với business codes tương ứng.
- Runtime-only fallback: invalid page trả 422; status/channel enum không match chỉ tạo empty result.
- Empty result trả 200 với pagination; không có 404.
- Query và response mapping hoàn tất trước khi trả; success không commit; lỗi query/projection gọi rollback.
- Không gọi notification provider hoặc operation tracker.

## Mutation matrix

| Mutation ID | Operation | Target | Condition | Fields | Mapping / transaction |
|---|---|---|---|---|---|
| — | N/A — READ-ONLY API | N/A | N/A | Không INSERT/UPDATE/DELETE | Không commit; rollback khi lỗi |

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
