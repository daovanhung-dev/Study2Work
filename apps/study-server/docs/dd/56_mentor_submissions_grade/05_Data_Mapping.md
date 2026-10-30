---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "56"
api_name: "Lưu điểm bài làm Mentor"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
0. Authenticate Bearer JWT and require explicit MENTOR role
1. Parse signed-int64 submission_id and validate strict score/rubric_items body
2. Lock submission row and LEFT JOIN assignment/course candidate relations
3. Missing submission or malformed path -> catalog 404; broken required relation -> catalog 500
4. Check direct courses.mentor_id owner; mismatch -> catalog 403
5. Validate DERIVED score range [0, assignments.max_score]; invalid -> catalog 422
6. UPDATE assignment_submissions.score/status, preserving feedback
7. Resolve zero/one UploadAsset by exact URL + owner + SUBMISSION purpose + course
8. Validate Submission response projection, then commit
9. Return 200 DESIGN_RESOURCE_UPDATED; API #57 separately owns feedback
~~~

Current source implements this flow. The query/table relations and score rule use the checked-in legacy DDL as a candidate; no live schema or deployment verification is claimed. rubric_items is accepted but not interpreted, persisted, or echoed.

## Request Usage Matrix

| Request item | Source | Validation | Use | Status |
|---|---|---|---|---|
| Authorization | Header | Bearer JWT; explicit MENTOR role | Numeric JWT subject for direct-owner predicate | Guard source-backed; ownership mapping DERIVED |
| submission_id | Path | Signed int64 parser | Submission lock/update key | DIRECT type; malformed/overflow → 404 fallback |
| score | Body | Strict int32, then [0, max_score] | NUMERIC(6,2) update and response | Type DIRECT; range DERIVED |
| rubric_items | Body | Required strict string | No persistence or response mapping | Key spelling/opaque handling DERIVED; storage unresolved |
| Query parameters | None | N/A | None | Catalog has no query fields |
| Additional body fields | None | Rejected | None | Request model forbids extras |

## 0. Check quyền

The shared request guard authenticates Bearer and enforces MENTOR before path parsing or DB access. The handler checks the locked row's course.mentor_id against the numeric subject, then the UPDATE repeats the owner predicate to guard against an ownership change. A different owner returns 403 without exposing Submission fields. Assigned-Mentor access is not represented.

## 1. Validate data input

- submission_id must parse as signed int64; malformed or overflow maps to 404 DESIGN_RESOURCE_NOT_FOUND.
- score must be a strict JSON int32; body-shape/type errors map to 422 DESIGN_VALIDATION_ERROR.
- DERIVED fallback requires 0 <= score <= assignments.max_score. A null, malformed or negative max_score projection maps to safe 500 because it cannot support the candidate operation.
- rubric_items must be a strict string. It is opaque input and is currently discarded due to absent persistence schema.
- No current-status precondition is enforced; repeated grading is allowed by current fallback. The catalog declares no 409 trigger.

## 2. Read and lock

LOCK_MENTOR_SUBMISSION_FOR_GRADE selects the submission and LEFT JOINs assignment/course, with FOR UPDATE OF s. The handler validates positive BIGINT-era IDs and matching joined keys before authorization. Missing row maps to 404; null/orphan required relations map to 500.

Read columns are assignment_submissions.id, assignment_id, user_id, content, file_url, submitted_at, score, feedback and status; assignments.id, course_id, max_score; courses.id and mentor_id.

## 3. Update

UPDATE_MENTOR_SUBMISSION_GRADE writes only score and status='GRADED', casts score to NUMERIC(6,2), filters by submission and assignment, and repeats direct-owner scope through EXISTS. RETURNING supplies the response row. feedback is unchanged.

## 4. Resolve response and transaction

When file_url is non-null, FIND_GRADED_SUBMISSION_UPLOAD matches uploads.url exactly with owner_id=user_id, purpose='SUBMISSION' and matching course_id; it orders by id ASC and limits to one. No match yields files=[]. This relation is DERIVED and API #35 producer compatibility remains open.

The reusable API #54 SubmissionResponse validates the response. If the update, file projection or response mapping fails, the transaction rolls back. The handler commits only after the complete projection is valid. No live database behavior is established by fake-DB tests.
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
