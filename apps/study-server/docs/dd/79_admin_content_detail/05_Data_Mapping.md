---
title: "Data Mapping"
order: 5
dd_id: "79"
api_name: "Lấy chi tiết content và metadata review"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
Admin Bearer principal -> shared ADMIN guard -> parse raw content_id:int64 -> SELECT active contents row by bound id -> map exact reusable Content fields -> 200 DESIGN_RESOURCE_RETRIEVED; invalid/missing/deleted -> catalog 404; query/projection failure -> safe 500
~~~

## Mục lục

- [0. Check quyền](#step-0-check-quyen)
- [1. Validate data input](#step-1-validate-data-input)
- [2. Get thông tin](#step-2-get-thong-tin)
- [3. Map response](#step-3-map-response)
- [4. Trả response hoặc lỗi](#step-4-tra-response-hoac-loi)
- [Request Usage Matrix](#request-usage-matrix)
- [Query Matrix](#query-matrix)
- [Mutation Matrix](#mutation-matrix)
- [Response Source Matrix](#response-source-matrix)

<a id="step-0-check-quyen"></a>

## 0. Check quyền

### 0.1. Xác thực Admin

- Đọc Authorization Bearer JWT theo catalog.
- Runtime dùng `validate_current_user_request(..., role="ADMIN")` trước parse path và trước mọi DB access.
- Shared guard xác minh principal/role theo auth helper hiện tại; không có policy moderation riêng trong API #79.

### 0.2. Thứ tự truy cập

- Không chạy query trước khi authentication và authorization thành công.
- Không tiết lộ Content có tồn tại hay không khi authorization thất bại.
- Không tự thêm permission table, claim name hoặc tenant scope.

### 0.3. Kết quả authorization

- Thiếu/sai Bearer hoặc token không hợp lệ: 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Principal hợp lệ nhưng thiếu role Admin: 403 `DESIGN_ACCESS_DENIED`.

<a id="step-1-validate-data-input"></a>

## 1. Validate data input

### 1.1. content_id

- Nhận path `content_id` bắt buộc kiểu signed int64 theo catalog.
- Route truyền raw path value để guard chạy trước parser.
- Không thêm min/max nghiệp vụ, đổi ID sang UUID, hoặc nhận version_id/body/query.
- Malformed hoặc ngoài signed-int64 range trả 404 theo API #69 precedent và catalog error set; đây là fallback DERIVED.

<a id="step-2-get-thong-tin"></a>

## 2. Get thông tin

### 2.1. Q1 — current Content row

Runtime đọc đúng một active row từ checked-in legacy candidate `contents`, bind `content_id` vào `id`, và loại soft-deleted row bằng `deleted_at IS NULL`. APIs #49–#53 hiện cũng dùng relation này. DDL/migrations là local source evidence, không xác nhận live schema/deployment.

| Response field | Physical source | Mapping/rule |
|---|---|---|
| id | `contents.id` | Trả stored BIGINT identifier. |
| course_id | `contents.course_id` | Trả stored course ID; không join để suy ra author. |
| content_type | `contents.content_type` | Trả stored string; không thêm enum allowlist. |
| title | `contents.title` | Trả stored text. |
| payload | `contents.payload` | Phải là JSON object theo reusable Content schema; projection sai trả safe 500. |
| status | `contents.status` | Trả current stored status; không lọc `PENDING_REVIEW` ở detail. |
| parent_id | `contents.parent_id` | Nullable; serializes null when absent. |
| order | `contents.content_order` | Map physical column sang response field `order`. |

Không có status predicate ngoài active-row filter. API #78 chọn queue row theo `PENDING_REVIEW`, còn #79 trả trạng thái hiện tại; stale queue policy giữa detail và #80/#81 vẫn cần xác nhận.

### 2.2. Q2 — selected Content version

- AC-33 n6 trực tiếp yêu cầu đọc version.
- `content_versions` lưu snapshot trước update theo migration 007, nhưng API #79 không nhận version ID/selector và response `Content` không có version field.
- Runtime hiện chỉ đọc current `contents` row; không truy vấn snapshot hay chọn “latest/pending/published” revision.
- Quy tắc revision identity giữa #78 → #79 → #80/#81 còn mở.

### 2.3. Q3 — Content author

- AC-33 n6 trực tiếp yêu cầu đọc author.
- `contents` không có creator/author field; API #50 insert cũng không ghi creator key.
- `content_versions.archived_by` là actor cập nhật row đã tạo snapshot, không phải tác giả gốc.
- Không suy ra author từ Mentor của course, reviewer, updater hoặc pilot UUID identity; runtime không trả author PII.

### 2.4. Physical source boundary

- Checked-in legacy `DB.sql`/migrations 006/007 định nghĩa `contents` và `content_versions`; đây là source hiện hành mà APIs #49–#53/#78/#79 dùng, nhưng không phải bằng chứng live deployment.
- V1-PILOT `content_blocks`/`course_versions` dùng UUID và version-scoped relations; không map trực tiếp sang BIGINT `contents` projection.
- `content_review_decisions.reviewer_subject_id` là reviewer identity, không phải Content author.

### 2.5. Kết quả query

- Không có active `contents` row theo ID, gồm soft-deleted row: 404 `DESIGN_RESOURCE_NOT_FOUND`.
- SQL/query/projection failure: safe 500 `DESIGN_INTERNAL_ERROR` và rollback.
- Query chỉ đọc; không commit, mutate, approve/reject hoặc ghi audit.

<a id="step-3-map-response"></a>

## 3. Map response

### 3.1. Direct ApiEnvelope<Content>

- `data` là một Content theo catalog; không bọc Page/list.
- Map đúng tám field của reusable Content schema.
- `data.status` phản ánh row hiện tại; không ép `PENDING_REVIEW`.
- Không thêm version, author, review_reason, reviewer, decision history hoặc audit fields.
- Diagram metadata-read intent và serialized response còn discrepancy; owner cần xác nhận metadata chỉ phục vụ xử lý nội bộ hay cần contract projection khác.

### 3.2. Envelope

- Success: HTTP 200 `DESIGN_RESOURCE_RETRIEVED`.
- Errors: đúng 401/403/404/500 và catalog business codes.
- `meta={}`; API #79 không có pagination.
- Runtime `error_response()` trả error `data:null`, phù hợp API guideline.

### Request Usage Matrix

| Request item | Source | Mapping step | Query use | Branch/response use | Gap |
|---|---|---|---|---|---|
| Authorization | Catalog Bearer/Admin | 0.1 | Guard trước Q1 | 401/403 | Moderation permission riêng chưa có. |
| content_id | Catalog int64 required | 1.1 | Bind `contents.id = :content_id` | Map `data.id`; invalid/no active row → 404 | Parse-to-404 là DERIVED theo #69. |
| Body | Not declared | N/A | None | None | DIRECT absence. |
| Query | Not declared | N/A | None | None | DIRECT absence. |

### Query Matrix

| Query ID | Type | Source | Conditions/projection | Result/branch | Evidence/status |
|---|---|---|---|---|---|
| Q1 | SELECT | `contents` | `id=:content_id AND deleted_at IS NULL`; select eight Content fields | One current Content; no row → 404 | Current checked-in legacy candidate; live DB unknown. |
| Q2 | None | `content_versions` not queried | No version selector in request/response | No version field returned | AC-33 read intent DIRECT; selection unresolved. |
| Q3 | None | No author relation | No author column or approved identity join | No author field returned | AC-33 read intent DIRECT; source absent. |

### Mutation Matrix

| Mutation ID | Operation | Target | Condition | Fields/effect | Status |
|---|---|---|---|---|---|
| N/A | None | N/A | API #79 is GET/read-only | No INSERT/UPDATE/DELETE, review decision or audit write | Runtime/source verified locally. |

## Response Source Matrix

| Response field | Contract type | Source | Transform/null rule | Gap/status |
|---|---|---|---|---|
| success | boolean | Envelope | true on success; false on error | Shared convention. |
| businessCode | string | Catalog | `DESIGN_RESOURCE_RETRIEVED` or exact listed error | DIRECT. |
| message | string | Application | Safe localized message | Exact wording not specified. |
| data | Content | Q1 | Singular object | DIRECT type; checked-in `contents` projection. |
| data.id | int64 | `contents.id` | Stored ID | Local source candidate. |
| data.course_id | int64 | `contents.course_id` | Stored relation ID | Local source candidate. |
| data.content_type | ContentType | `contents.content_type` | Stored string | No enum allowlist added. |
| data.title | string | `contents.title` | Stored string | Local source candidate. |
| data.payload | object | `contents.payload` | Preserve object; invalid projection fails safely | Local source candidate. |
| data.status | ContentStatus | `contents.status` | Current stored status | Stale-review policy remains open. |
| data.parent_id | int64? | `contents.parent_id` | Nullable value serializes as null | Local source candidate. |
| data.order | int32 | `contents.content_order` | Alias to `order` | Local source candidate. |
| meta | object | Envelope | `{}` | No pagination contract. |
| traceId | uuid | Shared trace middleware | Current trace ID or generated value | Runtime middleware. |
| Error data | null | Shared error helper | JSON null | Current source and guideline align. |

AC-33 node n6 requests version and author reads, but neither is part of reusable Content response and no response schema/author mapping is approved. This runtime returns only the direct catalog projection.

<a id="step-4-tra-response-hoac-loi"></a>

## 4. Trả response hoặc lỗi

- Thiếu/sai Bearer hoặc token không hợp lệ: 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Principal hợp lệ nhưng không có role Admin: 403 `DESIGN_ACCESS_DENIED`.
- Malformed/out-of-range ID hoặc không có active Content row: 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Query/read/mapping failure: 500 `DESIGN_INTERNAL_ERROR`.
- Không thêm 422/409, status gate, version conflict hoặc metadata fields ngoài catalog.

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
