---
title: "Overview"
order: 2
dd_id: "80"
api_name: "Phê duyệt nội dung"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | **#80** |
| Module | **ADMIN / SYSTEM MANAGEMENT — AC-33** |
| Method | **PATCH** |
| Endpoint | **/api/v1/admin/content/{content_id}/approve** |
| Purpose | Phê duyệt Content được chọn trong hàng đợi moderation theo AC-33. |
| Consumer/Actor | **Admin** |
| Authentication | **Bearer JWT** |
| Authorization | Role Admin theo catalog; guard, claim mapping và scope chưa có trong Study source. |
| Basis | Endpoint, path, response, status và error codes: **DIRECT**; target status, revision selection và physical writes: **SOURCE_REQUIRED**. |
| Status | **Draft — Needs Confirmation**; API chưa được wire trong Study source. |
| Transaction | **TBD**; AC-33 có status update và audit nhưng không chỉ định tính atomic hoặc transaction boundary. |
| Side effects | AC-33 nêu **UPDATE status = APPROVED/PUBLISHED + audit**; nghĩa trạng thái và persistence mapping chưa được quyết định. |

## Sources

- [API catalog và reusable Content schema](../../../../../docs/lists/list_api.md) — row #80, response fields và exact error set.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-33 Admin actor, pending-review precondition và sequence.
- [AC-33 moderation diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — #78 queue → #79 detail → decision → #80 approve → update status plus audit → reload queue.
- [AC-22 Mentor content diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — separate API #52 updates publication status.
- [DD #78 queue](../78_admin_content_pending/02_Overview.md), [DD #79 detail](../79_admin_content_detail/02_Overview.md) and [DD #79 open questions](../79_admin_content_detail/OPEN_QUESTIONS.md) — pending state and version/author identity gaps.
- [DD #52 publish/unpublish](../52_mentor_content_publish/02_Overview.md) and [open questions](../52_mentor_content_publish/OPEN_QUESTIONS.md) — separate publication operation and unresolved interaction with Admin approval.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — no generic Content/review relation.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID content/version/decision artifacts; not a direct BIGINT Content mapping.
- [Current Study router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py) and [response helper](../../../app/core/responses.py) — no API #80 route, no Admin guard, absent middleware path and current error envelope behavior.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — common envelope and expected error data=null convention.

## Tables read

| Logical/physical source | Purpose | Basis/status |
|---|---|---|
| Logical Content | Resolve the path-selected item and fields required by response | Logical lookup intent; physical relation/key SOURCE_REQUIRED. |
| Logical Content review state | Check that the item is eligible for an approval action | AC-33 precondition is pending review; exact state check DERIVED. |
| Logical Content revision | Keep the decision bound to the version shown in #79 | Revision identity and selector SOURCE_REQUIRED. |
| Admin principal | Determine role and audit actor | Role requirement direct; claim and identity mapping SOURCE_REQUIRED. |
| V1-PILOT content_review_decisions | Compare available pilot decision artifact | UUID revision/reviewer model; not selected as #80 physical source. |

## Tables write

| Logical target | Intended effect | Basis/status |
|---|---|---|
| Content review/publication state | Update after approve branch | AC-33 logical effect direct; exact target and physical relation/column unresolved. |
| Review audit/decision | Record approval audit | AC-33 logical effect direct; physical relation/fields and atomicity SOURCE_REQUIRED. |

## Mục chú ý

- Catalog #80 declares path content_id:int64! only; it has no body/query, revision ID or expected row version.
- AC-33 says APPROVED/PUBLISHED in one node; AC-22 has a separate Mentor API #52 for publication status. Do not treat these states as one approved transition rule.
- Catalog response is one Content with eight fields. AC-33 detail also reads version/author, but reusable Content schema contains neither; do not add fields.
- Catalog allows 422 DESIGN_VALIDATION_ERROR but does not define its trigger.
- Study workflow delivers Markdown only; this package has no ZIP.

## Assumptions

- No physical Content, review, audit table or column is selected in this DD.
- Response meta:{} is a proposal for this non-paginated singleton response; exact null/empty convention remains to align with runtime.
- The 422 code is retained as declared, while its condition remains open.

## Conflicts

- AC-33 approve effect APPROVED/PUBLISHED is ambiguous beside AC-22 API #52 publication update.
- AC-33 reads version/author but #80 request and response do not identify or return a revision/author.
- Legacy DDL lacks generic Content; V1-PILOT decision rows use UUID resource_version_id and cannot be mapped directly to Content int64.
- Current Study source has no Admin guard, #80 route or middleware allowlist path. The error helper returns {} when error data is not passed, while API guidelines expect null.

## Security note

Require Bearer JWT and Admin role before exposing or changing Content. Resolve the authenticated Admin identity from an approved claim policy; do not accept actor identity from request data. The current Study helper is Student-only, so no implementation guard is implied here. Keep version/audit information and any author projection behind an explicit response allowlist.

## Performance note

No physical query plan or index is prescribed because the Content and revision schema is not selected. The logical flow targets one Content and its reviewable revision; batching and lock strategy remain open.
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
