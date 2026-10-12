---
title: "Định nghĩa table"
order: 7
dd_id: "23"
api_name: "Khởi tạo/lưu lần bắt đầu học"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | lesson_progress — candidate, DESIGN_ONLY |
| Logical table | Lesson progress |
| Operation | UPSERT theo AC-14; exact SQL/conflict target chưa xác nhận |
| Data Mapping step | 3 |

## Update mapping

**Áp dụng khi**

- AC-14 diagram mô tả UPSERT lesson progress = IN_PROGRESS; update path cụ thể chưa được định nghĩa.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---:|---|
| 1 | status | Progress status | VARCHAR | 20 | N/A | SOURCE_REQUIRED | N/A | IN_PROGRESS | AC-14 diagram | 3 | Intended value is explicit; existing-state transition/preservation is unresolved. |

## Insert mapping

**Áp dụng khi**

- AC-14 diagram mô tả UPSERT; insert path và generated/required values chưa được phân rã.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---|---|---|---|---:|---|
| 1 | user_id | Student ID | BIGINT | N/A | N/A | SOURCE_REQUIRED | N/A | From authenticated Student identity | DB design relationship + actor contract | 3 | Token claim binding and requiredness at runtime not verified. |
| 2 | lesson_id | Lesson ID | BIGINT | N/A | N/A | SOURCE_REQUIRED | N/A | Request path lesson_id | API catalog + DB design | 1/3 | Candidate FK; runtime constraint not verified. |
| 3 | status | Progress status | VARCHAR | 20 | N/A | Yes for intended state | N/A | IN_PROGRESS | AC-14 diagram | 3 | DDL default is NOT_STARTED; AC-14 explicitly describes IN_PROGRESS for start flow. |

> Các kiểu/cột trên chỉ đối chiếu checked-in DDL. Không xác nhận live schema, unique constraint, id generation, write order hoặc mặc định runtime.

## Delete mapping

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | AC-14 API #23 không mô tả DELETE. |

## Read source note

- Checked-in DDL định nghĩa lesson_progress columns: id, user_id, lesson_id, status, progress_percent, last_accessed_at, completed_at.
- DDL không khai báo unique constraint cho cặp user_id/lesson_id; không đủ căn cứ chọn conflict target cho UPSERT.
- Các cột progress_percent, last_accessed_at và completed_at không được sơ đồ API #23 nêu là giá trị cần cập nhật; không tự đặt hoặc reset.
- Candidate schema không xác nhận API runtime hay live database. Xem [05_Data_Mapping.md](./05_Data_Mapping.md) và [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

---
## Phụ lục đối chiếu template Markdown

- Template: [07_table.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/07_table.md).
- Sheet nguồn: table.
