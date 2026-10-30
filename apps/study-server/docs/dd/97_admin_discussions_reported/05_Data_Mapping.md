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
Admin Bearer principal -> shared ADMIN guard -> parse optional reason/severity/page -> Study-local `discussion_reports` active queue read -> one Discussion summary per ID -> fixed Page metadata -> 200 DESIGN_RESOURCE_RETRIEVED; auth failures 401/403; invalid page 422 DERIVED; internal failures 500
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

- Xác thực Bearer JWT bằng `validate_current_user_request(..., role="ADMIN")` trước khi đọc reports/discussions.
- Shared ADMIN guard hiện có và được dùng bởi Admin APIs #68–#96; fine-grained AC-37 permission/tenant policy vẫn chưa được xác minh.
- Không chạy queue query trước authorization thành công và không làm lộ dữ liệu queue cho principal bị từ chối.
- 401/403 dùng đúng business code catalog. Thứ tự kiểm tra role so với các query filter không được phép tạo side channel.

<a id="step-1-validate-request"></a>
## 1. Validate request

- `reason` và `severity` là optional string, được bind exact-match không chuẩn hóa; nếu cùng truyền thì kết hợp AND trên cùng report.
- `page` là optional int32; fallback dùng default 1, yêu cầu dương, page size cố định 20.
- Page parse/range lỗi trả 422 `DESIGN_VALIDATION_ERROR` theo fallback `DERIVED`; catalog không liệt kê status này.

<a id="step-2-doc-queue"></a>
## 2. Đọc queue

### 2.1. Q1 — logical reported queue read

AC-37 diagram node n3 trực tiếp yêu cầu “Đọc reports + discussion summary”. Do không có report relation Study, implementation thêm migration fallback `discussion_reports` gắn vào Discussion BIGINT.

| Logical input/field | Use | Rule/status |
|---|---|---|
| Report state | Chọn report thuộc queue | `OPEN` hoặc `IN_REVIEW`; `DERIVED` từ generic moderation report status tokens |
| `reason` | Optional report filter | Exact `discussion_reports.reason_code` match; free-form taxonomy |
| `severity` | Optional report filter | Exact `discussion_reports.severity` match; free-form taxonomy |
| `discussion_id` | Join report với discussion | BIGINT FK `discussion_reports.discussion_id` → `discussions.id` |
| `page` | Paginate queue | Default 1, fixed size 20, positive int32, stable order |
| Deduplication | Queue item grain | One unique Discussion; count distinct IDs |

Physical table and status/filter rules are a local `DERIVED` fallback; the migration is not deployed-schema evidence and this API has no report-ingest writer.

### 2.2. Discussion summary projection

| Candidate source | Candidate field | Possible response use | Evidence/status |
|---|---|---|---|
| legacy `discussions` | `id`, `course_id`, `content`, `status` | `Discussion` | Legacy candidate; required nulls/status strings are validated |
| legacy `discussions` | `content` | `Discussion.title` | Whitespace-normalized and clipped to 120 characters; `DERIVED` |
| legacy `discussions` | `user_id` | Join key for author | Legacy nullable FK; absent user makes projection fail safely |
| legacy `users` | `id`, `full_name`, `avatar_url` | `UserSummary` | Legacy join candidate, live schema unverified |
| `discussion_reports` | `created_at`, `discussion_id` | Queue order and Discussion grouping | Latest matching active report per Discussion |
| `discussions` self-reference | `parent_id` | `comments[]` | Not loaded in queue summary; returned `[]`, `DERIVED` |

### 2.3. Q2 — Page metadata

`PageMeta` returns the requested/default page, fixed size 20, count of unique Discussions with a matching active report, and `ceil(total/20)` (`0` when total is 0). Out-of-range pages return an empty `items` array and preserve the requested page. All values are `DERIVED`.

### 2.4. Q3 — nested comments

`Discussion.comments` is a required array in the reusable schema. AC-37 calls #97 a summary and #98 separately reads full thread detail; therefore #97 returns an empty array and leaves child rows to #98 (`DERIVED`).

<a id="step-3-mutation"></a>
## 3. Mutation

No mutation is declared. API #97 performs no `INSERT`, `UPDATE`, `DELETE`, report acknowledgement, moderation action, or audit write. Those actions belong to later AC-37 APIs and are not part of this read endpoint.

<a id="step-4-response-mapping"></a>
## 4. Response mapping

- Return only catalog `ApiEnvelope<Page<Discussion>>`; do not add report fields to Discussion.
- `title` uses the documented normalized-content snippet fallback; `comments=[]` is the queue-summary fallback.
- Required `course_id` and author fields are validated; malformed/nullable projection returns 500, never fabricated values.
- Pagination behavior is `DERIVED` and recorded above.

