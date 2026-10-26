---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "47"
api_name: "Tạo lecture"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
0. Validate Mentor Bearer JWT.
1. Validate path/body types and ranges; parse asset_refs JSON string into an ordered int64 ID array; allow [], reject duplicates and invalid values.
2. Read course by path ID; return 404 if missing and 403 unless `courses.mentor_id` equals the authenticated Mentor. Do not filter course status.
3. Resolve every non-empty asset ID from uploads where owner is the same Mentor, purpose is LECTURE and course_id matches path; any unresolved ID returns the same 404.
4. Insert lessons with content as a decimal string, status `PUBLISHED` and database `CURRENT_TIMESTAMP` for both required timestamps.
5. For non-empty asset refs, insert `lesson_uploads` rows in request order in the same transaction; commit and return assets in input order.
~~~

The API route, module and HTTP tests are source-backed. Legacy BIGINT DDL and migration files remain checked-in artifacts; live schema and deployment are not verified.

## Request Usage Matrix

| Request field | Source | Validate | Query/mutation usage | Response usage | Gap |
|---|---|---|---|---|---|
| Authorization | Header | Valid Bearer JWT with Mentor role | Mentor principal is compared with `courses.mentor_id` and filters asset `owner_id` | Not echoed | Direct owner only; no assignment lookup. |
| course_id | Path | Signed int64 | Q1 reads course; Q2 filters uploads; M1 sets lessons.course_id | data.course_id | Legacy BIGINT source; live schema not verified. |
| title | Body | Required string; maximum 200 | M1 sets lessons.name | data.title | No minimum or trim rule. |
| content | Body | Required signed int64 | M1 stores `str(content)` in lessons.content | data.content | Response is the decimal string; semantics are user-approved. |
| asset_refs | Body | JSON text array of unique signed int64 IDs; empty array allowed | Q2 reads uploads with owner/purpose/course predicates | data.assets[] | Any ID not resolved in scope returns generic 404. |
| order | Body | Required signed int32 | M1 sets lessons.sort_order | data.order | No positivity rule. |

## Query Matrix

| Query ID | Mục đích | Type | Base table | Predicate | Order handling | Result / branch |
|---|---|---|---|---|---|---|
| Q1 | Course owner check | SELECT | courses | id = :course_id | N/A | Missing course→404; `mentor_id != current Mentor`→403; no course-status predicate. |
| Q2 | Resolve asset metadata | SELECT | uploads | id in request; owner_id = Mentor; purpose = LECTURE; course_id = path | Rebuild result in original ID order | Empty ID list returns `[]` without query; unresolved IDs→generic 404. |

Q2 must project `id`, `file_name`, `url`, `content_type`, `size_bytes` and `status` from uploads. It must not read client-supplied URL or metadata.

## Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Target column | Value source | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|
| M1 | INSERT | lessons | After auth, request validation, direct course ownership and full asset resolution | course_id, name, content, sort_order, status, created_at, updated_at | Path/request; `str(content)`; fixed `PUBLISHED`; `CURRENT_TIMESTAMP` | 07_lessons_insert.md | Caller-owned transaction; commit after response mapping; rollback on DB/insert/commit failure | Live target schema not verified. |
| M2 | INSERT | lesson_uploads | After lesson row and asset scope checks; only for non-empty refs | lesson_id, upload_id, asset_position | Generated lesson ID; validated IDs and zero-based original order | migration 005 / API #47 view | Same transaction as M1; require every requested ID returned; rollback on mismatch/error | Live migration not verified. |
| M3 | N/A | uploads/resources | API #47 does not mutate upload metadata or legacy resources | N/A | Resolved IDs are read-only | N/A | No asset mutation | Do not create resource rows. |

## Response Source Matrix

| Response field | Type | Source type | Table/column or generator | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|
| data.assets[] | UploadAsset[] | Persisted API #34 metadata | uploads row | Resolve exact ID and rebuild in request order | Empty input → `[]` | Any unresolved ID maps to generic 404. |
| data.assets[].id | int64 | Persisted | uploads.id | Direct | Required per item | API #34 BIGINT artifact; live schema unknown. |
| data.assets[].name | string | Persisted | uploads.file_name | file_name → name | Required per item | API #34 fallback is `upload`. |
| data.assets[].url | uri | Persisted | uploads.url | Direct | Required per item | Public URL from API #34. |
| data.assets[].content_type | string | Persisted | uploads.content_type | Direct | Required per item | API #34 metadata. |
| data.assets[].size_bytes | int64 | Persisted | uploads.size_bytes | Direct | Required per item | API #34 measured bytes. |
| data.assets[].status | UploadStatus | Persisted | uploads.status | Current constant `UPLOADED` | Required per item | Catalog enum fixed for #34. |

## 0. Check quyền

- Decode Mentor principal with `validate_current_user_request(..., role="MENTOR")` before DB access.
- Read course by `courses.id`; require `courses.mentor_id` to match the numeric JWT subject. No assignment relation or course-status filter is used.
- Asset lookup scopes every row by that Mentor principal; never accept owner_id from request.
- Asset purpose must equal `LECTURE`.
- Asset course_id must equal path course_id.
- Preserve request order after lookup; database result order is not the contract.

## 1. Validate data input

- `asset_refs` is a required string containing JSON text whose top-level value is an array.
- Every element must be a signed int64 UploadAsset ID.
- Empty array is allowed and maps to empty `assets`.
- Duplicate IDs are rejected before asset lookup.
- `content:int64` is stored in `lessons.content` as `str(content)` and returned as that decimal string.
- Invalid request types/ranges, malformed JSON, duplicate IDs and title over 200 return 422.
- Missing or cross-scope assets must never be returned as UploadAsset values; all unresolved IDs map to generic 404.

## 2. Check results and map response

- Query uploads only when the parsed ID array is non-empty.
- Require one eligible uploads row for each requested ID under the owner/purpose/course predicates.
- Build an ID-to-row map and emit assets by iterating the original ID array, preserving its order.
- Do not use resources rows for UploadAsset projection.
- Insert each resolved asset ID into `lesson_uploads` with zero-based request position after the lesson INSERT; skip the relation INSERT for an empty array.
- Insert lesson status as `PUBLISHED`; use database `CURRENT_TIMESTAMP` for both `created_at` and `updated_at`.
- Commit lesson and asset links together only after response model construction; rollback if query, INSERT, relation mapping or commit fails.
- Live schema/migration availability remains unverified and keeps this DD in Draft.

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
