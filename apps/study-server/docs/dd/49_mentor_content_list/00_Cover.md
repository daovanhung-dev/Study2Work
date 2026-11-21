---
title: "Cover"
order: 0
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Cover"
format: markdown
dd_id: "49"
api_name: "Lấy cây nội dung course"
status: "Draft — Needs Confirmation"
---

# Study2Work — API Detail Design

## Thông tin tài liệu

| Thuộc tính | Giá trị |
|---|---|
| Project/System | Study2Work / Study Server |
| Module | MENTOR / TEACHING & SUPPORT |
| Loại tài liệu | API Detail Design |
| API ID | 49 |
| API name | Lấy cây nội dung course |
| HTTP method | GET |
| Endpoint | `/api/v1/mentor/courses/{course_id}/content` |
| Version | v1 |
| Status | Draft — Needs Confirmation |
| Created by | Codex |
| Reviewed by | Chưa xác nhận |
| Approved by | Chưa xác nhận |
| Created date | 2026-10-24 |
| Updated date | 2026-10-25 |

## Tên hiển thị

**Lấy cây nội dung course của Mentor**

## Mục tiêu

Đọc các Content node đang hoạt động trong course để Mentor xem cây trước các thao tác AC-22. Implementation trả `ApiEnvelope<Content[]>`; `parent_id` liên kết node với parent và root không serialize `parent_id`.

## Tài liệu liên quan

- Catalog: `docs/lists/list_api.md`, API #49 và reusable schema `Content`.
- AC-22: `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md` và `AC_03_MENTOR_TEACHING.drawio`.
- DB artifacts: `apps/study-server/docs/diagrams/DB_UNICA_TABLES.md`, `DB_UNICA_ERD.drawio`, `infra/postgres/study-server/DB.sql`, migration `006_contents.sql`.
- Runtime: `apps/study-server/app/modules/mentor/api_49_mentor_content_list/`.
- Workflow: `.agents/server-study/workflows/README.md`; skill registry `createDD-markdown`.

## Phạm vi

Tài liệu này đặc tả riêng API #49. Các thao tác tạo/sửa/version/publish/xóa là API #50–#53. Bộ DD vẫn cần business/schema owner xác nhận các câu hỏi còn mở; DDL trong repository chưa chứng minh trạng thái DB live.

## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Cover`
- Dimension: `A1:AN46`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `1`
- Số vùng merge: `40`

<details>
<summary>Danh sách vùng merge</summary>

- `O42:R42`
- `S42:Z42`
- `AA42:AD42`
- `AE42:AN42`
- `O43:R46`
- `S43:V46`
- `W43:Z46`
- `AA43:AD46`
- `AE43:AN46`
- `O40:R40`
- `S40:Z40`
- `AA40:AN40`
- `O41:R41`
- `S41:Z41`
- `AA41:AN41`
- `O38:R38`
- `S38:Z38`
- `AA38:AN38`
- `O39:R39`
- `S39:Z39`
- `AA39:AN39`
- `O36:R36`
- `S36:Z36`
- `AA36:AN36`
- `O37:R37`
- `S37:Z37`
- `AA37:AN37`
- `O34:R34`
- `S34:Z34`
- `AA34:AN34`
- `O35:R35`
- `S35:Z35`
- `AA35:AN35`
- `G14:AG20`
- `O32:R32`
- `S32:Z32`
- `AA32:AN32`
- `O33:R33`
- `S33:Z33`
- `AA33:AN33`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 14 | `G14` | Tên Project　API design<br>Tên API |  |

</details>
