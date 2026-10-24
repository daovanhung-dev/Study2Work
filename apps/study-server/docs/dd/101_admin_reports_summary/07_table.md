---
title: "Định nghĩa table"
order: 7
dd_id: "101"
api_name: "Lấy KPI tổng quan"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Candidate read tables

| Table | Schema evidence | Operation | Data Mapping step | Status |
|---|---|---|---|---|
| `users` | `infra/postgres/study-server/DB.sql` | SELECT COUNT | Q1 | Legacy design candidate; not live verification |
| `courses` | `infra/postgres/study-server/DB.sql` | SELECT COUNT | Q2 | Legacy design candidate; not live verification |
| `enrollments` | `infra/postgres/study-server/DB.sql` | SELECT COUNT | Q3 | Legacy design candidate; not live verification |
| `discussions` | `infra/postgres/study-server/DB.sql` | SELECT COUNT | Q4 | Legacy design candidate; not live verification |
| `report_snapshots` | `infra/postgres/02_study_db.sql` | Candidate SELECT only | Q5 | V1-PILOT alternative; not selected and not live verification |

## Read mapping — legacy `users`

| Column | Type/constraint in DDL | Query use | Candidate metric | Status |
|---|---|---|---|---|
| `created_at` | `TIMESTAMP NOT NULL` | Date-range predicate | `user_records_created` | Metric semantics DERIVED; live schema unknown |

## Read mapping — legacy `courses`

| Column | Type/constraint in DDL | Query use | Candidate metric | Status |
|---|---|---|---|---|
| `created_at` | `TIMESTAMP NOT NULL` | Date-range predicate | `course_records_created` | Metric semantics DERIVED; live schema unknown |

## Read mapping — legacy `enrollments`

| Column | Type/constraint in DDL | Query use | Candidate metric | Status |
|---|---|---|---|---|
| `enrolled_at` | `TIMESTAMP NOT NULL` | Date-range predicate | `enrollment_records_created` | Metric semantics DERIVED; live schema unknown |

## Read mapping — legacy `discussions`

| Column | Type/constraint in DDL | Query use | Candidate metric | Status |
|---|---|---|---|---|
| `created_at` | `TIMESTAMP NOT NULL` | Date-range predicate | `discussion_records_created` | Counts topic/reply records in proposal; live schema unknown |

## Alternative read model — pilot `report_snapshots`

| Column | Type/constraint in pilot DDL | Possible use | Mapping status |
|---|---|---|---|
| `id` | `uuid PRIMARY KEY` | Snapshot identity | Not part of API Report; no mapping selected |
| `report_code` | `varchar(80) NOT NULL` | Select report kind | API #101 code not defined; SOURCE_REQUIRED |
| `period_start` | `timestamptz NOT NULL` | Snapshot range start | Date-boundary conversion not defined |
| `period_end` | `timestamptz NOT NULL` | Snapshot range end | Inclusive/exclusive policy not defined |
| `dimension_hash` | `char(64) NOT NULL` | Dimension identity | No dimensions contract for #101 |
| `dimensions` | `jsonb NOT NULL` | Snapshot filters | JSON shape not defined |
| `metrics` | `jsonb NOT NULL` | Possible `ImpactMetric[]` source | JSON schema/version mapping not defined |
| `source_high_watermark` | `timestamptz NOT NULL` | Source freshness boundary | No API response field mapping |
| `calculation_version` | `integer NOT NULL` | Formula version | No API version selection rule |
| `generated_at` | `timestamptz NOT NULL` | Candidate `Report.generated_at` | Shape similar; record selection/writer not established |

`report_snapshots` is a distinct UUID-based pilot model. Do not combine it with the legacy BIGINT tables in one query or claim it is live/written by API #101.

## Mutation mapping

**Áp dụng khi** N/A — API #101 là read-only.

| Operation | Target | Mapping |
|---|---|---|
| UPDATE | N/A | Không cập nhật metric/source rows |
| INSERT | N/A | Không tạo report snapshot trong endpoint theo evidence hiện có |
| DELETE | N/A | Không xóa report snapshot/source rows |
---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `table`
- Dimension: `A1:BA35`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `19`
- Số vùng merge: `5`

<details>
<summary>Danh sách vùng merge</summary>

- `W34:BA34`
- `W14:BA14`
- `W15:BA15`
- `W19:BA19`
- `W32:BA32`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `A2` | № |  |
| 2 | `B2` | Tên table |  |
| 3 | `B3` | SB |  |
| 3 | `S3` | Độ dài |  |
| 3 | `T3` | Dấu phẩy thập phân |  |
| 3 | `U3` | Bắt buộc |  |
| 3 | `V3` | Main key |  |
| 3 | `W3` | Nội dung setting |  |
| 4 | `B4` | № |  |
| 4 | `C4` | Item ID |  |
| 4 | `I4` | Item name |  |
| 4 | `O4` | Kiểu |  |
| 5 | `A5` | 1 |  |
| 5 | `B5` | table id |  |
| 5 | `I5` | table name |  |
| 6 | `B6` | Update |  |
| 6 | `I6` | Trường hợp số record get được từ xử lý 3. của sheet [３．Data mapping]  > 0 |  |
| 21 | `B21` | Insert |  |
| 21 | `I21` | Trường hợp số record get được từ xử lý 3. của sheet [３．Data mapping]  = 0 |  |

</details>
