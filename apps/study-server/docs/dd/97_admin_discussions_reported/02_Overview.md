---
title: "Overview"
order: 2
dd_id: "97"
api_name: "Lấy reported discussions"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #97 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-37 |
| Method | GET |
| Endpoint | `/api/v1/admin/discussions/reported` |
| Purpose | Lấy hàng đợi discussion đã được báo cáo để Admin xem xét. |
| Consumer/Actor | Admin |
| Authentication | Bearer JWT |
| Authorization | Role Admin là DIRECT theo catalog; Admin guard/claim policy chưa có trong Study source. |
| Direct request | Query `reason?:string`, `severity?:string`, `page?:int32`; không body. |
| Direct response | HTTP 200 `ApiEnvelope<Page<Discussion>>`. |
| Direct errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 500 `DESIGN_INTERNAL_ERROR`. |
| AC-37 step | Mở queue → đọc reports + discussion summary → mở API #98 detail. |
| Runtime state | `UNWIRED / NOT_FOUND`; chưa có route/module/test #97. |
| Side effects | Read-only; không cập nhật discussion, report hoặc audit. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — #97, `PageMeta`, `Page<Discussion>`, `Discussion`, `DiscussionComment`, `UserSummary`.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, precondition, postcondition và AC-37 API mapping.
- [AC-37 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — queue, đọc reports + discussion summary và chuyển sang #98.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md), [DB ERD](../../diagrams/DB_UNICA_ERD.drawio), [legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate discussions/users schema; không chứng minh live schema.
- [API #39 DD](../39_discussions/00_Cover.md), [API #42 DD](../42_discussions_detail/00_Cover.md) — discussion projection, Page semantics và title/schema gaps.
- [Admin moderation DDs #78–#81](../78_admin_content_pending/00_Cover.md) — Admin guard/source boundary and explicit logical-versus-physical mapping pattern.
- [API #96 DD](../96_admin_notifications_status/00_Cover.md) — read-only Admin endpoint precedent; its data model does not transfer to AC-37.
- [Current router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py) — current route/auth/error boundary.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — envelope/error representation.

## Tables read

| Relation/source | Mục đích | Basis/status |
|---|---|---|
| Logical report record | Xác định reported state, reason/severity filter | AC-37 logical read; physical relation/key `SOURCE_REQUIRED`. |
| `discussions` | Candidate Discussion summary | Legacy DDL artifact; not reported selector, title absent, live status unverified. |
| `users` | Candidate author projection | Legacy schema candidate; required join/null behavior unresolved. |
| `discussions` self-reference | Candidate comment rows | Physical candidate only; queue projection extent unresolved. |

## Tables write

- N/A — GET read-only; không có INSERT/UPDATE/DELETE hoặc provider side effect.

## Mục chú ý

- `reason`, `severity` là optional string theo catalog; enum/taxonomy, matching và kết hợp filter chưa được đặc tả.
- `PageMeta` yêu cầu `page`, `size`, `total`, `total_pages`, nhưng request chỉ nêu `page` optional và không có default/size/order.
- AC-37 diagram yêu cầu đọc report cùng summary, còn `Discussion` không có report fields. Không thêm trường response ngoài catalog.
- Reusable `Discussion.title` là bắt buộc nhưng legacy DB guide/DDL không có cột `title`.
- Không có query filter trạng thái/root/comment nào được suy ra trực tiếp từ AC-37.

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
