---
title: "Data Mapping"
order: 5
dd_id: "101"
api_name: "Lấy KPI tổng quan"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

```text
Admin Bearer principal -> authorize report access -> parse optional date bounds -> derive effective period -> Q1 users count + Q2 courses count + Q3 enrollments count + Q4 discussions count -> map four candidate ImpactMetric records + Report period/generated_at -> 200 DESIGN_RESOURCE_RETRIEVED or exact 401/403/500 catalog errors -> AC-38 continues to #102 or #103
```

## 0. Xác thực và quyền

- Đọc Bearer JWT từ `Authorization` theo contract.
- Yêu cầu Admin/report permission theo catalog và AC-38.
- Current Study helper chỉ có Student guard; Admin claim/policy là `SOURCE_REQUIRED`.
- Không nhận role, user ID hoặc scope từ query.

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Admin principal | JWT claims/role | Admin | Contract DIRECT; claim/policy source chưa có |

## 1. Validate request và xác định period

- `from`: optional calendar date theo catalog.
- `to`: optional calendar date theo catalog.
- Không có body/path parameter.
- Proposed effective window: cả hai bound có thì dùng inclusive; không có bound thì 30 ngày gần nhất đến hôm nay; chỉ có `from` thì `from` đến hôm nay; chỉ có `to` thì 30 ngày kết thúc tại `to`.
- `from > to`, date parse failure, maximum span và timezone convention chưa có error mapping được duyệt; catalog #101 không khai báo 422.

## 2. Aggregate candidate metrics

Các query độc lập để không làm nhân bản row do join giữa các domain. Đây là `DERIVED` MVP proposal, chưa phải SQL runtime đã kiểm chứng.

### Q1 — User records created

| Thuộc tính | Candidate mapping |
|---|---|
| Base table | Legacy `users` |
| Selected value | `COUNT(*)` |
| Date column | `users.created_at` |
| Predicate | `DATE(users.created_at) BETWEEN :effective_from AND :effective_to` |
| Population | Tất cả role/status; không lọc |
| Result key | `user_records_created` |
| Empty source | `0`, serialize thành `"0"` |
| Basis | Metric/filters DERIVED; timestamp column có trong legacy DDL |

### Q2 — Course records created

| Thuộc tính | Candidate mapping |
|---|---|
| Base table | Legacy `courses` |
| Selected value | `COUNT(*)` |
| Date column | `courses.created_at` |
| Predicate | `DATE(courses.created_at) BETWEEN :effective_from AND :effective_to` |
| Population | Tất cả status; không lọc |
| Result key | `course_records_created` |
| Empty source | `0`, serialize thành `"0"` |
| Basis | Metric/filters DERIVED; timestamp column có trong legacy DDL |

### Q3 — Enrollment records created

| Thuộc tính | Candidate mapping |
|---|---|
| Base table | Legacy `enrollments` |
| Selected value | `COUNT(*)` |
| Date column | `enrollments.enrolled_at` |
| Predicate | `DATE(enrollments.enrolled_at) BETWEEN :effective_from AND :effective_to` |
| Population | Tất cả status; mỗi row là một record, không deduplicate user/course |
| Result key | `enrollment_records_created` |
| Empty source | `0`, serialize thành `"0"` |
| Basis | Metric/filters DERIVED; `enrolled_at` có trong legacy DDL |

### Q4 — Discussion records created

| Thuộc tính | Candidate mapping |
|---|---|
| Base table | Legacy `discussions` |
| Selected value | `COUNT(*)` |
| Date column | `discussions.created_at` |
| Predicate | `DATE(discussions.created_at) BETWEEN :effective_from AND :effective_to` |
| Population | Topic và reply rows; không lọc status/parent |
| Result key | `discussion_records_created` |
| Empty source | `0`, serialize thành `"0"` |
| Basis | Metric/filters DERIVED; `created_at` có trong legacy DDL |

### Q5 — Pilot report snapshot alternative

- Pilot `report_snapshots` có `report_code`, `period_start`, `period_end`, `dimension_hash`, `dimensions`, `metrics`, `source_high_watermark`, `calculation_version`, `generated_at`.
- Không viết query executable vì code, period alignment, dimension policy, metric JSON schema/version và live availability chưa được xác định.
- Không map pilot UUID `id` thành domain ID, và không coi table này là runtime writer/source chỉ vì DDL tồn tại.

## 3. Build `Report`

