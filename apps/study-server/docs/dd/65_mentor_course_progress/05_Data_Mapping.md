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
| success | boolean | Envelope success branch | true trên success; false trên error | Schema/convention; endpoint UNWIRED. |
| businessCode | string | Catalog | Success literal DESIGN_RESOURCE_RETRIEVED | DIRECT. |
| message | string | Application message | Exact text chưa được quy định | SOURCE_REQUIRED. |
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
| meta | object | Envelope | Empty object chỉ là candidate convention | Current response helper cần kiểm chứng khi wired. |
| traceId | uuid | Request trace context | Propagate current trace | Shared convention; endpoint absent. |

## Query Matrix — candidate legacy mapping

Các query dưới đây là sơ đồ đọc đề xuất, không phải SQL đã triển khai hay live-schema contract.

| Query | Type | Candidate relation/columns | Predicate/join | Group/order | Evidence/status |
|---|---|---|---|---|---|
| Q1 | SELECT | courses.id, courses.mentor_id | id=:course_id; candidate owner mentor_id=:mentor_id | N/A | Legacy schema candidate; access rule DERIVED. |
| Q2 | SELECT | enrollments.course_id, enrollments.user_id | course_id=:course_id; no status filter | One distinct learner per user ID | AC-26 says enrollment aggregate; enrollment status and duplicate policy SOURCE_REQUIRED. |
| Q3 | SELECT | users.id, users.full_name, users.avatar_url | Join user by enrollment user ID | Candidate stable order by name, then ID | UserSummary mapping candidate; role/deleted-row policy unresolved. |
| Q4 | SELECT | lessons.id, lessons.course_id, lessons.status | Course match; candidate status PUBLISHED | Count published lessons | DERIVED from API #9; denominator policy needs approval. |
| Q5 | SELECT | lesson_progress.user_id, lesson_id, status, progress_percent | Left join by learner and lesson | Aggregate once per learner | Legacy DDL candidate; uniqueness/enums/live state unverified. |

## Candidate aggregation — DERIVED

- Learner set: unique enrollment user_id values for the requested course; no status filter until approved.
- total_lessons: count of course lessons with status='PUBLISHED'.
- completed_lessons: count in that lesson set whose progress row has status='COMPLETED'.
- progress_percent: floor of sum of each lesson progress percent, treating missing progress as zero, divided by total_lessons; if there are no published lessons, return zero.
- A course with no learners returns an empty items list. The single-page metadata proposal uses page=1, size=0, total=0, total_pages=0.
- These are DERIVED proposals; table names, enum values, null policy and formula require confirmation against the selected live schema and business owner.

## Candidate response mapping — not the catalog contract

| Candidate field | Type | Candidate source/transform | Status |
|---|---|---|---|
| student | UserSummary | users reached through enrollment | DERIVED; direct Course schema has no student member. |
| completed_lessons | int32 | Count completed lesson progress within denominator | DERIVED; status rule unapproved. |
| total_lessons | int32 | Published lesson count | DERIVED from API #9 visibility. |
| progress_percent | int32 | Floor average across denominator | DERIVED; formula unapproved. |

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
