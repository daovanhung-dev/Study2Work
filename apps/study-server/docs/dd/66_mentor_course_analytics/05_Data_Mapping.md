---
title: "Data Mapping"
order: 5
dd_id: "66"
api_name: "Lấy analytics tổng hợp"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Response Source Matrix — contract trực tiếp

| Response field | Contract type | Candidate source | Mapping/null rule | Evidence |
|---|---|---|---|---|
| success | boolean | Envelope branch | true khi thành công; false khi lỗi | Reusable schema; endpoint UNWIRED. |
| businessCode | string | Catalog | Success literal DESIGN_RESOURCE_RETRIEVED | DIRECT. |
| message | string | Application message | Exact text chưa được quy định | SOURCE_REQUIRED. |
| data.items[] | Course[] | Catalog reusable Course | Giữ nguyên direct type | DIRECT; không chứa event metric. |
| items[].id | int64 | Legacy candidate courses.id | Course ID scoped bởi path | Candidate; live schema chưa xác minh. |
| items[].title | string | Legacy candidate courses.name | name sang title | Candidate mapping; không liên quan event measure. |
| items[].description | string? | courses.description | Optional/null policy cần xác nhận | Legacy candidate. |
| items[].thumbnail_url | uri? | courses.thumbnail_url | Optional/null policy cần xác nhận | Legacy candidate. |
| items[].price | decimal-string | courses.price | Serialize dạng decimal string | Candidate; currency/precision không được API #66 nêu. |
| items[].status | CourseStatus | courses.status | Trả enum đã lưu nếu schema được chọn | Enum members chưa xác nhận. |
| items[].mentor | UserSummary | Candidate owner relation qua courses.mentor_id và users | id, full_name, avatar_url tùy chọn | Candidate; identity/owner join chưa được duyệt. |
| items[].category | Category? | Không có relation được phê duyệt | Không tự thêm join/object | SOURCE_REQUIRED. |
| data.pagination | PageMeta | Catalog reusable Page | page, size, total, total_pages | DIRECT schema; request không khai báo page/size. |
| meta | object | Envelope convention | Empty object chỉ là ví dụ | Runtime behavior chưa xác minh cho #66. |
| traceId | uuid | Request trace | Propagate request trace | Shared convention; route absent. |

## Query Matrix

| Query ID | Operation | Relation/columns | Predicate/group | Result/branch | Status |
|---|---|---|---|---|---|
| Q1 | SELECT candidate | Legacy candidate courses.id, courses.mentor_id | Course ID match; direct owner candidate | Existing/missing/access branch | DERIVED; principal mapping and live schema unresolved. |
| Q2 | Aggregate concept | No approved learning-event relation or columns | Conceptually scoped to course; no physical SQL specified | Candidate metrics only | SOURCE_REQUIRED; reviewed schemas do not provide a learning-event ledger. |

Do not use lesson_progress or progress_snapshots as event history. Do not use audit_events or outbox_events without an approved domain mapping.

## Candidate analytics mapping — DERIVED, not wire contract

| Candidate field | Type | Logical source needed | Candidate rule | Gap |
|---|---|---|---|---|
| total_learning_events | int64 | Approved event record for course | Count qualifying learning events from start to current time | Relation, event definition, dedup key and retention SOURCE_REQUIRED. |
| students_with_learning_events | int32 | Event actor linked to Student | Count distinct Student actors with at least one qualifying event | Actor identity/role and assignment mapping SOURCE_REQUIRED. |
| last_activity_at | date-time? | Event occurrence timestamp | Maximum event time; null for zero events | Timestamp field and timezone/precision SOURCE_REQUIRED. |

Candidate item definition is intentionally conceptual. No physical table name, column name, SQL, status enum or index is proposed.

## Candidate aggregation decisions to review

- Scope: all-time-to-date because API #66 declares no from/to query; DERIVED.
- Empty event set: counts are zero and last_activity_at is null; DERIVED.
- Duplicates/retries: deduplication rule is not defined; SOURCE_REQUIRED.
- Event taxonomy: only approved learner activity may count; exact event names are SOURCE_REQUIRED.
- Snapshot/cache and freshness are unspecified; do not infer either.

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
