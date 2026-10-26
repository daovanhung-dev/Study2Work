---
title: "Định nghĩa table"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "50"
api_name: "Tạo nội dung mới Conditional"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — Content insert target `contents` (DDL artifact)

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table/model | Legacy `contents` trong `DB.sql` và migration 006; live schema chưa xác minh. |
| Logical entity | `Content` theo API catalog #50. |
| Operation | Một logical INSERT theo AC-22. |
| Data Mapping step | 5–7 |
| Evidence | Catalog row #50 + Content schema; AC-22 INSERT node; AC-33 pending queue; legacy/pilot DDL comparison. |
| Runtime | API #50 route/module/TestClient tests source-backed locally; live schema/migration status remains unverified. |

## Insert mapping

| Logical field | Value source | Candidate rule | Evidence/status |
|---|---|---|---|
| `id` | Persistence layer | BIGSERIAL generates Content ID | Column/key source-backed in local DDL; live schema unverified |
| `course_id` | Request body | Persist after direct-owner check | Contract field; local FK to `courses`; live schema unverified |
| `content_type` | Request body | Persist open string unchanged | Contract field; local column TEXT; enum members unknown |
| `title` | Request body | Persist strict string unchanged | Contract field; local column TEXT; no additional length/normalization rule |
| `payload` | Request JSON object | JSON serialize then `CAST(:payload AS JSONB)` | Contract object; local JSONB object constraint; subtype keys unknown |
| `status` | Server lifecycle | `PENDING_REVIEW` | DERIVED from AC-33 queue condition; runtime implementation decision |
| `parent_id` | Server default; not request | SQL NULL for root Content | DERIVED from absence of parent input; response omits null |
| `content_order` / response `order` | Server allocator; not request | `GREATEST(MAX(content_order)+1, 0)` among active roots, first order 0 | DERIVED; course row lock serializes API #50 allocation per course |
| `id` | Persistence layer | BIGSERIAL-generated Content ID | Present in local DDL; live schema unverified |
| `deleted_at` | Local DDL default | Omitted in INSERT, therefore NULL | Local DDL column; active-row predicate used for root order |

## SQL mapping

The local legacy DDL/migration 006 defines `id`, `course_id`, `content_type`, `title`, `payload`, `status`, `parent_id`, `content_order` and `deleted_at`. API #50 inserts the writable fields and reads the generated ID/JSONB projection with `RETURNING`; it does not set `deleted_at`, audit fields or timestamps. V1-PILOT `content_blocks` is not substituted. Live schema and migration application remain unverified.

### Legacy course access candidate only

~~~sql
SELECT id, mentor_id
FROM courses
WHERE id = :course_id
LIMIT 1
FOR UPDATE;
~~~

This query is implemented against the checked-in legacy source. The shared JWT guard supplies numeric Mentor subject; the view compares it to `mentor_id`. The row lock supports serialized order allocation for API #50 writes. Assignment access is not included and live schema is not verified.

## Cross-API lifecycle

- API #50 creates Content with DERIVED status `PENDING_REVIEW`; AC-33 queue reads this state.
- API #51 updates Content, #52 publishes/unpublishes and #53 deletes. Their interactions with pending/rejected/approved content and the physical model need the AC-22 macro-review after #51–#53 DDs are available.
- AC-33 approves/rejects and refers to audit/review data; API #50 adds no audit columns. Pending item deletion/withdrawal behavior remains open with API #53.

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
