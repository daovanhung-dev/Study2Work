---
title: "Cover"
order: 0
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Cover"
format: markdown
---

# Study2Work — API Detail Design

## Thông tin tài liệu

| Thuộc tính | Giá trị |
|---|---|
| Project/System | Study2Work |
| Module | Student / Learning & Interaction |
| Loại tài liệu | API Detail Design |
| API ID | 20 |
| API name | Lấy danh sách khóa học đã đăng ký |
| HTTP method | GET |
| Endpoint | /api/v1/users/me/courses |
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
Lấy danh sách khóa học đã đăng ký
~~~

## Cảnh báo contract

Catalog khai báo response là ApiEnvelope<UserProfile>. AC-13 yêu cầu hiển thị danh sách Course cùng progress lấy riêng từ API #21. DD giữ nguyên response catalog và đánh dấu payload danh sách khóa học là gap cần xác nhận.

---
## Phụ lục đối chiếu template Markdown

- Template: [createDD_MARKDOWN_SKILL.md](../../../../../.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md).
- Template folder: [DD_API_Template_MD](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/).
- Sheet nguồn: Cover.
