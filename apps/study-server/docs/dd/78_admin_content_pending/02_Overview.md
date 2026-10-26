---
title: "Overview"
order: 2
dd_id: "78"
api_name: "Lấy pending content"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #78 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-33 |
| Method | GET |
| Endpoint | `/api/v1/admin/content/pending` |
| Purpose | Đọc hàng chờ Content có trạng thái `PENDING_REVIEW`. |
| Consumer/Actor | Admin |
| Authentication | Bearer JWT |
| Authorization | Catalog yêu cầu Admin; runtime dùng shared `ADMIN` guard. Permission moderation riêng chưa được xác minh. |
| Direct request | Query `type?:string`, `course?:int64`, `page?:int32`; không body. |
| Direct response | HTTP 200 `ApiEnvelope<Content>` theo catalog. |
| Local runtime response | `ApiEnvelope<Page<Content>>` — fallback `DERIVED` để endpoint queue có thể trả danh sách/phân trang. |
| Direct errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 500 `DESIGN_INTERNAL_ERROR`. |
| Local derived validation | 422 `DESIGN_VALIDATION_ERROR` cho `course`/`page` sai kiểu hoặc ngoài miền. |
| AC-33 queue condition | `contents.status=PENDING_REVIEW`; diagram yêu cầu đọc trạng thái này. |
| Runtime state | `SOURCE_BACKED / LOCAL_TESTED`; route, shared Admin guard, module và HTTP tests đã được wire. |
| Side effects | Read-only; không approve/reject, audit-write hoặc cập nhật Content. |

### Discrepancy: danh sách so với response

Tên API, AC-33 queue và query `page` biểu thị collection; catalog vẫn khai báo `ApiEnvelope<Content>` đơn. Runtime dùng `ApiEnvelope<Page<Content>>` theo fallback `DERIVED`, giữ size cố định 20, page mặc định 1 và `id ASC`. Không sửa catalog hoặc diagram; cần owner đồng bộ direct contract. DD vẫn `Draft — Needs Confirmation`.

## Sources

- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-33 actors, precondition và endpoint sequence.
- [AC-33 moderation diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — queue predicate, #79 detail, #80/#81 branches và reload.
- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — #78–#81, Content, Page và PageMeta.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql), [migration 006](../../../../../infra/postgres/study-server/migrations/006_contents.sql), [migration 007](../../../../../infra/postgres/study-server/migrations/007_content_versions.sql) — checked-in legacy candidates; live DB chưa xác minh.
- [Mentor Content #49](../49_mentor_content_list/02_Overview.md), [#50](../50_mentor_content_create/02_Overview.md), [#51](../51_mentor_content_update/02_Overview.md), [#52](../52_mentor_content_publish/02_Overview.md), [#53](../53_mentor_content_delete/02_Overview.md) — current Content projection/lifecycle source.
- [Admin course list #73](../73_admin_courses_list/04_Response.md) — fixed size 20, `id ASC`, empty/out-of-range Page 200 and shared Admin list convention.
- [Admin review #79](../79_admin_content_detail/02_Overview.md), [#80](../80_admin_content_approve/02_Overview.md), [#81](../81_admin_content_reject/02_Overview.md) — linked review/version/audit boundaries remain separate.
- [Current router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py) — local route/auth/error integration.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — envelope and error representation.

## Tables read

| Relation/source | Mục đích | Basis/status |
|---|---|---|
| Legacy `contents` | Current logical Content row and queue source | Checked-in DDL + migrations 006 and current APIs #49–#53; live schema not verified. |
| Legacy `content_versions` | Previous-state snapshots created by API #51 | Migration 007/current code; not joined for queue items. |
| V1-PILOT `content_blocks` | Compare versioned lesson-bound model | UUID model, not mapped to int64 Content API. |
| V1-PILOT `content_review_decisions` | Compare append-only review decision model | UUID revision log, not queue source for this API. |

## Tables write

Không có. API #78 chỉ đọc; approval/rejection/audit thuộc #80/#81 theo AC-33.

## Mục chú ý

- AC-33 directly requires `status=PENDING_REVIEW`; current API #50 creates that status and API #51 sets the current logical Content row to that status after archiving its prior state.
- Runtime filters `contents.deleted_at IS NULL` by DERIVED fallback, consistent with active views in APIs #49/#53. AC-33 does not directly specify deleted-item visibility.
- `type` maps exactly to `content_type`; `course` maps exactly to `course_id`. No enum whitelist, trimming or case normalization is added.
- Page behavior is DERIVED from Admin list API #73: page 1 default, fixed size 20, `id ASC`, count/list share identical filters; no `size`/`sort` query is introduced.
- Queue returns current logical `contents` rows only; it does not join `content_versions` or add author/version/review metadata. Which revision #79–#81 act on remains open.
- `error_response()` defaults error `data` to JSON `null`; the fixed API #78 path is now in `DESIGN_CONTRACT_PATHS`.
- Legacy DDL/migrations and fake-session tests do not verify live schema, deployment, grants or moderation policy.

## Assumptions

- Local response is `ApiEnvelope<Page<Content>>` because the endpoint is a queue and the direct query contains `page`; this is a DERIVED fallback and conflicts with the catalog's singular `Content` response.
- `page` is 1-based/default 1, must fit positive int32, uses fixed size 20 and stable `id ASC`; numeric parse/range failures use derived 422 `DESIGN_VALIDATION_ERROR`.
- Empty queue and pages beyond the last page return HTTP 200 with `items=[]`; no 404 is added.
- Soft-deleted rows are excluded; exact `type`/`course` equality is applied only when supplied.

## Conflicts

- Direct catalog response `ApiEnvelope<Content>` cannot represent the queue/page flow; runtime uses a documented `DERIVED` Page fallback without changing catalog.
- Catalog lists only 401/403/500, while runtime adds 422 for numeric query parsing based on the shared Admin-list validation convention; this error-set discrepancy remains open for contract correction.
- Checked-in legacy `contents`/`content_versions` and current APIs #49–#53 supersede the older DD statement that no generic Content source exists; neither proves live DB state.
- AC-33 does not define deleted/stale visibility, enum members, approval revision identity, Admin moderation permission or live migration/deployment.

## Security note

- Shared Bearer/JWT guard requires role `ADMIN` before parsing numeric query values or reading the queue.
- No author, reviewer, decision history, JWT claim, raw payload internals beyond the reusable Content payload, SQL detail or stack trace is added to the response.
- The shared role does not establish a separate content-moderation permission policy.

## Performance note

- Query uses count plus a bounded 20-row page with `id ASC`; count/list share the same predicates.
- No review-history join or unbounded payload query is added. Query plans/indexes and live schema are unverified.

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
