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
3. [Step 2 — Đọc notification](#step-2-đọc-notification)
4. [Step 3 — Ánh xạ response](#step-3-ánh-xạ-response)
5. [Step 4 — Trả kết quả hoặc lỗi](#step-4-trả-kết-quả-hoặc-lỗi)

<a id="step-0-xác-thực-và-phân-quyền"></a>

## Step 0 — Xác thực và phân quyền

| Check | Source | Rule | Basis/status |
|---|---|---|---|
| Bearer token | Catalog #92 | Request dùng Bearer JWT | DIRECT contract |
| Role | Catalog #92 | Actor là Admin | DIRECT |
| Notification permission | AC-36 | Admin có notification-management permission | DIRECT intent; claim/policy SOURCE_REQUIRED |
| Current guard | Study auth/router | Chưa có Admin guard hoặc route #92 | CURRENT_BEHAVIOR: UNWIRED / NOT_FOUND |

- Xác thực và authorize trước khi đọc notification.
- Không dùng Student guard thay Admin policy và không nhận role/actor ID từ query.

<a id="step-1-kiểm-tra-request"></a>

## Step 1 — Kiểm tra request

### Request usage matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Header | Authenticate Bearer; authorize Admin | Role DIRECT; permission mapping SOURCE_REQUIRED |
| `status` | Optional query string | Intended filter over `Notification.status` | Enum and physical mapping SOURCE_REQUIRED |
| `channel` | Optional query string | Intended filter over `Notification.channels[]` | Channel values and source grain SOURCE_REQUIRED |
| `page` | Optional int32 | Intended list page | No direct size or response PageMeta; semantics unresolved |
| Body/path | None | None | DIRECT |

- Không tự thêm `size`, date range, recipient ID, `sort`, 422 hoặc error code khác.
- Parse/range behavior chưa có mapping trong contract; giữ câu hỏi thay vì tự gán 400/422.

<a id="step-2-đọc-notification"></a>

## Step 2 — Đọc notification

### Q1 — Complete Admin list source

`SOURCE_REQUIRED`: chưa có physical model được duyệt để đọc một Admin notification với toàn bộ field `Notification`, channel/status, recipient/campaign grain và page semantics. Vì vậy DD không ghi SQL có thể bị hiểu là executable query.

### Candidate source matrix

| Query | Type | Candidate source | Columns/items | Predicate/order | Purpose/status |
|---|---|---|---|---|---|
| Q1 | SELECT | Chưa chọn | Full Notification projection | Chưa xác định filter, join, grouping hoặc pagination | `SOURCE_REQUIRED` |
| Q1-L | SELECT candidate | Legacy `notifications` | `id,title,content,created_at`; thêm `user_id,sender_id,type,is_read` chỉ là legacy columns | Không map `type`/`is_read` sang contract; notification grain chưa rõ | Candidate schema, không phải query đã duyệt |
| Q1-P | SELECT candidate | V1-PILOT `notifications` + `notification_deliveries` | UUID notification/delivery, learner, body, read_at, channel/status | ID/grain/status khác API #92 | Discrepancy; không dùng như legacy query |
| Q1-C | DERIVED proposal | Approved future list source | Exact status match; channel membership match | Chỉ áp dụng sau khi schema/enum/response được duyệt | Proposal, không phải DIRECT |

### Pagination proposal — chỉ khi contract Page được duyệt

- Page bắt đầu từ 1, fixed size 20 và stable order `created_at DESC, id DESC` là proposal `DERIVED`, tham khảo cách page design-only ở API #43.
- Query count dùng cùng filter với item query chỉ khi response Page được duyệt và schema/grain đã chọn.
- Không áp dụng predicate `user_id = principal_id` của API #43 cho Admin API.
- Empty list trả 200 với `items: []` chỉ thuộc Page proposal; direct singleton contract chưa quy định empty behavior.

### Candidate row outcome

| Outcome | Candidate behavior | Status |
|---|---|---|
| Notification phù hợp | Trả object theo direct contract hoặc item trong Page nếu contract sửa | Direct type / Page DERIVED |
| Không có record | Chưa chốt do response singleton/list conflict; catalog không có 404 | SOURCE_REQUIRED |
| Query/database failure | Giữ error code 500 theo catalog | Code DIRECT; branch detail chưa có source |
| Dependency unavailable | Giữ error code 503 theo catalog | Trigger chưa chỉ ra; SOURCE_REQUIRED |

<a id="step-3-ánh-xạ-response"></a>

## Step 3 — Ánh xạ response

### Direct `Notification` response source matrix

| Field | Type | Candidate source | Mapping/null rule | Status |
|---|---|---|---|---|
| `data.id` | int64 | Legacy `notifications.id` BIGSERIAL | Candidate numeric ID; Admin resource grain chưa chốt | SOURCE_REQUIRED |
| `data.title` | string | Legacy/pilot `notifications.title` | Candidate theo schema được chọn | Candidate only |
| `data.content` | string | Legacy `notifications.content` | Pilot `body` không tự đổi tên thành content | Legacy candidate |
| `data.channels[]` | NotificationChannel[] | Pilot delivery `channel` | Không lấy legacy `type`; channel-level không đồng nghĩa campaign channels | SOURCE_REQUIRED |
| `data.status` | NotificationStatus | Không có Notification-level source được duyệt | Không suy từ `is_read` hay delivery status | SOURCE_REQUIRED |
| `data.read_at` | date-time? | Pilot learner notification | Không có trong legacy; Admin meaning chưa rõ | SOURCE_REQUIRED |
| `data.scheduled_at` | date-time? | Không thấy field trong schema đã rà soát | Không map `expires_at` | SOURCE_REQUIRED |
| `data.created_at` | date-time | Legacy/pilot `created_at` | Candidate; timezone and grain depend on selected model | SOURCE_REQUIRED |

### Envelope fields

| Field | Source | Rule |
|---|---|---|
| `success` | Envelope branch | true success / false error |
| `businessCode` | Catalog | Exact direct business code |
| `message` | Application | Safe text; exact message not defined |
| `meta` | ApiEnvelope | Object; members not defined. Do not place PageMeta here without contract. |
| `traceId` | Request context | Propagate according to shared convention; route not wired. |

### Mutation matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | API #92 is read-only | No INSERT/UPDATE/DELETE | `N/A — READ-ONLY API` |

<a id="step-4-trả-kết-quả-hoặc-lỗi"></a>

## Step 4 — Trả kết quả hoặc lỗi

- Direct success: HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Notification>`.
- Exact direct errors: 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 503 `DESIGN_DEPENDENCY_UNAVAILABLE`, 500 `DESIGN_INTERNAL_ERROR`.
- Catalog does not list 404 or 422 for #92; do not add them for empty list or query validation.
- Current middleware does not allowlist `/api/v1/admin/notifications`; future route integration may otherwise use fallback codes. This is not current API #92 behavior because no route exists.
- Do not return SQL, stack trace, provider details or unnecessary recipient personal data.

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
