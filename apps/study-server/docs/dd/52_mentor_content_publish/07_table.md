---
title: "Định nghĩa table"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "52"
api_name: "Publish/unpublish nội dung Mentor"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — Logical Content publication status

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table/model | Legacy `contents` base relation in DDL/migration 006; live schema unverified. |
| Logical table/entity | Content và publication/review state |
| Operation | UPDATE publication status |
| Data Mapping step | 3–4 |
| Evidence | AC-22: PATCH → UPDATE publication status → reload tree. |
| Runtime | Local API #52 route/module/tests are source-backed; canonical contract and live DB remain unverified. |

## Update mapping

**Áp dụng khi**

- Mentor đã xác thực và có quyền quản lý course theo AC-22.
- Content tồn tại và target transition được policy đã duyệt cho phép.
- Với publish, readiness check đạt.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| 1 | `contents.status` | Publication/review status | TEXT | N/A | N/A | Yes | N/A | Proposed publish: APPROVED → PUBLISHED. | Local DDL/migration 006 | 3–4 | Column available locally; transition and full enum remain unresolved. |
| 2 | N/A | Content revision | Logical revision | N/A | N/A | N/A | N/A | No new revision proposed. | AC-22 status-only step; #51 update/version step | 3–4 | `contents` has no version/current pointer. |
| 3 | `contents.content_type/title/payload` | Content fields | TEXT/JSONB | N/A | N/A | N/A | N/A | Preserve without content edit. | Local DDL/migration 006 | 3–4 | Base projection present locally; subtype policy open. |
| 4 | `contents.course_id/parent_id/content_order` | Course/tree fields | BIGINT/INTEGER | N/A | N/A | N/A | N/A | Preserve ownership and tree placement. | Local DDL/migration 006 | 2–4 | Base projection present locally; live schema unverified. |

## Insert mapping

N/A — API #52 does not create Content or a revision in this proposal. AC-22 specifies publication-status update only.

## Delete mapping

N/A — deletion is API #53.

## Proposed logical transition table

| Target input proposal | Current state candidate | Readiness | Proposed result | Evidence/status |
|---|---|---|---|---|
| published=true | APPROVED | Pass | PUBLISHED | State names partly in AC-33; transition/readiness details DERIVED. |
| published=false | PUBLISHED | Not required | APPROVED | DERIVED; preserves approval, confirm with AC-33. |
| Same target | Already matches desired state | Not required | Return current Content without write | DERIVED idempotency rule. |
| Either target | PENDING_REVIEW, REJECTED or other unconfirmed state | N/A | No mutation; 422 candidate | Named states direct from AC-33; transition rule DERIVED. |

AC-33's approval node says APPROVED/PUBLISHED + audit and does not identify whether both statuses are set together or are alternatives. The proposed table separates approval and publication so API #52 has a distinct role; this must be resolved in the AC-22/AC-33 macro-review.

## Physical SQL

Local API #52 SQL locks active Content/Course and updates `contents.status` only. This is a DERIVED fallback, not approved canonical SQL; transitions/readiness remain unresolved. Local `contents` has no revision history. V1-PILOT content_blocks remains a separate UUID model; do not substitute its row_version.

## Transaction and audit

The view commits the single status update after validating its response projection; fake Session tests cover commit/rollback only. This is DERIVED and does not establish live transaction behavior. AC-33 mentions audit for Admin approval, but API #52 does not specify an audit record or fields; audit mapping remains SOURCE_REQUIRED.

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
