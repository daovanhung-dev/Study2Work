---
title: "Data Mapping"
order: 5
dd_id: "78"
api_name: "Lấy pending content"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
GET /api/v1/admin/content/pending -> shared ADMIN JWT guard -> parse raw type/course/page -> COUNT + page SELECT active contents with status=PENDING_REVIEW and identical exact filters -> map reusable Content -> return DERIVED Page<Content> in DESIGN_RESOURCE_RETRIEVED envelope; validation is derived 422; query/mapping failure is safe 500; no writes
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

<a id="0-check-quyen"></a><a id="step-0-check-quyen"></a>
## 0. Check quyền

### 0.1. Xác thực Admin

- Dùng `validate_current_user_request(..., role="ADMIN")` từ shared auth helper.
- Xác thực Bearer/JWT và role trước khi parse `course`/`page` hoặc query.
- Thiếu/sai token trả 401 `DESIGN_AUTHENTICATION_REQUIRED`; thiếu role trả 403 `DESIGN_ACCESS_DENIED`.
- Shared guard hiện xác minh role ADMIN; permission `content-moderation` riêng chưa có source.

### 0.2. Thứ tự truy cập

- Không chạy count/list query trước khi authorization và numeric query validation thành công.
- Không để principal trái quyền suy luận số lượng hoặc đọc payload pending.

<a id="step-1-validate-data-input"></a>

<a id="step-1-validate-data-input"></a>
## 1. Validate data input

### 1.1. `type`

- Query string tùy chọn; giữ nguyên giá trị và exact-match `contents.content_type`.
- Không trim, đổi case hoặc thêm whitelist vì ContentType members chưa có nguồn.
- Chuỗi lạ hợp lệ về kiểu và thường trả page rỗng.

### 1.2. `course`

- Parse raw query thành signed int64; không áp đặt positive-only rule ngoài contract.
- Khi có giá trị, exact-match `contents.course_id`.
- Sai format hoặc overflow trả 422 `DESIGN_VALIDATION_ERROR` theo fallback DERIVED; không truy cập DB.

### 1.3. `page`

- Parse raw query thành positive int32; omitted mặc định 1.
- Fixed page size là 20, theo Admin list #73; không thêm query `size` hoặc `sort`.
- Sai format, `page < 1` hoặc vượt int32 trả 422 `DESIGN_VALIDATION_ERROR` theo fallback DERIVED.
- `offset = (page - 1) * 20`; page nằm ngoài phạm vi dữ liệu vẫn trả 200 với items rỗng.

### 1.4. Cardinality discrepancy

- Direct catalog `ApiEnvelope<Content>` không khớp AC-33 queue/page flow.
- Runtime chọn `ApiEnvelope<Page<Content>>` là DERIVED để biểu diễn nhiều rows và queue rỗng. Cần owner/catalog correction; không sửa catalog trong task này.

<a id="step-2-get-thong-tin"></a>

<a id="step-2-get-thong-tin"></a>
## 2. Get thông tin

### 2.1. Q1 — count active pending Content

`COUNT_ADMIN_PENDING_CONTENTS` đếm `contents` rows với predicates:

| Column | Predicate | Basis |
|---|---|---|
| `status` | `= 'PENDING_REVIEW'` | Direct AC-33 queue step n3. |
| `deleted_at` | `IS NULL` | DERIVED active-row policy, aligned with current APIs #49/#53. |
| `content_type` | Optional `= :content_type` | DERIVED exact mapping from query `type`. |
| `course_id` | Optional `= :course_id` | DERIVED exact mapping from query `course`. |

### 2.2. Q2 — read bounded page

`LIST_ADMIN_PENDING_CONTENTS` selects the same predicates and columns needed for reusable Content: `id`, `course_id`, `content_type`, `title`, `payload`, `status`, `parent_id`, `content_order AS order`. It orders by `id ASC`, with fixed `LIMIT 20` and computed `OFFSET`.

Count and list share identical filter SQL and bound parameters. No `content_versions`, author, reviewer or decision-history join is performed. API #50 creates a current `contents` row as `PENDING_REVIEW`; API #51 snapshots the previous row and updates the current logical row to `PENDING_REVIEW`. Which revision the later #79–#81 operation should bind remains unresolved.

### 2.3. Kết quả query

- Query, malformed count, invalid page row, or invalid Content projection returns safe 500 `DESIGN_INTERNAL_ERROR` and rolls back the read transaction.
- Empty queue and page beyond last page return 200 with `items=[]`, total preserved, and `total_pages=0` only when total is zero.
- Soft-deleted rows are not returned under the local DERIVED active-row filter.
- No query mutation, commit, audit or status transition occurs.

<a id="step-3-map-response"></a>

<a id="step-3-map-response"></a>
## 3. Map response

### 3.1. Content item

