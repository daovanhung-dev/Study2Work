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
Admin Bearer principal -> authorize role Admin -> parse optional type/course/page -> Q1 logical Content read where status=PENDING_REVIEW and apply approved filters -> reconcile list cardinality with ApiEnvelope<Content> -> map only Content contract -> 200 DESIGN_RESOURCE_RETRIEVED; auth failures 401/403; query/mapping failures 500
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
- Xác thực token trước khi truy cập pending queue.
- Principal cần role Admin theo catalog.
- Current `validate_current_user_request` chỉ chấp nhận role `STUDENT`; không dùng guard này cho API #78.
- Admin claims/guard/policy chưa có source hiện tại; API #78 chưa được wire.

### 0.2. Thứ tự truy cập

- Không chạy Q1 hoặc Q2 trước khi xác thực và authorize Admin thành công.
- Không lộ payload/content IDs cho principal không có role Admin.

### 0.3. Kết quả authorization

- Thiếu/sai Bearer hoặc token không hợp lệ: 401 `DESIGN_AUTHENTICATION_REQUIRED` theo catalog.
- Principal đã xác thực nhưng thiếu role Admin: 403 `DESIGN_ACCESS_DENIED` theo catalog.
- Không thêm permission riêng, tenant rule hoặc physical admin table khi chưa có source.

<a id="step-1-validate-data-input"></a>

## 1. Validate data input

### 1.1. `type`

- Nhận query `type` dạng string tùy chọn theo catalog.
- Proposal `DERIVED`: khi có giá trị, lọc exact match trên logical `Content.content_type`.
- ContentType members, casing, trimming và unknown-value behavior chưa được xác nhận.

### 1.2. `course`

- Nhận query `course` dạng int64 tùy chọn theo catalog.
- Proposal `DERIVED`: khi có giá trị, lọc exact match trên logical `Content.course_id`.
- Course existence rule và invalid/overflow mapping chưa được catalog xác định.

### 1.3. `page`

- Nhận query `page` dạng int32 tùy chọn theo catalog.
- Catalog không nêu default/min/max/page size; response schema hiện cũng không có pagination.
- Candidate nếu collection contract được duyệt: 1-based, default 1, fixed size 20, `id ASC`; toàn bộ là `DERIVED` theo precedent #68/#73, chưa áp dụng direct.
- Không thêm `size` hoặc `sort` vào request.

### 1.4. Input parsing boundary

- API #78 chỉ liệt kê error 401/403/500; không liệt kê 422.
- Invalid enum, page <= 0, int overflow và framework query parsing cần contract/integration confirmation.
- Middleware hiện trả 422 `VALIDATION_ERROR` cho path không thuộc `DESIGN_CONTRACT_PATHS`; route #78 hiện absent.

<a id="step-2-get-thong-tin"></a>

## 2. Get thông tin

### 2.1. Q1 — logical pending queue read

AC-33 node n3 trực tiếp ghi “Đọc content status = PENDING_REVIEW”. Q1 chỉ được mô tả ở mức logical vì không có physical Content relation phù hợp đã được duyệt.

| Logical field | Value/source | Rule/status |
|---|---|---|
| `status` | `PENDING_REVIEW` | Direct fixed predicate từ AC-33. |
| `content_type` | Query `type` khi được gửi | Exact-match candidate; enum/casing/source unresolved. |
| `course_id` | Query `course` khi được gửi | Exact-match candidate; physical course relation unresolved. |
| `id` | Content identifier | Không có Content BIGINT table đã được xác nhận. |
| Content payload fields | Reusable Content schema | Field list direct; physical columns/serialization SOURCE_REQUIRED. |

Do không có approved table/column, không viết SQL giả định như `contents`, `content_versions` hoặc đổi `content_blocks` thành Content. V1-PILOT `content_review_decisions` là decision log, không phải queue source.

### 2.2. Pagination and ordering candidate

