---
title: "Overview"
order: 2
dd_id: "81"
api_name: "Từ chối nội dung"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | **#81** |
| Module | **ADMIN / SYSTEM MANAGEMENT — AC-33** |
| Method | **PATCH** |
| Endpoint | **/api/v1/admin/content/{content_id}/reject** |
| Purpose | Từ chối Content được chọn trong hàng đợi review và ghi nhận lý do theo AC-33. |
| Consumer/Actor | **Admin** |
| Authentication | **Bearer JWT** |
| Authorization | Role Admin theo catalog; guard, claim mapping và moderation scope chưa có trong Study source. |
| Basis | Method/path/auth/input/response/status/errors: **DIRECT**; eligibility check, persistence mapping và audit parity: **SOURCE_REQUIRED/DERIVED**. |
| Status | **Draft — Needs Confirmation**; API chưa được wire trong Study source. |
| Transaction | **TBD**; status update và review reason có một logical outcome nhưng physical transaction boundary chưa có nguồn. |
| Side effects | AC-33 ghi **UPDATE status = REJECTED + review reason**; physical relation/columns chưa được chọn. |

## Sources

- [API catalog và reusable Content schema](../../../../../docs/lists/list_api.md) — row #81, Content fields and exact errors.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-33 Admin actor, pending-review precondition and API sequence.
- [AC-33 moderation diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — #78 queue → #79 detail → reject branch with reason → #81 status/reason update → reload #78.
- [DD #78 queue](../78_admin_content_pending/02_Overview.md), [mapping](../78_admin_content_pending/05_Data_Mapping.md) and [open questions](../78_admin_content_pending/OPEN_QUESTIONS.md) — PENDING_REVIEW queue predicate, response cardinality and revision selection.
- [DD #79 detail](../79_admin_content_detail/02_Overview.md) and [open questions](../79_admin_content_detail/OPEN_QUESTIONS.md) — version/author read intent and stable revision identity gap.
- [DD #80 approve](../80_admin_content_approve/02_Overview.md) and [open questions](../80_admin_content_approve/OPEN_QUESTIONS.md) — separate approval status/audit effects and shared revision questions.
- [DD #52 publish/unpublish](../52_mentor_content_publish/02_Overview.md) and [DD #53 delete](../53_mentor_content_delete/02_Overview.md) — Content lifecycle interactions still proposed.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — no generic Content/review relation.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID content/review artifacts; not direct mapping for catalog Content int64.
- [Current Study router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py) — route/Admin guard/path allowlist absence and current error envelope behavior.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — common envelope and expected error data:null convention.

## Tables read

| Logical/physical source | Purpose | Basis/status |
|---|---|---|
| Logical Content | Resolve the path-selected item and response projection | Logical lookup intent; physical relation/key SOURCE_REQUIRED. |
| Logical Content review state | Determine whether the item is still eligible for rejection | AC-33 pending precondition direct; recheck behavior DERIVED/open. |
| Logical Content revision | Bind rejection to the revision Admin saw in #79 | Revision identity/selector SOURCE_REQUIRED. |
| Admin principal | Authorize the caller and identify the reviewer | Admin role direct; claim/identity mapping SOURCE_REQUIRED. |
| V1-PILOT content_review_decisions | Compare existing pilot decision artifact | UUID revision/reviewer model; not selected as physical source for #81. |

## Tables write

| Logical target | Intended effect | Basis/status |
|---|---|---|
| Content review status | Set status to REJECTED | AC-33 logical effect direct; physical relation/column and state owner unresolved. |
| Rejection reason | Store request reason with the review outcome | AC-33 logical effect direct; physical field/relation unresolved. |
| Separate review audit event | Not explicitly stated in reject node | Do not assume an additional append; parity with #80 needs confirmation. |

## Mục chú ý

- Catalog declares path content_id:int64! and body reason:string!; no query parameters.
- No reason maximum length, trim rule, blank-value rule, enum or reason code list is declared.
- Catalog response is one Content with eight fields. It has no review_reason, reviewer, version or audit field; do not add any.
- AC-33 queue filters PENDING_REVIEW. After status becomes REJECTED, the item no longer satisfies that logical predicate and should be absent from the reloaded queue; this outcome follows the two direct diagram steps.
- #80 says “+ audit”; #81 says “+ review reason”. Do not silently add a separate audit write to #81.

## Assumptions

- A request body object is sent as application/json, following the catalog body schema and existing Study API DD convention.
- A successful Content projection reports the resulting logical status REJECTED; physical source remains unresolved.
- The required marker means reason must be present; whitespace-only/length/content policy is not inferred.

## Conflicts

- AC-33 asks to store a review reason, but the reusable Content response has no reason field. The reason's persistence and client visibility are unresolved.
- #80 explicitly writes audit, while #81 explicitly writes status and review reason but does not mention an audit append.
- #78/#79/#80/#81 identify the target only by content_id; AC-33 detail reads version, so a stale revision can be acted upon without a version selector in the request.
- Legacy DDL lacks generic Content; V1-PILOT review decisions use UUID resource_version_id and do not directly map to Content int64.
- Current Study source has no API #81 route or Admin guard; the path is absent from middleware allowlist. Current error helper defaults absent error data to {} while guidelines expect null.

## Security note

Require Bearer JWT and Admin role before exposing or changing Content. Resolve reviewer identity from an approved claim policy; do not accept it from the request body. Restrict review reason and any audit details to the approved response projection. Current Study helper is Student-only; no Admin implementation is implied.

## Performance note

No physical query, lock, index or transaction plan is prescribed because Content/revision schema is not selected. Logical processing targets one Content and the revision shown in #79.
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
