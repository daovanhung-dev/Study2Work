---
title: "Data Mapping"
order: 5
dd_id: "102"
api_name: "Lấy dữ liệu tác động cộng đồng"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

```text
Admin Bearer principal -> authorize Admin/report access -> parse optional string dates + segment -> derive effective period -> Q1 distinct enrolled learners + Q2 course completions + Q3 root topics + Q4 replies -> select all/learning/community metrics -> map Report(period, metrics, generated_at) -> 200 DESIGN_RESOURCE_RETRIEVED or exact catalog 401/403/500 -> dashboard filter then optional #103 export
```

## 0. Xác thực và quyền report

- Đọc Bearer JWT theo contract.
- Xác thực Admin và quyền xem analytics/report trước khi chạy query.
- AC-38 yêu cầu Admin có quyền report; current Study helper chỉ có Student guard. Không khẳng định API #102 được secure runtime.

| Principal field | Source/use | Rule/status |
|---|---|---|
| Authorization | Bearer JWT | DIRECT auth requirement |
| Admin role/report permission | Token/policy chưa có source | DIRECT expected behavior; implementation `SOURCE_REQUIRED` |

## 1. Normalize query và hiệu lực kỳ báo cáo

- `from`/`to` là optional string theo catalog. Proposal parse định dạng `YYYY-MM-DD` thành calendar date.
- `segment` optional string; proposal `learning`, `community`; bỏ trống trả đủ metric.
- Dùng cùng effective-range proposal của #101: hai bound đầy đủ inclusive; cả hai thiếu là rolling 30 ngày tới hôm nay; chỉ `from` thì tới hôm nay; chỉ `to` thì 30 ngày kết thúc tại `to`.
- Date parse lỗi, `from > to`, timezone, max span, empty/unknown segment và error mapping chưa được contract chốt. Catalog #102 không khai báo 400/422.

| Item | Normalized/candidate use | Status |
|---|---|---|
| `from` | `effective_from` | String type DIRECT; ISO parsing/default DERIVED |
| `to` | `effective_to` | String type DIRECT; ISO parsing/default DERIVED |
| `segment` omitted | `learning` + `community` metric groups | DERIVED |
| `segment=learning` | Q1 + Q2 | DERIVED |
| `segment=community` | Q3 + Q4 | DERIVED |

## 2. Aggregate candidate metrics

Các query độc lập để tránh fan-out. Đây là `DERIVED` proposal trên legacy DDL/ERD; chưa phải SQL runtime hoặc live-schema verification. Không đọc nội dung thảo luận/PII và không filter `status` do enum/visibility rule chưa được duyệt.

### Q1 — Unique enrolled learners

| Thuộc tính | Candidate mapping |
|---|---|
| Base table | Legacy `enrollments` |
| Selected value | `COUNT(DISTINCT user_id)` |
| Date column | `enrolled_at` |
| Predicate | `CAST(enrolled_at AS DATE) BETWEEN :effective_from AND :effective_to` |
| Null behavior | `COUNT(DISTINCT ...)` không đếm `user_id IS NULL`; legacy DDL cho phép NULL nhưng guide/ERD nêu FK bắt buộc |
| Result key | `unique_enrolled_learners` |
| Segment | `learning` |
| Status | DERIVED; live schema, enrollment population và date boundary chưa verified |

### Q2 — Course completion records

| Thuộc tính | Candidate mapping |
|---|---|
| Base table | Legacy `enrollments` |
| Selected value | `COUNT(*)` |
| Date column | `completed_at` |
| Predicate | `completed_at IS NOT NULL AND CAST(completed_at AS DATE) BETWEEN :effective_from AND :effective_to` |
| Population | Enrollment rows; không deduplicate theo user/course; không suy enum từ `status` |
| Result key | `course_completions` |
| Segment | `learning` |
| Status | DERIVED; nghĩa timestamp/status và duplicate policy cần xác nhận |

### Q3 — Root discussion topics

| Thuộc tính | Candidate mapping |
|---|---|
| Base table | Legacy `discussions` |
| Selected value | `COUNT(*)` |
| Date column | `created_at` |
| Predicate | `parent_id IS NULL AND CAST(created_at AS DATE) BETWEEN :effective_from AND :effective_to` |
| Population | Root discussion rows; không đọc `content`, không filter status |
| Result key | `discussion_topics_created` |
| Segment | `community` |
| Status | DERIVED; AC-19 Comment storage may differ from legacy model |

### Q4 — Discussion replies

| Thuộc tính | Candidate mapping |
|---|---|
| Base table | Legacy `discussions` |
| Selected value | `COUNT(*)` |
| Date column | `created_at` |
| Predicate | `parent_id IS NOT NULL AND CAST(created_at AS DATE) BETWEEN :effective_from AND :effective_to` |
| Population | Child discussion rows; không đọc `content`, không filter status |
| Result key | `discussion_replies_created` |
| Segment | `community` |
| Status | DERIVED; AC-19 Comment storage may differ from legacy model |

### Q5 — Pilot report snapshot alternative

Pilot `report_snapshots` has `report_code`, period timestamps, `dimensions`, `metrics`, watermark/version and `generated_at`; no #102 code, segment JSON contract, writer or API mapping was found. UUID pilot `course_enrollments` also differs from the legacy BIGINT candidate. No executable snapshot query is selected and no pilot/legacy join is allowed.

