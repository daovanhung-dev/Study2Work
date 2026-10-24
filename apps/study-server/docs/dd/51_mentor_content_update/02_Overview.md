---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "51"
api_name: "Cập nhật nội dung Mentor"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #51 |
| Module | MENTOR / TEACHING |
| Method | PUT |
| Endpoint | `/api/v1/mentor/content/{content_id}` |
| Purpose | Cập nhật một Content và version theo AC-22. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Mentor phải có quyền quản lý course chứa Content; cơ chế identity/assignment chưa có source runtime. |
| Basis | Catalog + AC-22 diagram; body/version details partly `DERIVED`. |
| Status | Draft — Needs Confirmation; API chưa được wire. |
| Transaction | Content và version cần thay đổi nguyên tử theo đề xuất; physical transaction mapping chưa xác định. |
| Side effects | `UPDATE Content + version`; sau đó client reload cây. |

## Sources

- [API catalog #51](../../../../../docs/lists/list_api.md) — path-only contract, response và exact error set.
- [AC-22 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) và page AC-22 trong `AC_03_MENTOR_TEACHING.drawio` — Mentor quản lý course; PUT cập nhật Content + version rồi reload cây.
- [API #50 create DD](../50_mentor_content_create/02_Overview.md) — nguồn các trường nội dung `content_type`, `title`, `payload` và đề xuất review lifecycle.
- [AC-33 moderation diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — queue đọc Content `PENDING_REVIEW`, Admin đọc content/version/author.
- [Legacy DB guide](../../diagrams/DB_UNICA_TABLES.md), [legacy DDL](../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — schema boundary; không xác nhận live schema.
- Current router, middleware, tests and response helpers under `apps/study-server/app/` — current implementation evidence.

## Tables read

- Logical `Content` by `content_id` — physical relation `SOURCE_REQUIRED`.
- Owning course and Mentor access relation — legacy `courses` candidate only, `DERIVED`.
- Current Content version/revision — relation and column `SOURCE_REQUIRED`.

## Tables write

- Logical Content current revision — AC-22 update intent; physical mapping `SOURCE_REQUIRED`.
- Logical version history/state — AC-22 says “+ version”; physical relation and revision semantics `SOURCE_REQUIRED`.

## Mục chú ý

- Catalog and AC-22 both omit a request body for this PUT. The update operation cannot be programmed from the path alone; proposed body is documented separately as `DERIVED`, not as approved contract.
- Proposed complete replacement body contains `content_type`, `title`, and `payload`, reusing API #50's content-bearing fields. `course_id`, `status`, `parent_id`, `order`, and `id` are treated as server-managed in this proposal.
- Proposed revision enters `PENDING_REVIEW`; a previously published revision remains active until the new revision is approved/published. This is a simple lifecycle proposal, not a direct diagram rule.
- No `version` field exists in the reusable `Content` response; version effect is not exposed in response unless the catalog changes.

## Assumptions

- Full replacement of `content_type/title/payload` is the candidate PUT semantics (`DERIVED`).
- Each successful update creates a new logical revision and moves it to `PENDING_REVIEW` (`DERIVED` from AC-22 update/version plus AC-33 pending queue).
- Content identity, course, tree placement and publish state are not accepted from this proposed request body.

## Conflicts

- Request body omission vs PUT and diagram `UPDATE Content + version`: `DISCREPANCY`; contract owner should confirm field list and requiredness.
- Generic Content/version physical schema absent or incompatible in available DDL; no executable UPDATE SQL can be approved.
- AC-33 approval says `APPROVED/PUBLISHED`, while AC-22 has a separate Mentor publish API #52. Their publication-state interaction remains a group-level open question.

## Security note

Load the target Content and its owning course before mutation; authorize Mentor against the stored course, never trust client-supplied owner/course. Exact principal binding and assigned-course support are unresolved.

## Performance note

Use one target lookup and a bounded atomic version write once schema is selected. Do not add a version scan or history query without a source-backed index/model.

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
