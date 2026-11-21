---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 19 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | POST |
| Endpoint | /api/v1/courses/{course_id}/enrollments |
| Purpose | Tạo Enrollment cho Student hiện tại và khởi tạo Progress theo AC-12. |
| Consumer/Actor | Student |
| Authentication | Bearer JWT |
| Authorization | role=Student; claim-to-user mapping chưa được chốt cho contract API #19. |
| Basis | DIRECT — approved design contract; AC-12 mô tả flow mutation |
| Status | Draft — Needs Confirmation |
| Runtime status | UNWIRED / NOT_FOUND |
| Transaction | AC-12 yêu cầu tạo Enrollment và INIT Progress trong transaction; chi tiết commit/rollback chưa có runtime source. |
| Side effects | Logical INSERT vào enrollments và một hoặc nhiều INSERT vào lesson_progress; physical runtime chưa được xác minh. |

## Sources

- [list_api.md](../../../../../docs/lists/list_api.md) — API contract, schema Enrollment, ApiEnvelope và business codes.
- [00_AC_API_INDEX.md](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — API #19 được gắn với AC-12.
- [AC_02_STUDENT_LEARNING.drawio](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — precondition, flow và transaction intent.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) — logical purpose, thiết kế cột và trạng thái DESIGN_ONLY.
- [DB_UNICA_ERD.drawio](../../diagrams/DB_UNICA_ERD.drawio) — quan hệ logical trong ERD V1.
- [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — checked-in DDL; không xác nhận schema live.
- [auth.py](../../../app/utils/auth.py) — current Study helper đọc sub và roles; đây không phải implementation của API #19.
- [v1.py](../../../app/api/v1.py), [declared-routes.md](../../../../../.agents/server-study/apis/declared-routes.md) và [tests.md](../../../../../.agents/server-study/tests.md) — current route/test boundary.
- [createDD_MARKDOWN_SKILL.md](../../../../../.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md) và [DD_API_Template_MD](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/) — authoring/template baseline.

## Tables read

- courses — course existence/eligibility is relevant to the API contract, but API #19 lookup conditions are SOURCE_REQUIRED.
- enrollments — logical duplicate/state check by user/course is required by AC-12; exact selection policy is SOURCE_REQUIRED.
- lessons — candidate source for lesson IDs used to initialize progress; lesson selection/cardinality is SOURCE_REQUIRED.

## Tables write

- enrollments — DESIGN_ONLY INSERT for the logical Enrollment.
- lesson_progress — DESIGN_ONLY INSERT for Progress initialization; row count and initial values are SOURCE_REQUIRED.

## Mục chú ý

- AC-12 routes free courses directly to API #19 and routes paid courses there after payment succeeds.
- The API catalog repeats course_id in both path and body and describes user as JWT-sourced without a settled wire-field/claim mapping.
- API #19 is absent from the current Study route, module, query and test surface.
- Checked-in DB.sql and ERD are design evidence; live database metadata is not verified.

## Assumptions

- This deliverable documents API #19 only; it does not implement routes, queries, schema or migrations.
- The endpoint response and listed status/business codes remain as declared in list_api.md.
- AC-12's transaction label applies to both logical mutations; exact physical transaction implementation is not asserted.

## Conflicts

- Catalog user identity is written as user from JWT:string, while Enrollment.user_id is int64 and current Study auth parses numeric JWT sub to int.
- DB_UNICA_TABLES marks enrollment/progress foreign keys required; DB.sql does not declare NOT NULL on those foreign keys.
- AC-12 requires anti-duplicate behavior, but DB.sql has no unique constraint on enrollments(user_id, course_id).
- AC-12 says INIT Progress without identifying the lesson set, row count or initialization values.

## Security note

- Contract requires Bearer JWT and Student role. Do not accept a caller-controlled identity until the contract owner confirms whether user is derived only from JWT or represented in the body.

## Performance note

- Progress initialization may write multiple rows, but the lesson set and expected cardinality are not defined; no query or batch-size policy is asserted.