## 3. Select metric set and build `Report`

1. Nếu segment không có: lấy Q1–Q4.
2. Nếu segment là `learning`: lấy Q1–Q2.
3. Nếu segment là `community`: lấy Q3–Q4.
4. Giá trị ngoài hai nhóm đề xuất chưa có branch/error mapping được duyệt; không tự trả empty set hoặc thêm code.
5. Chuyển COUNT sang decimal-string; zero-as-`"0"` là proposal.
6. `Report.period` dùng effective range; `generated_at` là thời điểm tạo response theo UTC proposal.

| Response field | Candidate source/transform | Status |
|---|---|---|
| `period.from/to` | Effective date bounds | DIRECT DateRange types; parse/default DERIVED |
| `metrics[].key` | Four proposed metric keys | DERIVED |
| `metrics[].value` | Q1–Q4 aggregate → decimal string | Type DIRECT; formula DERIVED |
| `metrics[].label` | Vietnamese display text | Type DIRECT; text DERIVED |
| `generated_at` | Report assembly clock | Type DIRECT; UTC proposal |
| `businessCode` | Catalog success literal | DIRECT `DESIGN_RESOURCE_RETRIEVED` |
| `traceId` | Request trace context | Shared API guideline |

## 4. Error branches

- 401 `DESIGN_AUTHENTICATION_REQUIRED` — authentication failure theo catalog.
- 403 `DESIGN_ACCESS_DENIED` — không có role/Admin-report permission theo catalog.
- 500 `DESIGN_INTERNAL_ERROR` — unexpected aggregate/query failure theo catalog.
- Date validation is explicit in AC-38, but the catalog row has no 400/422 code. Do not assign an unapproved mapping for parse/reversed ranges or unknown segment.
- Chi tiết xem [06_Error.md](./06_Error.md).

## 5. Mutation and consistency

- API #102 là read-only: không INSERT/UPDATE/DELETE, không ghi `report_snapshots`.
- Independent queries may see different committed states unless a consistent read snapshot is used; transaction/isolation policy is `SOURCE_REQUIRED`.
- Không trả raw `user_id`, discussion author/content, or row-level data; only aggregate values.

## Request Usage Matrix

| Request item | Source | Use | Rule/status |
|---|---|---|---|
| `Authorization` | Bearer JWT | Authenticate Admin and check report permission first | DIRECT expected; Admin guard SOURCE_REQUIRED |
| `from` | Optional query string | Lower period bound for Q1–Q4 | DIRECT field; parse/default DERIVED |
| `to` | Optional query string | Upper period bound for Q1–Q4 | DIRECT field; parse/default DERIVED |
| `segment` | Optional query string | Select metric subset | DIRECT field; values/branch DERIVED |
| Body/path | None | No use | DIRECT |

## Query Matrix

| Query | Type | Base table | Candidate columns | Predicate | Result/status |
|---|---|---|---|---|---|
| Q1 | SELECT COUNT DISTINCT | `enrollments` | `user_id`, `enrolled_at` | Period on enrolled_at | Unique enrolled learners; DERIVED |
| Q2 | SELECT COUNT | `enrollments` | `completed_at` | Non-NULL and period | Completion records; DERIVED |
| Q3 | SELECT COUNT | `discussions` | `parent_id`, `created_at` | parent NULL and period | Root topics; DERIVED |
| Q4 | SELECT COUNT | `discussions` | `parent_id`, `created_at` | parent non-NULL and period | Replies; DERIVED |
| Q5 | SELECT candidate | Pilot `report_snapshots` | `report_code`, period, `dimensions`, `metrics` | No approved report/segment selector | Alternative only; SOURCE_REQUIRED |

## Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Status |
|---|---|---|---|---|---|
| — | None | N/A | Read-only API | No writes | N/A — READ-ONLY API |

## Response Source Matrix

| Response field | Type | Source type | Table/column or generator | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|
| `success` | boolean | Envelope | N/A | true on success | Non-null | Shared convention |
| `businessCode` | string | Catalog | N/A | `DESIGN_RESOURCE_RETRIEVED` | Non-null | DIRECT |
| `message` | string | Application | N/A | Safe message | Literal unspecified | SOURCE_REQUIRED |
| `data.period.from` | date | Query/default | `from` / effective range | Normalize to date | Non-null | Parse/default DERIVED |
| `data.period.to` | date | Query/default | `to` / effective range | Normalize to date | Non-null | Parse/default DERIVED |
| `data.metrics[].key` | string | Derived | Metric key | Select by `segment` | Non-null | Key/group DERIVED |
| `data.metrics[].value` | decimal-string | Aggregate | Q1–Q4 counts | Decimal string | zero-as-`"0"` proposal | Formula DERIVED |
| `data.metrics[].label` | string | Derived label | Vietnamese display text | Plain label | Non-null | Text DERIVED |
| `data.generated_at` | date-time | Clock | Report assembly time | ISO-8601 UTC proposal | Non-null | Clock policy DERIVED |
| `meta` | object | Envelope | N/A | `{}` candidate | Non-null | Endpoint detail unspecified |
| `traceId` | uuid | Request context | Trace helper | Propagate request trace | Non-null | Common guideline |
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
