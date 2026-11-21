---
title: "Data Mapping"
order: 5
dd_id: "66"
api_name: "Lấy analytics tổng hợp"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Response Source Matrix — local runtime

| Response field | Type | Runtime source | Mapping rule | Status |
|---|---|---|---|---|
| success | boolean | Envelope branch | true khi thành công; false khi lỗi | Shared runtime convention. |
| businessCode | string | Catalog | Success literal DESIGN_RESOURCE_RETRIEVED | DIRECT. |
| message | string | View | Stable success message | Current API #66 source. |
| data.tracked_lesson_accesses | int64 | SQL aggregate | Count mỗi cặp user_id/lesson_id duy nhất có last_accessed_at trên lesson PUBLISHED của course | DERIVED progress-state proxy, không phải event count. |
| data.students_with_activity | int64 | SQL aggregate | Count distinct user_id trong các cặp proxy; users.role phải là STUDENT | DERIVED. |
| data.last_activity_at | datetime? | SQL MAX | MAX last_accessed_at; null khi aggregate rỗng | DERIVED current-state timestamp. |
| meta | object | Shared envelope | Empty object từ helper | Current source behavior. |
| traceId | string | Request trace | Propagate trace ID | Shared runtime convention. |

## Query Matrix

| Query ID | Operation | Relation/columns | Predicate/group | Result/branch | Status |
|---|---|---|---|---|---|
| Q1 | SELECT course owner | courses.id, courses.mentor_id | id = course_id | Missing → 404; owner mismatch → 403 | Legacy DDL-backed local mapping; live schema unverified. |
| Q2 | Aggregate activity proxy | lesson_progress.user_id, lesson_id, last_accessed_at; lessons.id, course_id, status; users.id, role; courses.id, mentor_id | Course owner; lesson PUBLISHED; user role STUDENT; timestamp non-null; GROUP BY user_id, lesson_id | Pair count, distinct Student count, MAX timestamp; empty yields zero/zero/null | DERIVED from checked-in legacy DDL; not learning-event history. |

## Aggregate semantics

- Duplicate progress rows for the same Student/lesson are collapsed by grouping the pair.
- A pair is counted only when at least one current progress row has non-null last_accessed_at.
- The latest available timestamp in the pair is MAX(last_accessed_at).
- Only lessons whose status is PUBLISHED and users whose role is STUDENT are included.
- No active-enrollment predicate is applied; the projection counts Student activity rows still present in progress state.
- The aggregate is all-time over current stored markers; it cannot recover repeated access events overwritten by current-state updates.
- Empty aggregate returns tracked_lesson_accesses=0, students_with_activity=0, last_activity_at=null.

## Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | GET is read-only | No INSERT/UPDATE/DELETE | N/A — READ-ONLY API |

## Source boundary

Legacy DDL provides the queried identifiers and last-access marker. V1-PILOT progress facts/snapshots and generic audit/outbox relations are not read. The API does not claim event-frequency, retry-deduplication, retention, or historical semantics.

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
