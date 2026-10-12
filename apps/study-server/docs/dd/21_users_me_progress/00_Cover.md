---
title: "Cover"
order: 0
dd_id: "21"
api_name: "Lấy tiến độ tổng hợp"
source_sheet: "Cover"
status: "Draft — Needs Confirmation"
---

# Study2Work — API Detail Design

## Thông tin tài liệu

| Thuộc tính | Giá trị |
|---|---|
| Project/System | Study2Work |
| Module | STUDENT / LEARNING & INTERACTION |
| Loại tài liệu | API Detail Design |
| API ID | 21 |
| API name | Lấy tiến độ tổng hợp |
| HTTP method | GET |
| Endpoint | /api/v1/users/me/progress |
| Version | v1 |
| Status | Draft — Needs Confirmation |
| Created by | Codex |
| Reviewed by | Pending |
| Approved by | Pending |
| Created date | 2026-10-11 |
| Updated date | 2026-10-11 |

## Tên hiển thị

~~~text
Study2Work API design
Lấy tiến độ tổng hợp
~~~

## Cảnh báo contract

Catalog và AC diagrams khai báo response ApiEnvelope<UserProfile>, trong khi AC-13/AC-18 mô tả dữ liệu tiến độ. Query phrase “course_id list hoặc aggregate?:string” cũng chưa xác định được tên field, kiểu của danh sách course_id hoặc semantics aggregate. DD giữ nguyên contract khai báo và để các quyết định payload/query ở OPEN_QUESTIONS.md.

---
## Phụ lục đối chiếu template Markdown

- Template: [createDD_MARKDOWN_SKILL.md](../../../../../.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md).
- Template folder: [DD_API_Template_MD](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/).
- Sheet nguồn: Cover.
