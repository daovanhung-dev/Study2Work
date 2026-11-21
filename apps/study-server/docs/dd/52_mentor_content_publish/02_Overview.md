---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "52"
api_name: "Publish/unpublish nội dung Mentor"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #52 |
| Module | MENTOR / TEACHING |
| Method | PATCH |
| Endpoint | /api/v1/mentor/content/{content_id}/publish |
| Purpose | Publish hoặc unpublish Content sau khi kiểm tra readiness theo contract. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | AC-22 requires permission to manage the owning course; local fallback uses direct `courses.mentor_id` ownership, while identity binding/assigned-Mentor policy remain unconfirmed. |
| Basis | Endpoint, path, response, status và errors: DIRECT. Request action/state transition: DERIVED proposal. |
| Status | Draft — Needs Confirmation; local route/module/tests are source-backed, but contract and live schema remain unconfirmed. |
| Transaction | Local fallback locks Content/Course and commits one status update; implementation is DERIVED and live transaction behavior is unverified. |
| Side effects | UPDATE publication status theo AC-22; sau đó caller reload content tree. |

## Sources

- [API catalog #52](../../../../../docs/lists/list_api.md) — method/path/auth/path/response/success/errors và reusable Content.
- [AC-22 API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) và [AC-22 diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — Mentor course permission; PATCH → UPDATE publication status → reload tree.
- [AC-33 moderation diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — moderation queue đọc PENDING_REVIEW; approval node ghi APPROVED/PUBLISHED + audit; ý nghĩa kết hợp chưa rõ.
- [DD #49](../49_mentor_content_list/02_Overview.md), [DD #50](../50_mentor_content_create/02_Overview.md), [DD #51](../51_mentor_content_update/02_Overview.md) — Content tree, create, update/version và lifecycle proposals.
- [Legacy DDL](../../../../../infra/postgres/study-server/DB.sql) và [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — schema boundary; không xác nhận live schema.
- Current Study router, middleware, modules and tests under apps/study-server — local implementation and error-code wiring; fake DB tests do not verify live schema.

## Tables read

- Local fallback reads `contents` and its current `status`; physical revision selector/live availability remain SOURCE_REQUIRED.
- Owning course and Mentor access relation — legacy courses.mentor_id is only a DERIVED candidate.
- Type-specific readiness data — SOURCE_REQUIRED; no approved ContentType/payload schema.

## Tables write

- Local fallback updates `contents.status`; AC-22's logical status effect is DIRECT, while physical schema availability and transition policy remain unverified/DERIVED.
- No content revision or payload write is proposed; this is DERIVED separation from API #51's UPDATE Content + version.

## Mục chú ý

- Catalog and AC-22 both declare only path content_id. They do not define how the client selects publish versus unpublish.
- This DD proposes body {published:boolean!} as DERIVED so the client sends a target state rather than triggering an ambiguous toggle. This proposal is not the canonical catalog contract.
- Implemented local fallback: APPROVED to PUBLISHED after the status readiness gate; PUBLISHED to APPROVED on unpublish; repeated target is a no-op. These state rules are DERIVED and require review.
- The status gate is the only available readiness signal. ContentType-specific payload, asset, and revision readiness are not checked because no approved schema/rules exist.
- AC-33 approval writes status = APPROVED/PUBLISHED + audit. It does not make clear whether approval itself publishes content. Resolve this with #50, #51, #53 and the AC-33 owner.
- Local `contents.status` supports storing an open state string, but exact readiness checks, ContentStatus enum, version/current revision model and live schema are not approved/verified.
- Local route and fake DB HTTP tests now exist. This does not establish deployed behavior or live schema availability.

## Assumptions

- A required boolean target state is the implemented DERIVED fallback for the two actions in the API title; confirm or replace it in the canonical catalog before treating it as approved.
- Only an approved logical revision can be published; unpublish returns its state to approved. Both transitions are DERIVED.
- Publishing changes publication status only and does not create a content version; DERIVED from the AC-22 diagram's status-only operation and API #51's separate version update.
- Same-target requests return current Content without a second mutation; this idempotency rule is DERIVED.

## Conflicts

- Publish/unpublish intent is not represented in the declared path-only request: DISCREPANCY.
- AC-33 combines APPROVED/PUBLISHED in one approval node while AC-22 has a separate publish API: DISCREPANCY / MACRO_REVIEW.
- ContentStatus and readiness rules are undefined; local BIGINT `contents` has no version-history relation and live schema is unverified.
- Mentor identity/assignment mapping is not source-backed.
- Catalog and AC-22 still omit the implemented request body: DISCREPANCY.
- The middleware allowlist now includes API #52 and local tests confirm its design validation code; live error behavior remains unverified.

## Security note

Authenticate Bearer JWT and require Mentor. Load the target Content and authorize against its stored course; do not accept a course or owner identifier from the proposed request body. Principal mapping and assigned-course policy remain SOURCE_REQUIRED.

## Performance note

The logical flow needs one target-state read, one access/readiness decision and at most one status update. No physical query or index can be prescribed until the Content model and live schema are approved.

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
