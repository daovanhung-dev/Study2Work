---
title: "Data Mapping"
order: 5
dd_id: "98"
api_name: "Lấy đầy đủ thread + report detail"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

```text
Admin Bearer principal -> authorize Admin -> parse discussion_id:int64 -> Q1 logical target lookup -> Q2 AC-37 logical report detail (physical source and response field absent) -> Q3 candidate direct-child comments/author projection -> one-item Page<Discussion> proposal -> 200 DESIGN_RESOURCE_RETRIEVED or exact 401/403/404/500 errors -> UI decides #99/#100
```

## Mục lục

- [0. Check quyền](#step-0-check-quyen)
- [1. Validate request](#step-1-validate-request)
- [2. Đọc thread và reports](#step-2-doc-thread-va-reports)
- [3. Mutation](#step-3-mutation)
- [4. Response mapping](#step-4-response-mapping)
- [Request Usage Matrix](#request-usage-matrix)
- [Query Matrix](#query-matrix)
- [Mutation Matrix](#mutation-matrix)
- [Response Source Matrix](#response-source-matrix)

<a id="step-0-check-quyen"></a>
## 0. Check quyền

- Xác thực Bearer JWT trước khi đọc discussion/comments/reports.
- Yêu cầu Admin role theo catalog. Current `validate_current_user_request` chỉ authorize Student; không tái sử dụng cho #98.
- Admin claim shape, principal mapping, scope/tenant rule và guard chưa có source trong Study; giữ `SOURCE_REQUIRED`.
- Không lookup discussion/report trước authorization thành công.
- Trả đúng 401/403 catalog codes; concealment/ordering giữa authorization và 404 cần policy xác nhận.

<a id="step-1-validate-request"></a>
## 1. Validate request

- `discussion_id` là path int64 bắt buộc theo catalog.
- Không nhận body, query, report ID hoặc cursor.
- Catalog không khai báo 422. Malformed/overflow path có thể bị framework parse trước handler; future route phải thống nhất mapping với catalog, không tự thêm code.
- `discussion_id` có phải root thread hay có thể là reported reply chưa được AC-37 xác định. API #42 dùng root ID là proposal cho Student reload; không tự coi đó là Admin policy đã duyệt.

<a id="step-2-doc-thread-va-reports"></a>
## 2. Đọc thread và reports

### 2.1. Q1 — logical report target and discussion

AC-37 diagram node n5 nói đọc `discussion/comments/reports`. Q1 đọc logical target discussion theo path ID; physical report-to-discussion relation chưa có nguồn.

| Logical item | Candidate use | Rule/status |
|---|---|---|
| `discussion_id` | Identify selected target | DIRECT path; relation to report source unresolved |
| Report detail | Show why/reporter/severity/state | AC-37 logical requirement; physical relation and response fields `SOURCE_REQUIRED` |
| Discussion | Build `Discussion` | Catalog shape direct; legacy projection incomplete due title and nullable FKs |
| Root/thread relation | Resolve full context | `parent_id` supports self-reference; root-vs-reply target semantics `DERIVED`/confirmation required |

### 2.2. Q1a — candidate legacy discussion row (not approved SQL)

| Candidate field | Response use | Evidence/status |
|---|---|---|
| `discussions.id` | `Discussion.id` | Legacy DDL candidate |
| `discussions.course_id` | `Discussion.course_id` | Nullable in DDL, required in contract |
| `discussions.user_id` | Author join | Nullable in DDL, author required |
| `discussions.parent_id` | Root/reply relationship | Nullable self-FK; row interpretation unresolved |
| `discussions.content` | `Discussion.content` | TEXT NOT NULL candidate |
| `discussions.status` | `Discussion.status` | `VARCHAR(20)` default ACTIVE; enum and Admin visibility unresolved |
| `created_at`, `updated_at` | Candidate context/ordering | Timestamp without timezone in legacy DDL |
| `title` | `Discussion.title` | Missing; do not derive from content |

No status `ACTIVE` predicate is copied from Student API #42: an Admin moderation detail may need to inspect hidden/locked rows. Which statuses/children are eligible remains `SOURCE_REQUIRED`.

### 2.3. Q2 — reports

AC-37 directly requires reading report detail. No discussion report table, key, or report columns are defined in legacy Study DDL or DB guide. The reusable analytics `Report` (`period`, `metrics`, `generated_at`) belongs to AC-38 and is not a discussion report. Do not write SQL against guessed `reports`/`discussion_reports`; do not add `reason`, `severity`, reporter, counts or timestamps to `Discussion`.

This query is not implementable against source-backed physical schema and its result cannot be represented by current `Page<Discussion>`. Keep it as `SOURCE_REQUIRED`/`DISCREPANCY` until the report schema or API response contract is approved.

### 2.4. Q3 — candidate comments and authors

API #42 proposes a root Discussion with direct child comments ordered `created_at ASC, id ASC`, wrapped in a one-item Page. This endpoint is Admin moderation, so do not inherit #42's Student enrollment gate or `ACTIVE` status filter.

- Candidate root lookup: `discussions.id = :discussion_id`; root-only (`parent_id IS NULL`) is a `DERIVED` proposal, not direct contract.
- Candidate comments: `child.parent_id = root.id`; direct children only; nested children, report-target replies and parent-context expansion need confirmation.
- Candidate order: `child.created_at ASC, child.id ASC` for stable chronological display (`DERIVED` from #42).
- Do not silently drop rows whose required author/course relation is missing; response mapping needs an approved integrity policy.

### 2.5. Q4 — one-item Page proposal

`PageMeta` requires page, size, total, total_pages while #98 has only a path ID. Proposal: one Discussion in `items`, `page=1`, `size=1`, `total=1`, `total_pages=1` when found. This follows #42's same response pattern, is marked `DERIVED`, and does not resolve report count/grain because report rows are not in the response.

<a id="step-3-mutation"></a>
## 3. Mutation

API #98 is read-only. It does not dismiss/resolve a report, update Discussion status, moderate, delete, or write audit. Those choices belong to later #99/#100 branches in AC-37.

<a id="step-4-response-mapping"></a>
## 4. Response mapping

- Preserve exact `ApiEnvelope<Page<Discussion>>`; no `Report` object/fields are cataloged for #98.
- Candidate one-item Page is explicitly `DERIVED`.
- `Discussion.title` has no source; never alias `content` to `title`.
- `course_id` and `author` are required by schema but legacy FKs are nullable.
- Admin detail must not filter out hidden/locked state solely because Student #42 proposes `ACTIVE` visibility.
- Nested comments are direct children only in the proposal; root/reply and recursive thread behavior remain open.

## Request Usage Matrix

| Request item | Source/use | Query/response use | Status |
|---|---|---|---|
| Authorization | Bearer header | Authenticate/authorize Admin | Role direct; Study implementation `SOURCE_REQUIRED` |
| `discussion_id` | Required int64 path | Q1 logical target lookup | Type direct; target root/reply semantics unresolved |
| Body/query | None | None | DIRECT |

## Query Matrix

| Query | Operation | Relation/fields | Purpose | Status |
|---|---|---|---|---|
| Q1 | Logical SELECT | Discussion by path ID; physical key candidate `discussions.id` | Load selected target | `DERIVED` candidate; missing title/nullable FKs |
| Q2 | Logical SELECT | Report relation, key, fields and predicates unknown | AC-37 report detail | `SOURCE_REQUIRED`; no guessed SQL |
| Q3 | Candidate SELECT | Child discussions by `parent_id`; candidate users author join | Thread comments | `DERIVED` from #42; Admin status/root policy unresolved |
| Q4 | Candidate Page metadata | One target Discussion | `page=1,size=1,total=1,total_pages=1` when found | `DERIVED` from #42 |

## Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | Read-only GET | No INSERT/UPDATE/DELETE/audit | `N/A — READ-ONLY API` |

## Response Source Matrix

| Response field | Type | Candidate source | Mapping/null rule | Evidence status |
|---|---|---|---|---|
| `success` | boolean | Envelope | true on success | DIRECT convention |
| `businessCode` | string | Catalog | `DESIGN_RESOURCE_RETRIEVED` | DIRECT |
| `message` | string | Application | Safe message | Exact wording unspecified |
| `data` | `Page<Discussion>` | Logical Q1 | One-item page candidate | DIRECT shape; `DERIVED` values |
| `data.items` | `Discussion[]` | Logical Q1 | One target candidate | DIRECT shape |
| `data.items[].id` | int64 | `discussions.id` | Direct candidate | Legacy only |
| `data.items[].course_id` | int64 | `discussions.course_id` | Required; DDL nullable | Discrepancy |
| `data.items[].title` | string | No source | Do not derive from content | `SOURCE_REQUIRED` |
| `data.items[].content` | string | `discussions.content` | Preserve text | Legacy candidate |
| `data.items[].author` | `UserSummary` | `discussions.user_id` → `users` | Required join | Nullable FK/identity unresolved |
| `data.items[].author.id` | int64 | `users.id` | Candidate direct mapping | Legacy candidate |
| `data.items[].author.full_name` | string | `users.full_name` | Candidate direct mapping | Legacy candidate |
| `data.items[].author.avatar_url` | uri? | `users.avatar_url` | Omit if null | Legacy candidate |
| `data.items[].status` | `DiscussionStatus` | `discussions.status` | Preserve only approved token; no ACTIVE filter | Enum unresolved |
| `data.items[].comments` | `DiscussionComment[]` | Child discussions | Direct children in proposal | `DERIVED`; full thread extent unresolved |
| `data.items[].comments[].id` | int64 | Child `discussions.id` | Candidate direct mapping | Legacy only |
| `data.items[].comments[].discussion_id` | int64 | Child `parent_id` | Candidate parent mapping | Legacy nullable |
| `data.items[].comments[].content` | string | Child `discussions.content` | Preserve text | Legacy candidate |
| `data.items[].comments[].author` | `UserSummary` | Child `user_id` → `users` | Required join | Missing author policy unresolved |
| `data.items[].comments[].author.id` | int64 | `users.id` | Candidate direct mapping | Legacy candidate |
| `data.items[].comments[].author.full_name` | string | `users.full_name` | Candidate direct mapping | Legacy candidate |
| `data.items[].comments[].author.avatar_url` | uri? | `users.avatar_url` | Omit if null | Legacy candidate |
| `data.items[].comments[].created_at` | date-time | Child `discussions.created_at` | Serialize using approved timezone convention | DDL timezone absent |
| `data.pagination` | `PageMeta` | One-item proposal | Values are `DERIVED` | Not approved |
| `data.pagination.page` | int32 | One-item proposal | 1 | `DERIVED` |
| `data.pagination.size` | int32 | One-item proposal | 1 | `DERIVED` |
| `data.pagination.total` | int64 | One Discussion proposal | 1 if target exists | `DERIVED` |
| `data.pagination.total_pages` | int32 | One-item proposal | 1 | `DERIVED` |
| `meta` | object | Envelope | No endpoint-specific fields defined | DIRECT type |
| `traceId` | uuid | Request trace | Propagate current trace | Envelope convention |
| Report details | Not in response schema | No approved report source | Must not add fields | `DISCREPANCY / SOURCE_REQUIRED` |

## Error mapping

| Condition | HTTP/business code | Basis/status |
|---|---|---|
| Missing/invalid Bearer/JWT | 401 `DESIGN_AUTHENTICATION_REQUIRED` | Catalog direct |
| Authenticated non-Admin | 403 `DESIGN_ACCESS_DENIED` | Catalog direct; guard absent |
| Discussion not found | 404 `DESIGN_RESOURCE_NOT_FOUND` | Catalog direct; row-missing mapping candidate |
| ID refers to non-root/reply | Not separately defined | Root-only 404 is `DERIVED`; confirmation required |
| Query/required response mapping failure | 500 `DESIGN_INTERNAL_ERROR` | Catalog direct; exact internal branches unspecified |
| Malformed/overflow path ID | No catalog code | `SOURCE_REQUIRED`; do not add 422 |

## Runtime/envelope discrepancy

API #98 is absent. Current middleware allowlist does not contain this path; generic validation/unhandled handlers would use fallback business codes if wired without update. Current `error_response` emits `{}` for absent error data while shared API guidelines specify `null`. This is conditional future integration discrepancy, not current #98 runtime behavior.

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
