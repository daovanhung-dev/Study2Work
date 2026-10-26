---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "47"
api_name: "Tạo lecture"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 47 |
| Module | MENTOR / TEACHING & SUPPORT |
| Method | POST |
| Endpoint | /api/v1/mentor/courses/{course_id}/lectures |
| Purpose | Tạo lecture trong course Mentor quản lý sau khi asset đã upload qua API #34. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Shared access-JWT guard yêu cầu role MENTOR; chỉ Mentor có `users.id = courses.mentor_id` được tạo lecture. Không bao gồm course được phân công. Asset phải cùng Mentor, purpose LECTURE và cùng course_id. |
| Basis | API catalog/AC-21 và quyết định người dùng ngày 2026-10-25; `content:int64` được lưu/trả dưới dạng chuỗi thập phân. |
| Status | Draft — Needs Confirmation |
| Current runtime state | SOURCE_BACKED — route, module và HTTP tests API #47 đã được wire; live DB/schema chưa xác minh. |
| Transaction | Một transaction đọc course/assets, INSERT một row lessons và ordered `lesson_uploads` links khi asset_refs không rỗng, rồi commit; mọi lỗi truy vấn/ghi/commit rollback. |
| Side effects | INSERT lessons với status `PUBLISHED`, content decimal string, timestamps, và asset links for API #48 reload; không tạo resources row hoặc mutate uploads. |

## Sources

- [API catalog](../../../../../docs/lists/list_api.md) — #46–#50, Lecture và UploadAsset.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) và [AC-21 diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — sequence upload/create/reload.
- [API #34 DD](../34_uploads/02_Overview.md), [response](../34_uploads/04_Response.md) và [uploads migration](../../../../../infra/postgres/study-server/migrations/004_uploads.sql) — ID, metadata, purpose/status and storage source.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — BIGINT courses/lessons/uploads artifact; live schema chưa xác minh.
- [Current router](../../../app/api/v1.py), [module](../../../app/modules/mentor/api_47_mentor_lectures_create/) and [declared routes context](../../../../../.agents/server-study/apis/declared-routes.md) — API #47 is source-backed; live DB remains unverified.

## Tables read

- courses — read `id, mentor_id`; require direct `mentor_id` ownership and do not filter by course status.
- uploads — resolve supplied int64 IDs only when owner_id is the same Mentor, purpose is LECTURE and course_id matches request path.

## Tables write

- lessons — INSERT with request title/order, decimal-string content, explicit `PUBLISHED` status and database-clock timestamps.
- lesson_uploads — INSERT each validated upload ID with a zero-based position from asset_refs, in the same transaction as lessons; empty refs create no link rows.
- uploads/resources — no write in #47; API #47 reads uploads metadata and does not create resource rows.

## Mục chú ý

- `asset_refs` is a required string containing JSON text for an ordered array of UploadAsset int64 IDs.
- Empty array `[]` is valid; duplicate IDs are rejected; resolved `assets[]` preserve request order.
- API #47 may resolve only assets owned by the same Mentor with purpose `LECTURE` and the same course ID.
- Request `content` remains signed int64; runtime converts it to its base-10 string for `lessons.content` and response `data.content`.
- Course status is not a creation predicate; the new lesson status is `PUBLISHED`.

## Assumptions

- API #34 persists `uploads.id` as BIGINT and complete UploadAsset metadata in the legacy schema artifact; live DB is not verified.
- Asset metadata is resolved from uploads; ordered association is stored in lesson_uploads for API #48. API #47 does not insert into resources or mutate uploads.
- Legacy lessons mapping and direct-owner course predicate are the checked-in source implementation; live schema compatibility remains unverified.

## Conflicts

- Legacy BIGINT DDL and V1-PILOT UUID/versioned schema differ; live schema remains unverified.
- Route/module/tests verify local source behavior only; no live database or migration behavior is claimed.

## Security note

- Parse IDs from `asset_refs`; never trust request URLs or client-provided asset metadata.
- Do not expose assets belonging to another Mentor, purpose or course.

## Performance note

- Parse references once and batch resolve non-empty IDs; preserve output order using the submitted ID order.
- Empty array returns `assets: []` and requires no asset lookup.

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
