---
title: "Định nghĩa table"
order: 7
dd_id: "102"
api_name: "Lấy dữ liệu tác động cộng đồng"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Candidate read tables

| Table | Schema evidence | Operation | Data Mapping step | Status |
|---|---|---|---|---|
| `enrollments` | `infra/postgres/study-server/DB.sql`; `DB_UNICA_ERD.drawio`; `DB_UNICA_TABLES.md` | SELECT COUNT / COUNT DISTINCT | Q1–Q2 | Legacy design candidate; live schema unverified |
| `discussions` | `infra/postgres/study-server/DB.sql`; `DB_UNICA_ERD.drawio`; `DB_UNICA_TABLES.md` | SELECT COUNT | Q3–Q4 | Legacy self-reference candidate; AC-19 comment storage differs |
| `report_snapshots` | `infra/postgres/02_study_db.sql` | Candidate SELECT only | Q5 | V1-PILOT alternative; no report/segment mapping; not selected |

## Read mapping — legacy `enrollments`

| Column | Type/constraint in DDL | Query use | Candidate metric | Status |
|---|---|---|---|---|
| `user_id` | `BIGINT REFERENCES users(id)`; nullable in DDL | Q1 `COUNT(DISTINCT user_id)` | `unique_enrolled_learners` | DB guide/ERD states required; discrepancy retained; live schema unknown |
| `enrolled_at` | `TIMESTAMP NOT NULL` | Q1 date predicate | `unique_enrolled_learners` | Candidate timestamp; date/time policy DERIVED |
| `completed_at` | `TIMESTAMP NULL` | Q2 non-null date predicate | `course_completions` | Completion semantics/uniqueness DERIVED; live schema unknown |
| `status` | `VARCHAR(20) DEFAULT 'ACTIVE'` | Not filtered | None | Enum incomplete; status predicate not selected |

## Read mapping — legacy `discussions`

| Column | Type/constraint in DDL | Query use | Candidate metric | Status |
|---|---|---|---|---|
| `id` | `BIGSERIAL PRIMARY KEY` | Not returned; aggregate input rows only | None | No domain ID in response |
| `parent_id` | `BIGINT NULL REFERENCES discussions(id)` | Q3 root / Q4 reply predicate | `discussion_topics_created`, `discussion_replies_created` | ERD/guide self-reference; differs from AC-19 separate Comment step |
| `created_at` | `TIMESTAMP NOT NULL` | Q3/Q4 date predicate | Both community metrics | Candidate timestamp; date/time policy DERIVED |
| `status` | `VARCHAR(20) DEFAULT 'ACTIVE'` | Not filtered | None | Visibility/moderation population unresolved |
| `content` | `TEXT NOT NULL` | Never selected | None | Do not return raw discussion content |
| `user_id` | `BIGINT REFERENCES users(id)`; nullable in DDL | Not selected | None | No actor-level output or PII query |

## Pilot alternative — `report_snapshots`

The V1-PILOT snapshot model is UUID/versioned and contains JSONB dimensions/metrics. The API #102 report code, segment vocabulary, JSON schema, writer, freshness and live availability are not established. It is not joined to the legacy BIGINT candidates and is not selected as an executable query.

## Mutation mapping

**Áp dụng khi** N/A — API #102 là read-only.

| Operation | Target | Mapping |
|---|---|---|
| UPDATE | N/A | Không cập nhật enrollment/discussion rows |
| INSERT | N/A | Không tạo report snapshot theo evidence hiện có |
| DELETE | N/A | Không xóa enrollment/discussion/snapshot rows |
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
