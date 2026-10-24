---
title: "Data Mapping"
order: 5
dd_id: "97"
api_name: "Lấy reported discussions"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

```text
Admin Bearer principal -> authorize Admin -> parse optional reason/severity/page -> logical AC-37 read reports + discussion summary -> candidate discussion/author/comment projection if approved schema supports it -> Page<Discussion> with unresolved PageMeta values -> 200 DESIGN_RESOURCE_RETRIEVED; auth failures 401/403; internal failures 500
```

## Mục lục

- [0. Check quyền](#step-0-check-quyen)
- [1. Validate request](#step-1-validate-request)
- [2. Đọc queue](#step-2-doc-queue)
- [3. Mutation](#step-3-mutation)
- [4. Response mapping](#step-4-response-mapping)
- [Request Usage Matrix](#request-usage-matrix)
- [Query Matrix](#query-matrix)
- [Mutation Matrix](#mutation-matrix)
- [Response Source Matrix](#response-source-matrix)

<a id="step-0-check-quyen"></a>
## 0. Check quyền

- Xác thực Bearer JWT trước khi đọc reports/discussions.
- Yêu cầu Admin role theo catalog. Current `validate_current_user_request` chỉ authorize Student; không tái sử dụng cho API #97.
- Admin claim shape, identity mapping, scope/policy và guard chưa có source trong Study; giữ `SOURCE_REQUIRED`.
- Không chạy queue query trước authorization thành công và không làm lộ dữ liệu queue cho principal bị từ chối.
- 401/403 dùng đúng business code catalog. Thứ tự kiểm tra role so với các query filter không được phép tạo side channel.

<a id="step-1-validate-request"></a>
## 1. Validate request

- `reason` và `severity` là optional string; filter logic trực tiếp trên report source chưa có schema.
- `page` là optional int32. Catalog không có default/min/max, không có `size` và không nêu sort.
- Không chuẩn hóa trim/casing, không xác định AND/OR, không từ chối giá trị lạ khi taxonomy chưa được định nghĩa.
- Catalog không liệt kê 422; parse/range behavior của framework khi route được wire cần được giải quyết mà không tự thêm business code vào contract.

<a id="step-2-doc-queue"></a>
## 2. Đọc queue

### 2.1. Q1 — logical reported queue read

AC-37 diagram node n3 trực tiếp yêu cầu “Đọc reports + discussion summary”. Đây là logical read; sơ đồ không nêu relation, report ID, report grain, join key, dedup rule hoặc sort.

| Logical input/field | Use | Rule/status |
|---|---|---|
| Report state | Chọn report thuộc queue | AC-37 precondition nói có discussion bị report hoặc cần moderation; trạng thái lưu trữ `SOURCE_REQUIRED` |
| `reason` | Optional report filter | DIRECT query name/type; source field, taxonomy và matching `SOURCE_REQUIRED` |
| `severity` | Optional report filter | DIRECT query name/type; source field, taxonomy và matching `SOURCE_REQUIRED` |
| `discussion_id` | Join report với discussion | Diagram implies relationship; physical key/source `SOURCE_REQUIRED` |
| `page` | Paginate queue | DIRECT query name/type; default, size, sort, count grain `SOURCE_REQUIRED` |
| Deduplication | One row per discussion or one row per report | Not defined by catalog/diagram; `SOURCE_REQUIRED` |

Không viết SQL giả định như `reports` hoặc `discussion_reports`. Legacy DDL chỉ có `discussions`; chưa có relation để nhận diện reported rows hay filter reason/severity.

### 2.2. Candidate discussion projection — not an approved query

| Candidate source | Candidate field | Possible response use | Evidence/status |
|---|---|---|---|
| legacy `discussions` | `id` | `Discussion.id` | DDL candidate, not live confirmation |
| legacy `discussions` | `course_id` | `Discussion.course_id` | DDL nullable vs logical required |
| legacy `discussions` | `content` | `Discussion.content` | Candidate direct mapping |
| legacy `discussions` | `user_id` | Join key for author | DDL nullable; author required |
| legacy `discussions` | `status` | `Discussion.status` | Enum and moderation visibility unresolved |
| legacy `discussions` | `parent_id` | Root/comment relation candidate | No root-only or child inclusion rule in #97 |
| legacy `discussions` | timestamps | Candidate ordering only | No ordering contract; do not use as chosen sort |
| legacy `users` | `id`, `full_name`, `avatar_url` | `UserSummary` | Candidate projection only |
| legacy `discussions` | `title` | `Discussion.title` | Missing column; no derivation from `content` |

### 2.3. Q2 — Page metadata

`PageMeta` directly requires `page`, `size`, `total`, `total_pages`. Request exposes only optional `page`; catalog and AC-37 do not define default, page size, ordering, count grain, out-of-range behavior, or whether total counts reports or unique discussions. Keep values `SOURCE_REQUIRED`.

A candidate `page=1`, fixed `size=20`, count with same filters, and `ceil(total/size)` is `DERIVED` only by analogy with other Admin list DDs. It is not approved behavior and is not used to close the gap in this DD.

### 2.4. Q3 — nested comments

`Discussion.comments` is a required array in the reusable schema, while AC-37 step calls this a discussion summary and API #98 separately reads full thread detail. Whether #97 includes no comments, comment preview, all comments, or only direct children is unresolved. Candidate self-reference is `discussions.parent_id`; do not create an empty-array policy or status/order filter without confirmation.

<a id="step-3-mutation"></a>
## 3. Mutation

No mutation is declared. API #97 performs no `INSERT`, `UPDATE`, `DELETE`, report acknowledgement, moderation action, or audit write. Those actions belong to later AC-37 APIs and are not part of this read endpoint.

<a id="step-4-response-mapping"></a>
## 4. Response mapping

- Return only the catalog `ApiEnvelope<Page<Discussion>>`; do not add report reason/severity fields to Discussion.
- Every Discussion/DiscussionComment/UserSummary field is inventoried in Response Source Matrix.
- `title` cannot be sourced from legacy DDL. Do not derive it from `content`.
- Candidate `course_id`, `user_id` are nullable in DDL although logical response requires course and author. Treat missing required joins as an unresolved integrity mapping, not an empty/fabricated value.
- Do not claim that example pagination values are defaults.

## Request Usage Matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Bearer header | Authenticate and authorize Admin | Role direct; implementation `SOURCE_REQUIRED` |
| `reason` | Optional query string | Logical report filter | DIRECT name/type; physical source/semantics unresolved |
| `severity` | Optional query string | Logical report filter | DIRECT name/type; enum/semantics unresolved |
| `page` | Optional int32 query | Requested result page | DIRECT name/type; pagination policy unresolved |
| Body/path | None declared | None | DIRECT |

## Query Matrix

| Query | Operation | Relation/fields | Purpose | Status |
|---|---|---|---|---|
| Q1 | Logical SELECT | Report source + discussion join, fields/key/filter/order unknown | AC-37 reported queue | `SOURCE_REQUIRED`; no SQL/table invented |
| Q1a | Candidate SELECT only | legacy `discussions`: id, course_id, user_id, parent_id, content, status, timestamps | Discussion projection candidate | Legacy schema artifact; cannot identify report rows or title |
| Q1b | Candidate JOIN only | legacy `users`: id, full_name, avatar_url via candidate `user_id` | `UserSummary` candidate | Join/null/live behavior unresolved |
| Q1c | Candidate self-JOIN only | `discussions.parent_id` and child rows | `comments[]` candidate | Summary extent/status/order unresolved |
| Q2 | Logical COUNT/page | Queue grain and predicates unavailable | PageMeta | `SOURCE_REQUIRED` |

## Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | Read-only GET | No INSERT/UPDATE/DELETE | `N/A — READ-ONLY API` |

## Response Source Matrix

| Response field | Type | Candidate source | Mapping/null rule | Evidence status |
|---|---|---|---|---|
| `success` | boolean | Envelope | `true` on success branch | DIRECT convention |
| `businessCode` | string | Catalog | `DESIGN_RESOURCE_RETRIEVED` | DIRECT |
| `message` | string | Application | Safe message | Exact wording unspecified |
| `data` | `Page<Discussion>` | Logical Q1 result | Queue grain/dedup unresolved | DIRECT schema; source `SOURCE_REQUIRED` |
| `data.items[]` | `Discussion[]` | Logical Q1 result | Queue grain/dedup unresolved | DIRECT schema; source `SOURCE_REQUIRED` |
| `data.items[].id` | int64 | `discussions.id` candidate | Direct candidate | Legacy only |
| `data.items[].course_id` | int64 | `discussions.course_id` candidate | Required; physical null discrepancy | Legacy nullable |
| `data.items[].title` | string | No source | Do not alias from `content` | `SOURCE_REQUIRED` |
| `data.items[].content` | string | `discussions.content` candidate | Preserve text | Legacy candidate |
| `data.items[].author` | `UserSummary` | Candidate `users` join | Required object; missing author behavior unresolved | `SOURCE_REQUIRED` if absent |
| `data.items[].author.id` | int64 | `users.id` candidate | Candidate join on user_id | Live join/required author unresolved |
| `data.items[].author.full_name` | string | `users.full_name` candidate | Direct candidate | Legacy candidate |
| `data.items[].author.avatar_url` | uri? | `users.avatar_url` candidate | Omit if null | Legacy candidate |
| `data.items[].status` | `DiscussionStatus` | `discussions.status` candidate | Return source token only if enum approved | Enum unresolved |
| `data.items[].comments` | `DiscussionComment[]` | Child discussion rows | No inclusion/cardinality rule | `SOURCE_REQUIRED` |
| `data.items[].comments[].id` | int64 | Child `discussions.id` | Direct candidate | Legacy only |
| `data.items[].comments[].discussion_id` | int64 | Child `parent_id` | Candidate parent key | Legacy nullable |
| `data.items[].comments[].content` | string | Child `discussions.content` | Preserve text | Legacy candidate |
| `data.items[].comments[].author` | `UserSummary` | Candidate child `users` join | Required object | Missing-author behavior unresolved |
| `data.items[].comments[].author.id` | int64 | Child `user_id` → `users.id` | Candidate author key | Legacy only; live join unverified |
| `data.items[].comments[].author.full_name` | string | `users.full_name` candidate | Direct candidate | Legacy only |
| `data.items[].comments[].author.avatar_url` | uri? | `users.avatar_url` candidate | Omit if null | Legacy only |
| `data.items[].comments[].created_at` | date-time | Child `discussions.created_at` | Serialize per approved timezone convention | DDL timestamp lacks timezone |
| `data.pagination` | `PageMeta` | Logical page metadata | Values/default unresolved | DIRECT schema; source `SOURCE_REQUIRED` |
| `data.pagination.page` | int32 | Request/default policy | No default inferred | `SOURCE_REQUIRED` |
| `data.pagination.size` | int32 | Page-size policy | No size query or approved fixed size | `SOURCE_REQUIRED` |
| `data.pagination.total` | int64 | Queue count | Report-vs-discussion grain unresolved | `SOURCE_REQUIRED` |
| `data.pagination.total_pages` | int32 | Page calculation | Formula/default unresolved | `SOURCE_REQUIRED` |
| `meta` | object | Envelope | No endpoint-specific fields defined | DIRECT type |
| `traceId` | uuid | Request trace | Propagate trace ID | Envelope convention |

## Error mapping

| Condition | HTTP/business code | Basis/status |
|---|---|---|
| Missing/invalid Bearer JWT | 401 `DESIGN_AUTHENTICATION_REQUIRED` | Catalog direct |
| Authenticated non-Admin | 403 `DESIGN_ACCESS_DENIED` | Catalog direct; Admin guard source absent |
| Query/data retrieval or required-field mapping failure | 500 `DESIGN_INTERNAL_ERROR` | Catalog direct; exact internal branch unspecified |
| Invalid query parse/range | No catalog code specified | `SOURCE_REQUIRED`; do not add 422 |
| No matching reported rows | 200 success candidate with empty `items` | `DERIVED`; empty page metadata policy unresolved |

## Runtime and envelope discrepancy

API #97 is absent. Current middleware `DESIGN_CONTRACT_PATHS` does not include its route, so future framework validation/unhandled errors would use generic fallback codes unless the allowlist/wiring is updated. Current `error_response` emits `{}` for absent `data`; API guidelines describe `data:null`. This is conditional integration discrepancy, not current #97 behavior.

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
