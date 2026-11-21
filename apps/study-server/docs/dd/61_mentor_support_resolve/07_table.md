---
title: "Định nghĩa table"
order: 7
dd_id: "61"
api_name: "Đóng yêu cầu hỗ trợ"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `support_requests` — local migration 008 / `DB.sql`; live schema chưa xác minh |
| Logical table | SupportRequest |
| Operation | UPDATE |
| Data Mapping step | [4–5](./05_Data_Mapping.md) |

## Update mapping

Áp dụng sau khi request row được `SELECT ... FOR UPDATE` và Mentor được xác thực là owner trực tiếp của course.

| No | Item ID / Column | Item name | Type | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---|---|---|---|---|
| 1 | `id` | Support request ID | BIGINT | Yes | PK | Match `request_id`; không thay đổi | Migration 008 | 3–4 | Catalog int64; numeric mapping DERIVED local fallback. |
| 2 | `course_id` | Course ID | BIGINT | Yes | FK | Dùng nối sang `courses.id` và kiểm tra `mentor_id` | Migration 008 | 2, 4 | API không cập nhật. |
| 3 | `status` | Request status | VARCHAR(24) | Yes | No | `OPEN`, `IN_PROGRESS`, `WAITING_LEARNER` → `RESOLVED` | AC-24 + migration 008 | 5.1 | Chuyển state là DIRECT; danh sách pre-state là DERIVED. |
| 4 | `resolved_at` | Resolution time | TIMESTAMPTZ | No | No | `COALESCE(resolved_at, CURRENT_TIMESTAMP)` khi chuyển active state | Migration 008 + DERIVED | 5.2 | Giữ giá trị cũ khi đã RESOLVED; không null trong success response. |

## Không ghi

- `student_id`, `created_at` và request ID không thay đổi.
- API #61 không INSERT/UPDATE/DELETE `support_messages` hoặc `support_message_uploads`.
- Không có cột `updated_at`, `row_version`, `resolution_code` hoặc `cancelled_at` trong local migration 008; không ghi các cột này.
- V1-PILOT `support_tickets` và trigger của nó không phải mapping cho implementation local.
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
