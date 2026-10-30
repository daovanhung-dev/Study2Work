---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "53"
api_name: "Xóa nội dung Mentor"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #53 |
| Module | MENTOR / TEACHING |
| Method | DELETE |
| Endpoint | /api/v1/mentor/content/{content_id} |
| Purpose | Soft-delete Content khi được phép; kiểm tra dependency trước mutation. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | role=Mentor và quyền quản lý course chứa Content theo AC-22; principal/assignment mapping chưa có source. |
| Basis | Contract và soft-delete effect DIRECT; dependency/status/history proposals DERIVED. |
| Status | Draft — Needs Confirmation |
| Transaction | View sở hữu transaction; commit sau khi `DeleteResult` được validate, rollback khi lỗi. |
| Side effects | Ghi `contents.deleted_at = CURRENT_TIMESTAMP`; không hard-delete, cascade hoặc reparent. Child/PUBLISHED guards là DERIVED; trả DeleteResult và client reload cây. |

## Sources

- Catalog row #53, Content và DeleteResult: [list_api.md](../../../../../docs/lists/list_api.md).
- AC-22: [AC_03_MENTOR_TEACHING.drawio](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio).
- AC-33: [AC_04_ADMIN_MANAGEMENT.drawio](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio).
- Related APIs #49–#52: [#49](../49_mentor_content_list/02_Overview.md), [#50](../50_mentor_content_create/02_Overview.md), [#51](../51_mentor_content_update/02_Overview.md), [#52](../52_mentor_content_publish/02_Overview.md).
- Current route/middleware: [v1.py](../../../app/api/v1.py), [middleware.py](../../../app/core/middleware.py).
- Legacy and pilot schema: [DB.sql](../../../../../infra/postgres/study-server/DB.sql), [02_study_db.sql](../../../../../infra/postgres/02_study_db.sql).
- Study DD workflow: [README.md](../../../../../.agents/server-study/workflows/README.md).

## Tables read

- Content target and owning course map to local `contents`/`courses`; live schema remains unverified.
- Direct child and active-row predicates map to `contents.parent_id` and `deleted_at IS NULL`; child-block policy remains DERIVED.

## Tables write

- API #53 updates local `contents.deleted_at`; migration deployment remains unverified.
- Content version/review history: no physical mutation proposed; retain history is DERIVED.

## Mục chú ý

- Catalog declares path content_id only; no body or query.
- AC-22 directly says DELETE/soft delete Content, then reload content tree.
- Content.parent_id is the only explicit generic parent-child relation.
- Proposed child dependency returns catalog 422 without cascade or reparent.
- Proposed PUBLISHED gate requires API #52 unpublish first so #52 remains publication-state owner.
- DeleteResult.status is literal deleted. No ContentStatus=DELETED is invented; the local implementation uses nullable `contents.deleted_at` as the tombstone.
- Current Study source has a DELETE route, module, middleware contract mapping (shared path template with PUT), and fake-DB HTTP tests. These establish local behavior only, not live DB/deployment.

## Assumptions

- A non-deleted child whose parent_id equals the target blocks deletion with 422; no cascade/reparent. This is DERIVED and avoids an invalid active tree in current API #49.
- PUBLISHED content returns 422 and must be unpublished through API #52 first; DERIVED proposal.
- Non-PUBLISHED statuses are currently deletable under the DERIVED fallback; queue withdrawal and review policy remain open.
- Soft delete writes `deleted_at` using database `CURRENT_TIMESTAMP`; local active API #49 excludes the target. History retention is not mutated, but formal retention/audit policy remains open.
- Exact deletion eligibility for pending/rejected/approved content requires confirmation.

## Conflicts

- Catalog says conditional delete/check dependency but does not define dependency types or policy.
- AC-22 does not define physical tombstone fields, status gate, cascade behavior or repeat-delete behavior.
- Catalog Content uses BIGINT IDs; pilot content_blocks uses UUID and lesson_id, so it is not a compatible generic Content model.
- AC-22 requires course management permission; current Study auth does not provide Mentor identity/assignment mapping.

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
