---
title: "Cover"
order: 0
dd_id: "73"
api_name: "Lấy danh sách khóa học Admin"
source_sheet: "Cover"
status: "Draft — Needs Confirmation"
---

# Study2Work — API Detail Design

## Thông tin tài liệu

| Thuộc tính | Giá trị |
|---|---|
| Project/System | Study2Work — Study Server |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-32 |
| Loại tài liệu | API Detail Design |
| API ID | #73 |
| API name | Lấy danh sách khóa học Admin |
| HTTP method | GET |
| Endpoint | `/api/v1/admin/courses` |
| Version | 1.0 |
| Status | Draft — Needs Confirmation |
| Created by | Codex |
| Reviewed by | Chờ xác nhận |
| Approved by | Chờ xác nhận |
| Created date | 2026-10-24 |
| Updated date | 2026-10-26 |

## Tên hiển thị

```text
GET /api/v1/admin/courses
Lấy danh sách khóa học để quản trị
```

## Phạm vi và trạng thái

Catalog yêu cầu Bearer JWT role Admin, query `status`, `mentor`, `category`, `page` tùy chọn và response `ApiEnvelope<Page<Course>>`. AC-32 đặt API này trước bước mở detail #74 và các nhánh update #75, status #76, delete #77.

Study hiện có route/module/test cục bộ cho API #73. Runtime dùng shared JWT role `ADMIN`, truy vấn legacy candidate `courses/users`, và từ chối `category` hợp lệ bằng 422 trước DB vì DDL không có quan hệ course-category. Fallback này cùng page 1, size 20, thứ tự ID tăng dần, equality filters, all-status mặc định và lỗi integrity 500 là `DERIVED`; DD vẫn Draft. Test dùng fake DB, nên live schema/deployment và quyền course-management riêng chưa được xác minh.

## Tài liệu tham chiếu

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #73, `Course`, `Page`, `PageMeta`.
- [AC-32 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, quyền course management và chuỗi #73–#77.
- [AC-32 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — query list → detail → update/status/delete → reload.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) — course mapping hiện là design-only.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT `courses`, `users`, `categories`; không chứng minh live schema.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID `courses` và `course_versions`, không tương đương contract int64.
- [API #06 course source](../../../app/modules/guest/api_06_courses/) — public projection, PageMeta, price mapping và category gap.
- [API #68 Admin list DD](../68_admin_users_list/02_Overview.md) — cách tách catalog contract, pagination proposal và Admin guard gap.
- [Worklog API #73](../../../../../.agents/worklog/2026-10-24/create-study-api73-dd.md) — preflight, plan và ma trận trước khi tạo folder.

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
