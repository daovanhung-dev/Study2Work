---
title: "Data Mapping"
order: 5
dd_id: "65"
api_name: "Lấy tiến độ toàn lớp"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Response Source Matrix — contract trực tiếp

| Response field | Contract type | Candidate source | Mapping/null rule | Evidence |
|---|---|---|---|---|
| success | boolean | Envelope success branch | true trên success; false trên error | Shared envelope; local HTTP tests. |
| businessCode | string | Catalog | Success literal DESIGN_RESOURCE_RETRIEVED | DIRECT. |
| message | string | Application message | `Course progress retrieved.` hoặc `No students found.` | Local runtime; message wording is not direct catalog data. |
| data.items[] | Course[] | Catalog reusable Course | Giữ nguyên kiểu trực tiếp | DIRECT; lệch intent AC-26. |
| items[].id | int64 | Legacy candidate courses.id | Course ID, không phải learner ID | Candidate only; live schema chưa xác minh. |
| items[].title | string | Legacy candidate courses.name | name → title | Candidate mapping; chưa giải quyết progress. |
| items[].description | string? | courses.description | Giữ optional/null policy cần xác nhận | Legacy candidate. |
| items[].thumbnail_url | uri? | courses.thumbnail_url | Giữ optional/null policy cần xác nhận | Legacy candidate. |
| items[].price | decimal-string | courses.price | Serialize decimal theo string | Candidate; decimal precision/currency chưa chốt ở đây. |
| items[].status | CourseStatus | courses.status | Trả enum được lưu | Enum members/schema deployment chưa xác nhận. |
| items[].mentor | UserSummary | Course owner relation | id, full_name, avatar_url? | Candidate; JWT/mentor identity mapping unresolved. |
| items[].category | Category? | Không có relation được phê duyệt | Không tự thêm join hay fabricate object | SOURCE_REQUIRED. |
| data.pagination | PageMeta | Request/roster query | page, size, total, total_pages | Schema direct; API không khai báo pagination inputs. |
| meta | object | Envelope | Empty object từ shared success helper | Local HTTP tests. |
| traceId | uuid | Request trace context | Propagate current trace | Shared convention; local HTTP test. |

## Query Matrix — candidate legacy mapping

`query.py` hiện có hai SQL constants. Đây là local legacy BIGINT mapping; checked-in DDL không chứng minh live schema.

| Query | Type | Candidate relation/columns | Predicate/join | Group/order | Evidence/status |
|---|---|---|---|---|---|
| Q1 | SELECT | courses.id, courses.mentor_id | id=:course_id | One owner row | Local direct-owner check uses API #62 pattern; DERIVED. |
| Q2 | SELECT | enrollments.course_id, enrollments.user_id, users.id/full_name/avatar_url/role | Join course and user; course_id=:course_id, mentor_id=:mentor_id, status ACTIVE, role STUDENT | DISTINCT user; order by user ID | Local SQL; active/role/owner mapping DERIVED from API #62. |
| Q3 | SELECT | lessons.id, lessons.course_id, lessons.status | Course match; status PUBLISHED | Denominator count | Local SQL; DERIVED from API #9. |
| Q4 | SELECT | lesson_progress.id, user_id, lesson_id, status, progress_percent, last_accessed_at | Join only to Q3 published lessons | DISTINCT ON pair; latest last_accessed_at DESC NULLS LAST, id DESC | Local SQL; duplicate resolution DERIVED because DDL has no unique pair. |
| Q5 | SELECT | progress status/percent by student | One chosen row per learner/published lesson; missing row becomes zero | completed count, percent sum, invalid status/range count | Local SQL/view; invalid state returns safe 500. |

## Local aggregation — DERIVED

- Learner set: distinct user IDs reached through `ACTIVE` enrollments for the requested course where `users.role='STUDENT'`.
- total_lessons: count of course lessons with status='PUBLISHED'.
- For duplicate progress rows, select the latest by `last_accessed_at DESC NULLS LAST`, then `id DESC`.
- completed_lessons: count selected rows with status `COMPLETED` within the published denominator.
- progress_percent: floor of sum of each selected progress percent, treating missing row/NULL percent as zero, divided by total_lessons; if there are no published lessons, return zero.
- Selected status outside `NOT_STARTED`, `IN_PROGRESS`, `COMPLETED`, or non-NULL percent outside 0..100 is treated as invalid stored projection and returns safe 500. Legacy DDL does not enforce these checks.
- A course with no learners returns an empty items list. The one-page metadata uses page=1, size=total=items count, total_pages=1 when nonempty and 0 when empty.
- These are local DERIVED fallbacks. Legacy DDL is candidate only; live schema, enum policy and business approval remain unverified.

## Local response mapping — not the catalog contract

| Candidate field | Type | Candidate source/transform | Status |
|---|---|---|---|
| student | UserSummary | users reached through active Student enrollment | DERIVED from API #62; direct Course schema has no student member. |
| completed_lessons | int32 | Count latest selected COMPLETED rows within denominator | DERIVED local status rule. |
| total_lessons | int32 | Published lesson count | DERIVED from API #9 visibility. |
| progress_percent | int32 | floor(progress_sum / total_lessons), bounded 0..100 | DERIVED local formula; 0 for empty denominator. |

## Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | GET is read-only | No INSERT/UPDATE/DELETE | N/A — READ-ONLY API |

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
