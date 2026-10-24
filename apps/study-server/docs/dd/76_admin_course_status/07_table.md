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
| Legacy courses | UPDATE candidate | Đổi trạng thái khóa học theo AC-32 STATUS branch | DERIVED candidate; live schema chưa verify. |
| Audit event | Logical append effect | Bắt buộc theo diagram nhưng chưa có physical table tương thích direct int64 contract | SOURCE_REQUIRED; không tạo mapping giả. |

Legacy Study DDL xác nhận courses.id BIGSERIAL, courses.status VARCHAR(20) DEFAULT 'DRAFT', courses.updated_at TIMESTAMP NOT NULL. Đây là DDL artifact, không chứng minh schema runtime.

V1-PILOT có UUID courses, UUID course_versions, course_versions.status enum và audit_events với UUID resource_id/actor_subject_id. Các bảng này không phải target tương đương cho API #76 BIGINT path. Live DB chưa được xác minh.

## Update mapping

### Candidate target — legacy courses

| Logical field | Relation | Column | Operation | Mapping/status |
|---|---|---|---|---|
| Course ID | courses | id | WHERE | Map course_id:int64; legacy BIGSERIAL candidate. |
| Target status | courses | status | UPDATE/RETURNING | Body status candidate; allowed semantics from catalog; exact enum/casing DERIVED/SOURCE_REQUIRED. |
| Updated time | courses | updated_at | UPDATE | Candidate database current timestamp; not direct AC rule. |
| Course metadata | courses | name, description, thumbnail_url, price | No change | Owned by API #75; preserve values. |
| Mentor owner | courses | mentor_id | No change | Not part of API #76. |

### Update condition

- Candidate predicate: courses.id = :course_id.
- Q1 obtains courses.status and locks the row before mutation.
- No old-status transition predicate is proposed because AC-32 has no transition matrix.
- No PUBLISHED filter; Admin may update all states.
- If no row matches, return 404 DESIGN_RESOURCE_NOT_FOUND candidate.
- SQL is design-only until schema/runtime owner confirms legacy model.

### Audit event mapping — SOURCE_REQUIRED

| Logical field | Candidate source | Physical mapping |
|---|---|---|
| Actor | Authenticated Admin principal | ID claim/type not known; do not convert numeric ID to UUID. |
| Resource | Course ID and resource type | Legacy course ID is int64; pilot audit resource_id is UUID, incompatible. |
| Action | Change course status | Exact action name not specified. |
| Change details | Previous and target status | Pilot has changes jsonb; no approved legacy audit target. |
| Outcome/code | Successful status update | Pilot audit_outcome/business_code are not direct contract. |
| Trace | Request trace ID | Study runtime trace is UUID; pilot audit trace_id is varchar. |
| Timestamp | Event occurrence | Source/timezone/retention policy not selected. |

No audit INSERT SQL or table mapping can be finalized until the project selects a schema compatible with API #76 and defines actor/resource/event fields. The diagram requirement remains mandatory; a status-only write is not complete.

### Transaction boundary

Candidate transaction:

1. Lock/read course.
2. Update status and timestamp.
3. Append audit event using approved physical mapping.
4. Read updated Course projection.
5. Commit only when all required operations succeed.

Study DB helpers do not commit; the use case/caller must own the transaction. Roll back if update, audit append, projection or commit fails.

## Insert mapping

Không xác định được physical audit relation cho API #76 từ legacy int64 schema. Audit log là logical side effect bắt buộc; physical INSERT mapping SOURCE_REQUIRED. Không coi pilot audit_events là tương thích khi resource/actor IDs vẫn UUID và live schema chưa xác minh.

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
