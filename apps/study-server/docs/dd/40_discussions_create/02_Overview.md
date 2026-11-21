---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "40"
api_name: "Tạo topic/câu hỏi mới"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 40 |
| Module | Student / Learning & Interaction |
| Method | POST |
| Endpoint | `/api/v1/discussions` |
| Purpose | Tạo topic/câu hỏi mới trong discussion của một course. |
| Consumer/Actor | Student |
| Authentication | Bearer JWT |
| Authorization | Role Student; DERIVED proposal: yêu cầu enrollment ACTIVE cho course_id. Predicate và policy vẫn cần xác nhận. |
| Basis | DIRECT — approved design contract và AC-19 |
| Status | Draft — Needs Confirmation; design-only, runtime `UNWIRED / NOT_FOUND`. |
| Transaction | TBD — transaction boundary và lỗi rollback chưa có source cho API #40. |
| Side effects | Candidate `INSERT` vào `discussions`; chưa có implementation hoặc live schema verification. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — `APPROVED_DESIGN_CONTRACT`; API #40, reusable `Discussion`, `Page`, `PageMeta`, `UserSummary`.
- [AC API index](../../../docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, precondition, postcondition và API mapping của AC-19.
- [AC-19 activity diagram](../../../docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — nhánh tạo topic, endpoint, request/response và thao tác `INSERT Discussion`.
- [Discussion DB guide](../../../docs/diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../../docs/diagrams/DB_UNICA_ERD.drawio) — candidate fields và quan hệ; design-only.
- [Checked-in DB DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate physical columns; không xác nhận live schema.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — envelope, trace ID và error response conventions.
- [Study auth helper](../../../app/utils/auth.py), [Study API router](../../../app/api/v1.py) và API #39 [DD](../39_discussions/00_Cover.md) — current auth evidence, runtime boundary và adjacent discussion context.

## Tables read

- `discussions` — candidate insert; schema evidence còn `DESIGN_ONLY`.
- `users` — candidate author projection only; query và response lookup chưa được chốt.
- `enrollments` — DERIVED source cho access principal/course/status ACTIVE; cần xác nhận.

## Tables write

- `discussions` — candidate insert theo AC-19; physical mapping chưa hoàn chỉnh.

## Mục chú ý

- Contract yêu cầu request `content:int64!`, trong khi reusable `Discussion.content` là `string` và DDL khai báo `discussions.content TEXT`.
- Contract yêu cầu `title:string!`, nhưng ERD và checked-in DDL không có cột `discussions.title`.
- Success contract là `ApiEnvelope<Page<Discussion>>` với HTTP 201; đề xuất DERIVED: một root item, metadata 1/1/1/1 và comments rỗng ngay sau khi tạo.
- AC-19 tách nhánh tạo topic khỏi nhánh reply; `parent_id = NULL` là root mapping theo DB guide và được đề xuất DERIVED.
- DDL cho phép `course_id` và `user_id` NULL, còn DB guide/ERD xem các quan hệ này là bắt buộc.

## Assumptions

- Giữ nguyên approved catalog contract theo lựa chọn của người dùng; mọi mismatch được ghi thành open question, không sửa API catalog.
- Đề xuất DERIVED: enrollment ACTIVE, root status ACTIVE, server timestamp, content int64 chuyển thành chuỗi thập phân và Page một item. Các đề xuất cần xác nhận.

## Conflicts

- Request `content:int64` không khớp reusable response `Discussion.content:string` hoặc physical `TEXT`.
- Required logical `Discussion.title` không có physical source column.
- AC-19 precondition yêu cầu course participation nhưng không định nghĩa predicate; enrollment ACTIVE là đề xuất DERIVED.
- Course/user FK nullability trong DB guide/ERD khác checked-in DDL.
- Response `Page<Discussion>` chưa có pagination source; one-item page là đề xuất DERIVED.

## Security note

- Contract chỉ nhận `course_id`, `title`, `content`; user identity phải đến từ authenticated Student principal, không nhận user ID từ body.
- Current auth helper xác thực JWT subject và Student role cho các route đã wire; API #40 chưa gọi helper này.
- Enrollment ACTIVE cho course_id là đề xuất DERIVED thống nhất với API #39/#41/#42; cần xác nhận trước implementation.

## Performance note

- Không có runtime query hoặc benchmark cho API #40; không ghi nhận performance target.
---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Overview`
- Dimension: `A1:BA10`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `4`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | 【Khái quát】 |  |
| 3 | `B3` | Get thông tin…. |  |
| 5 | `A5` | 【Mục chú ý】 |  |
| 7 | `B7` | Không có |  |

</details>