## Request Usage Matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Bearer header | Shared ADMIN guard | DIRECT role; shared guard used before query |
| `reason` | Optional query string | Exact filter on `reason_code` | `DERIVED`; no taxonomy/normalization |
| `severity` | Optional query string | Exact filter on `severity` | `DERIVED`; no taxonomy/normalization |
| `page` | Optional int32 query | Requested result page | Default 1; positive int32; size 20 (`DERIVED`) |
| Body/path | None declared | None | DIRECT |

## Query Matrix

| Query | Operation | Relation/fields | Purpose | Status |
|---|---|---|---|---|
| Q1 | SELECT + `DISTINCT ON` | `discussion_reports` active rows joined to legacy `discussions` | Unique reported Discussion queue | `DERIVED`; migration 014 candidate |
| Q1a | SELECT | `discussions`: id, course_id, user_id, content, status | Discussion projection | Legacy DDL candidate; title derives from content |
| Q1b | LEFT JOIN | `users.id = discussions.user_id` | `UserSummary` | Missing required author returns 500 |
| Q1c | No query | Child rows are not loaded | `comments=[]` summary | `DERIVED`; #98 owns full thread |
| Q2 | COUNT DISTINCT | Same active-state and exact filters as Q1 | PageMeta | Unique Discussion count, `DERIVED` |

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
| `data` | `Page<Discussion>` | Queue result | One unique Discussion per active-report group | DIRECT schema; grain `DERIVED` |
| `data.items[]` | `Discussion[]` | Joined Discussion row | Empty when no active report matches | DIRECT schema |
| `data.items[].id` | int64 | `discussions.id` | Direct mapping | Legacy candidate |
| `data.items[].course_id` | int64 | `discussions.course_id` | Required; null fails projection | Legacy nullable |
| `data.items[].title` | string | `discussions.content` | Normalize whitespace, clip to 120 chars | `DERIVED` |
| `data.items[].content` | string | `discussions.content` | Preserve exact content | Legacy candidate |
| `data.items[].author` | `UserSummary` | `users` join | Required; missing author fails projection | Legacy candidate |
| `data.items[].author.id` | int64 | `users.id` | Join by discussion.user_id | Legacy candidate |
| `data.items[].author.full_name` | string | `users.full_name` | Direct mapping | Legacy candidate |
| `data.items[].author.avatar_url` | uri? | `users.avatar_url` | Omit if null | Legacy candidate |
| `data.items[].status` | `DiscussionStatus` | `discussions.status` | Return stored string | Legacy nullable; null fails projection |
| `data.items[].comments` | `DiscussionComment[]` | Queue summary | Always empty array | `DERIVED` |
| `data.pagination` | `PageMeta` | Local page policy | Page 1 default, size 20 | `DERIVED` |
| `data.pagination.page` | int32 | Request/default | Requested positive page or 1 | `DERIVED` |
| `data.pagination.size` | int32 | Local constant | 20 | `DERIVED` |
| `data.pagination.total` | int64 | `COUNT(DISTINCT d.id)` | Same active reports/filters | `DERIVED` |
| `data.pagination.total_pages` | int32 | `ceil(total / 20)` | 0 when total is 0 | `DERIVED` |
| `meta` | object | Envelope | No endpoint-specific fields defined | DIRECT type |
| `traceId` | uuid | Request trace | Propagate trace ID | Envelope convention |

## Error mapping

| Condition | HTTP/business code | Basis/status |
|---|---|---|
| Missing/invalid Bearer JWT | 401 `DESIGN_AUTHENTICATION_REQUIRED` | Catalog direct |
| Authenticated non-Admin | 403 `DESIGN_ACCESS_DENIED` | Catalog direct; shared `ADMIN` guard |
| Query/data retrieval or required-field mapping failure | 500 `DESIGN_INTERNAL_ERROR` | Catalog direct; exact internal branch unspecified |
| Invalid page parse/range | 422 `DESIGN_VALIDATION_ERROR` | Local `DERIVED` fallback; absent from catalog |
| No matching reported rows | 200 `DESIGN_RESOURCE_RETRIEVED` | Empty `items`, total_pages 0 |

## Runtime and envelope discrepancy

API #97 is wired and its static route is in `DESIGN_CONTRACT_PATHS`; raw query values let ADMIN authorization run before page validation. `error_response` emits `data:null`, matching the API guideline. Migration deployment and live schema remain unverified.

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