| Response field | Candidate source/transform | Status |
|---|---|---|
| `period.from` | `effective_from` | Field DIRECT; date default DERIVED |
| `period.to` | `effective_to` | Field DIRECT; date default DERIVED |
| `metrics[].key` | Four proposed stable keys | DERIVED |
| `metrics[].value` | Independent `COUNT(*)` → decimal string | Type DIRECT; formula DERIVED |
| `metrics[].label` | Vietnamese display label | DIRECT type; label DERIVED |
| `generated_at` | Clock at report assembly | Field DIRECT; UTC source DERIVED |
| `businessCode` | Catalog literal | DIRECT `DESIGN_RESOURCE_RETRIEVED` |
| `traceId` | Request trace context | Common API guideline |

## 4. Error branches

- 401 `DESIGN_AUTHENTICATION_REQUIRED` — Bearer authentication failure per catalog contract.
- 403 `DESIGN_ACCESS_DENIED` — Admin/report permission failure per catalog contract.
- 500 `DESIGN_INTERNAL_ERROR` — unexpected report/query failure per catalog contract.
- Date parse/reversed range handling is unresolved; do not add an undocumented status or business code.
- Chi tiết xem [06_Error.md](./06_Error.md).

## 5. Mutation and consistency

- API #101 is read-only; it does not INSERT or UPDATE `report_snapshots`.
- Four independent aggregates may observe different commits unless they share a consistent DB snapshot; transaction/isolation rule is `SOURCE_REQUIRED`.
- Cache/freshness, retry, maximum date span and metric calculation version are not specified.

## Request Usage Matrix

| Request item | Source | Use | Rule/status |
|---|---|---|---|
| `Authorization` | Bearer JWT header | Authenticate Admin | DIRECT requirement; guard SOURCE_REQUIRED |
| `from` | Optional query date | Effective lower bound for Q1–Q4 | DIRECT field; default DERIVED |
| `to` | Optional query date | Effective upper bound for Q1–Q4 | DIRECT field; default DERIVED |
| Body | None | No use | DIRECT |

## Query Matrix

| Query ID | Type | Base table | Column/result | Filter | Purpose/status |
|---|---|---|---|---|---|
| Q1 | SELECT COUNT | `users` | `created_at`, count | Effective date range | Candidate registration-record KPI; DERIVED |
| Q2 | SELECT COUNT | `courses` | `created_at`, count | Effective date range | Candidate course-record KPI; DERIVED |
| Q3 | SELECT COUNT | `enrollments` | `enrolled_at`, count | Effective date range | Candidate enrollment-record KPI; DERIVED |
| Q4 | SELECT COUNT | `discussions` | `created_at`, count | Effective date range | Candidate discussion-record KPI; includes replies; DERIVED |
| Q5 | SELECT candidate | Pilot `report_snapshots` | `report_code`, period, dimensions, metrics, generated_at | No approved selector/mapping | Alternative only; SOURCE_REQUIRED |

## Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Audit | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|
| — | None | N/A | Read-only API | No writes | N/A | N/A | Read consistency TBD | Exact 401/403/500 catalog codes |

## Response Source Matrix

| Response field | Type | Source type | Table/column or generator | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|
| `success` | boolean | Envelope | Response branch | `true` on success | Non-null | Shared convention |
| `businessCode` | string | Catalog | N/A | Fixed `DESIGN_RESOURCE_RETRIEVED` | Non-null | DIRECT |
| `message` | string | Application | N/A | Safe message | Non-null | Exact text unspecified |
| `data.period.from` | date | Query/default | `from` or effective-range rule | Effective lower date | Non-null | Default DERIVED |
| `data.period.to` | date | Query/default | `to` or effective-range rule | Effective upper date | Non-null | Default DERIVED |
| `data.metrics[].key` | string | Derived label | Candidate metric key | Stable string | Non-null | Key list DERIVED |
| `data.metrics[].value` | decimal-string | Aggregate | Q1–Q4 COUNT | Decimal string | `"0"` for empty source proposal | Formula DERIVED |
| `data.metrics[].label` | string | Derived label | Vietnamese display text | Plain label | Non-null | Label DERIVED |
| `data.generated_at` | date-time | Clock | Report assembly time | ISO-8601 UTC proposal | Non-null | Clock policy DERIVED |
| `meta` | object | Envelope | N/A | Empty object candidate | Non-null | Endpoint metadata unspecified |
| `traceId` | uuid | Request context | Trace helper | Propagate request trace | Non-null | Common guideline |
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