- Nếu catalog response được cập nhật thành `ApiEnvelope<Page<Content>>`, dùng Q1 filter set thống nhất cho item query và count query.
- Candidate: page omitted → 1; fixed size → 20; `offset = (page - 1) * 20`; stable order → `id ASC`.
- Các candidate trên là `DERIVED`. Chưa có cột thời gian queue hoặc owner policy cho FIFO; `id ASC` chỉ là thứ tự ổn định đề xuất.
- Khi giữ direct `ApiEnvelope<Content>`, không có mapping đã xác định để trả một page hoặc biểu diễn queue rỗng.

### 2.3. Q2 — count candidate

- Chỉ cần Q2 nếu response contract được chuyển sang Page có `PageMeta`.
- Q2 phải dùng cùng `PENDING_REVIEW`, `type` và `course` predicates với Q1.
- Content schema/table chưa có source; Q2 là logical requirement, không phải SQL được duyệt.

### 2.4. Kết quả query

- Query/storage/mapping failure: 500 `DESIGN_INTERNAL_ERROR` theo catalog.
- Không có pending rows: candidate Page response là HTTP 200 với `items=[]`; empty behavior chưa áp dụng được cho direct `Content` đơn.
- Không trả 404 cho queue rỗng vì catalog #78 không liệt kê 404.
- Không select/version-join, review author hoặc decision record trong #78; AC-33 giao content/version/author detail cho #79.
- Deleted/stale revision filtering và producer selection chưa được AC-33 quy định; giữ `SOURCE_REQUIRED`.

<a id="step-3-map-response"></a>

## 3. Map response

### 3.1. Direct catalog contract

- Success code là 200 `DESIGN_RESOURCE_RETRIEVED` với `ApiEnvelope<Content>`.
- Nếu Content row/cardinality được xác định, map đúng tám reusable fields tại `04_Response.md`.
- `data.status` của item thuộc queue phải phản ánh `PENDING_REVIEW` theo predicate AC-33.
- Không thêm `author`, `version`, `review_reason`, `reviewer`, decision history, `items` hoặc `pagination` vào direct response.
- Vì response là một Content nhưng endpoint là queue có `page`, mapping cardinality chưa implementation-ready.

### 3.2. Candidate collection contract — cần catalog correction

- Proposal `DERIVED`: `ApiEnvelope<Page<Content>>` với `items[]` và `pagination`.
- Chỉ dùng proposal sau khi contract owner cập nhật catalog; không xem example candidate là runtime response.
- Q1 row count, PageMeta và empty `items=[]` khi queue rỗng cần đồng bộ với API #68/#73 conventions.

### Request Usage Matrix

| Request item | Source | Mapping step | Query use | Branch/response use | Gap |
|---|---|---|---|---|---|
| Authorization | Catalog Bearer/Admin | 0.1 | Không bind query; authorize trước Q1 | 401/403 | Admin guard/claim SOURCE_REQUIRED. |
| `type` | Catalog string | 1.1 | Candidate `content_type = :type` | Không echo request | Exact match/enum members SOURCE_REQUIRED. |
| `course` | Catalog int64 | 1.2 | Candidate `course_id = :course` | Không echo request | Physical relation SOURCE_REQUIRED. |
| `page` | Catalog int32 | 1.3 | Candidate LIMIT/OFFSET if Page | PageMeta only under revised contract | Current singular response conflicts. |
| Body | Not declared | N/A | None | None | DIRECT absence. |

### Query Matrix

| Query ID | Type | Candidate source | Logical fields/conditions | Result/branch | Evidence/status |
|---|---|---|---|---|---|
| Q1 | SELECT list, logical | Content source `SOURCE_REQUIRED` | `status=PENDING_REVIEW`; optional `content_type=:type`; optional `course_id=:course` | Queue rows; 500 on query/mapping failure | Status predicate DIRECT; table/columns SOURCE_REQUIRED. |
| Q1-PAGE | LIMIT/OFFSET candidate | Same Q1 logical set | Candidate page 1/size 20/order id ASC | Page items only if catalog changes to Page | DERIVED; not current direct contract. |
| Q2 | COUNT candidate | Same logical Content source | Exactly Q1 predicates | `PageMeta.total` candidate | Only if Page response approved; no physical SQL source. |