- Reuse API #49 `ContentResponse`: `id`, `course_id`, `content_type`, `title`, object `payload`, `status`, nullable `parent_id`, `order`.
- `status` must equal `PENDING_REVIEW`; returned filter values must match requested `type`/`course` when supplied.
- `order` maps from `content_order`; it is not used as queue priority.
- Do not add `author`, `version`, `review_reason`, `reviewer`, `items` or `pagination` to the Content item itself.

### 3.2. Page envelope

- Local DERIVED `data` is `{items: Content[], pagination: PageMeta}`.
- `page` is the validated request/default; `size=20`; `total` is the count query; `total_pages=ceil(total/20)`, or 0 when total is 0.
- Catalog's direct `data:Content` remains a documented discrepancy.

### Request Usage Matrix

| Request item | Source | Mapping step | Query use | Branch/response use | Gap |
|---|---|---|---|---|---|
| Authorization | Catalog Bearer/Admin | 0.1 | Authorize before query | 401/403 | Dedicated moderation permission remains open. |
| `type` | Catalog string | 1.1 | Optional exact `content_type` | Not echoed | Enum values/casing not defined. |
| `course` | Catalog int64 | 1.2 | Optional exact `course_id` | Not echoed | Malformed/overflow 422 is DERIVED. |
| `page` | Catalog int32 | 1.3 | `LIMIT/OFFSET` | Page metadata | Default/size/order/422 are DERIVED. |
| Body | Not declared | N/A | None | None | DIRECT absence. |

### Query Matrix

| Query ID | Type | Source | Conditions | Result/branch | Evidence/status |
|---|---|---|---|---|---|
| Q1 | COUNT | Legacy `contents` candidate | PENDING_REVIEW, active row, optional exact type/course | total | Status DIRECT; physical/filter/deleted mapping local candidate/DERIVED; live DB unknown. |
| Q2 | SELECT page | Legacy `contents` candidate | Same Q1 filters, `id ASC`, LIMIT 20/OFFSET | current Content rows | Schema and API #49–#53 source; pagination/order DERIVED. |

### Mutation Matrix

| Mutation ID | Operation | Target | Condition | Fields/effect | Status |
|---|---|---|---|---|---|
| N/A | None | N/A | API is GET/read-only | No INSERT/UPDATE/DELETE or audit write | `N/A — READ-ONLY API` |

## Response Source Matrix

| Response field | Contract type | Source/generator | Transform/null rule | Status |
|---|---|---|---|---|
| `success` | boolean | Shared envelope | true on success | Runtime convention. |
| `businessCode` | string | Catalog/helper | `DESIGN_RESOURCE_RETRIEVED` or exact error code | Success direct; 422 branch derived. |
| `message` | string | Application | Safe localized message | Text not specified. |
| `data.items[]` | Content[] | Query Q2 / `contents` | Map via API #49 reusable Content model | Page cardinality DERIVED. |
| `data.items[].id` | int64 | `contents.id` | Preserve BIGINT value | Checked-in candidate; live source unknown. |
| `data.items[].course_id` | int64 | `contents.course_id` | Preserve | Exact filter mapping DERIVED. |
| `data.items[].content_type` | ContentType | `contents.content_type` | Preserve exact string | Enum not confirmed. |
| `data.items[].title` | string | `contents.title` | Preserve | Legacy candidate. |
| `data.items[].payload` | object | `contents.payload` | JSONB object to JSON mapping | No payload keys invented. |
| `data.items[].status` | ContentStatus | `contents.status` | Selected row must be `PENDING_REVIEW` | Predicate direct; enum open. |
| `data.items[].parent_id` | int64? | `contents.parent_id` | Preserve null | Optional reusable field. |
| `data.items[].order` | int32 | `contents.content_order` | Alias to `order` | Checked-in candidate. |
| `data.pagination` | PageMeta | Request + count | Page/default, 20, total, ceil(total/20) | DERIVED. |
| `meta` | object | Shared envelope | `{}` | Current convention. |
| `traceId` | uuid | Trace middleware | Propagate/generate | Current source. |
| Error `data` | null | `error_response()` | JSON null by default | Current source; old DD `{}` claim corrected. |

<a id="step-4-tra-response-hoac-loi"></a>

<a id="step-4-tra-response-hoac-loi"></a>
## 4. Trả response hoặc lỗi

1. Authenticate shared Bearer JWT and require role ADMIN before parsing/querying.
2. Parse only catalog query keys `type`, `course`, `page`; do not add `size`/`sort`.
3. Count and select active rows whose status is `PENDING_REVIEW`; filters/order/page are documented above.
4. Return HTTP 200 `DESIGN_RESOURCE_RETRIEVED` with DERIVED `Page<Content>`; queue empty is a valid empty page.
5. Invalid numeric course/page returns derived 422 `DESIGN_VALIDATION_ERROR`; catalog correction remains open.
6. Query/count/projection failure returns safe 500 `DESIGN_INTERNAL_ERROR` and rolls back; no commit/mutation.
7. Detail/version/author and approve/reject/audit effects stay in #79–#81.

Chi tiết error: [06_Error.md](./06_Error.md). Response fields: [04_Response.md](./04_Response.md).

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
