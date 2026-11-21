---
title: "Định nghĩa table"
order: 7
dd_id: "76"
api_name: "Thay đổi trạng thái khóa học Admin"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

title: "Định nghĩa table"
order: 7
dd_id: "76"
api_name: "Thay đổi trạng thái khóa học Admin"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Table/Relation | Loại | Vai trò | Trạng thái |
|---|---|---|---|
| Legacy `courses` | `SELECT FOR UPDATE` / `UPDATE` | Đổi trạng thái theo AC-32 STATUS branch | Legacy BIGINT candidate; live schema chưa verify. |
| `course_status_audit_logs` | `INSERT` | Lưu course, Admin actor, status cũ/mới và thời điểm | Physical fallback DERIVED; migration 010 chưa xác nhận đã áp dụng. |

Legacy Study DDL xác nhận candidate `courses.id BIGSERIAL`, nullable `status VARCHAR(20)` và `updated_at TIMESTAMP NOT NULL`. Đây là DDL artifact, không chứng minh schema runtime.

V1-PILOT có UUID courses/course_versions và `audit_events` với UUID actor/resource IDs. API #76 dùng int64 contract và runtime legacy candidate; không nối ngầm sang UUID pilot. Live DB chưa được xác minh.

## Update mapping

| Logical field | Relation | Column | Operation | Mapping/status |
|---|---|---|---|---|
| Course ID | `courses` | `id` | WHERE/lock | `course_id:int64`; legacy BIGSERIAL candidate. |
| Target status | `courses` | `status` | UPDATE/RETURNING | Body `{status}`; DRAFT/PUBLISHED/SUSPENDED là fallback DERIVED. |
| Updated time | `courses` | `updated_at` | UPDATE | `CURRENT_TIMESTAMP`, DERIVED. |
| Course metadata | `courses` | `name`, `description`, `thumbnail_url`, `price` | No change | Owned by API #75. |
| Mentor owner | `courses` | `mentor_id` | No change | Not part of API #76. |

## Audit relation mapping — DERIVED fallback

| Logical field | Relation.column | Type/rule | Mapping/status |
|---|---|---|---|
| Audit identity | `course_status_audit_logs.id` | `BIGSERIAL PK` | Local schema fallback. |
| Course | `course_status_audit_logs.course_id` | `BIGINT NOT NULL FK courses.id ON DELETE RESTRICT` | API path ID; legacy key match. |
| Actor | `course_status_audit_logs.actor_user_id` | `BIGINT NOT NULL FK users.id ON DELETE RESTRICT` | Numeric user ID returned by shared JWT guard. |
| Previous status | `course_status_audit_logs.previous_status` | `VARCHAR(20) NULL` | Captures legacy nullable status. |
| New status | `course_status_audit_logs.new_status` | `VARCHAR(20) NOT NULL` | Target status from request. |
| Event time | `course_status_audit_logs.changed_at` | `TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP` | Database timestamp. |

AC-32 diagram directly requires an audit log but does not define its table or fields. This table is the smallest persistent fallback compatible with the current legacy int64 candidate. It is present in `DB.sql`, migration 010, the DB table guide/ERD and source SQL; none proves that a live database has the relation. The V1-PILOT `audit_events` table remains incompatible by key type.

## Mutation and transaction boundary

1. Lock `courses` by `id`; no row returns 404.
2. If status differs, update `status` and `updated_at`, then insert actor/course/old/new into `course_status_audit_logs` in the same transaction.
3. If status already equals the target, treat as idempotent no-op: no timestamp change and no duplicate audit row. This is DERIVED.
4. Read the #74 Course/mentor projection, validate it and commit only after mapping succeeds.
5. Roll back status and audit together on query, audit, projection, mapping or commit failure.

No transition/readiness gate, enrollment/content update, notification, action JSON, retention policy, trace column, audit read/update/delete endpoint or DB append-only trigger is inferred. Fine-grained Admin permission remains SOURCE_REQUIRED.

## Insert mapping

~~~sql
INSERT INTO course_status_audit_logs (
    course_id, actor_user_id, previous_status, new_status
) VALUES (
    :course_id, :actor_user_id, :previous_status, :new_status
)
~~~

The audit insert occurs only for an actual status change. SQL is parameterized in `query.py`; the view owns the shared transaction. The candidate migration is `infra/postgres/study-server/migrations/010_course_status_audit_logs.sql`.

## Delete mapping

N/A — API #76 không xóa khóa học. Soft delete và dependency policy thuộc API #77.

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
