---
title: "Định nghĩa table"
order: 7
dd_id: "78"
api_name: "Lấy pending content"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "DB table"
format: markdown
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Attribute | Value |
|---|---|
| Physical table candidate | `contents` |
| Source | `infra/postgres/study-server/DB.sql`; migration `006_contents.sql` |
| Primary key | `id BIGSERIAL` |
| Relation | `course_id BIGINT REFERENCES courses(id)`; nullable self-parent `parent_id` scoped by course |
| Queue status | `status TEXT`; no CHECK/enum is defined; AC-33 uses `PENDING_REVIEW` |
| Soft delete | `deleted_at TIMESTAMP NULL` |
| Payload | `payload JSONB NOT NULL CHECK (jsonb_typeof(payload) = 'object')` |
| Runtime use | APIs #49–#53 currently query/mutate `contents`; API #78 reuses that relation candidate |
| Verification | Checked-in artifact and current source only; live schema/migrations not verified |

## Read mapping

| Response/query item | Physical source | Rule |
|---|---|---|
| `id` | `contents.id` | Reusable Content ID. |
| `course_id` | `contents.course_id` | Exact optional `course` filter. |
| `content_type` | `contents.content_type` | Exact optional `type` filter; no enum whitelist. |
| `title` | `contents.title` | Preserve stored value. |
| `payload` | `contents.payload` | Preserve JSON object. |
| `status` | `contents.status` | Fixed `PENDING_REVIEW` queue predicate. |
| `parent_id` | `contents.parent_id` | Nullable. |
| `order` | `contents.content_order` | Response alias; does not set queue order. |
| active row | `contents.deleted_at` | `IS NULL` DERIVED visibility filter aligned with #49/#53. |
| queue order | `contents.id` | `ASC` DERIVED stable order. |
| page | Query + fixed `LIMIT 20` | Default 1, offset `(page-1)*20`; all DERIVED from #73 convention. |

## Update mapping

N/A — API #78 không cập nhật Content.

## Insert mapping

N/A — API #78 không thêm Content.

## Delete mapping

N/A — API #78 không xóa Content. API #53 owns Mentor Content soft-delete; #80/#81 own review decisions.

## Related version table

`content_versions` (migration 007) stores prior-state snapshots written by API #51. API #78 does not join it; the logical current `contents` row is the queue item under the local DERIVED choice. Which revision #79–#81 must act on remains open.

## Query mapping

- Q1 count and Q2 list both require `status='PENDING_REVIEW' AND deleted_at IS NULL`.
- Optional `type` maps to exact `content_type`; optional `course` maps to exact `course_id`.
- Q2 orders `id ASC` and uses fixed page size 20. No write, audit or lock is used.
- Physical mapping is a checked-in legacy/current-code candidate only, not live schema evidence.

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