### Mutation Matrix

| Mutation ID | Operation | Target | Condition | Fields/effect | Status |
|---|---|---|---|---|---|
| N/A | None | N/A | API is GET/read-only | No INSERT/UPDATE/DELETE or audit write | `N/A — READ-ONLY API` |

## Response Source Matrix

| Response field | Contract type | Source type | Table/column or generator | Transform/null rule | Gap/status |
|---|---|---|---|---|---|
| `success` | boolean | Envelope | Branch | true on success; false on error | Envelope convention. |
| `businessCode` | string | Catalog | Branch literal | Exact listed code only | DIRECT. |
| `message` | string | Application | Safe localized message | Exact wording unspecified | DERIVED. |
| `data` | `Content` | Logical pending row | Queue result | Catalog says singular; list/page cardinality unresolved | DIRECT / DISCREPANCY. |
| `data.id` | int64 | Content source | Logical Content identifier | Required | Physical mapping SOURCE_REQUIRED. |
| `data.course_id` | int64 | Content source | Logical owning course | Required | Physical mapping SOURCE_REQUIRED. |
| `data.content_type` | ContentType | Content source | Logical type | Preserve approved enum serialization | Enum/physical mapping SOURCE_REQUIRED. |
| `data.title` | string | Content source | Logical title | Preserve approved stored value | Physical mapping SOURCE_REQUIRED. |
| `data.payload` | object | Content source | Logical subtype payload | Do not invent keys/default | Schema/storage SOURCE_REQUIRED. |
| `data.status` | ContentStatus | AC-33 predicate + Content source | Logical status | Must satisfy `PENDING_REVIEW` filter | Predicate DIRECT; serialization/storage SOURCE_REQUIRED. |
| `data.parent_id` | int64? | Content source | Logical parent relation | Optional null/omit rule unresolved | SOURCE_REQUIRED. |
| `data.order` | int32 | Content source | Logical sibling position | Does not determine queue sort | SOURCE_REQUIRED. |
| `data.items[]` | `Content[]` | Q1 row set | Candidate Page wrapper | Not in direct schema | DERIVED; catalog update required. |
| `data.pagination.page` | int32 | Query/default candidate | Page selection | Candidate page | DERIVED; wrapper not direct. |
| `data.pagination.size` | int32 | Fixed-size candidate | Candidate 20 | No `size` query | DERIVED; wrapper not direct. |
| `data.pagination.total` | int64 | Q2 candidate | Count with Q1 filters | 0 when no rows under candidate | DERIVED; no source query. |
| `data.pagination.total_pages` | int32 | Formula candidate | `ceil(total/size)` | 0 when total=0 | DERIVED; wrapper not direct. |
| `meta` | object | Envelope | `{}` candidate | No approved page metadata under direct contract | Candidate convention. |
| `traceId` | uuid | Middleware | Current request trace | Propagate/generate | Current convention; endpoint unwired. |
| Error `data` | null by guideline | Helper current behavior | `error_response()` default | Current helper emits `{}` | DISCREPANCY. |

<a id="step-4-tra-response-hoac-loi"></a>

## 4. Trả response hoặc lỗi

1. Authenticate Bearer and require Admin before reading queue.
2. Parse only catalog query keys `type`, `course`, `page`; do not add `size`/`sort`.
3. Q1 selects logical items whose status is `PENDING_REVIEW` and applies approved optional filters.
4. Return HTTP 200 `DESIGN_RESOURCE_RETRIEVED` using catalog `ApiEnvelope<Content>` only after cardinality is resolved; candidate collection response requires catalog correction.
5. Thiếu/sai Bearer hoặc token không hợp lệ trả 401; principal thiếu role Admin trả 403 theo catalog.
6. Query/mapping failure maps to 500 `DESIGN_INTERNAL_ERROR`; do not expose SQL, payload internals or stack trace.
7. Detail/version/author lookup and approve/reject/audit effects remain in #79–#81.

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
