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
| Authorization | Role Admin là DIRECT; runtime dùng shared `validate_current_user_request(..., role="ADMIN")`; finer-grained Admin policy chưa được xác minh. |
| Direct request | Query `reason?:string`, `severity?:string`, `page?:int32`; không body. |
| Direct response | HTTP 200 `ApiEnvelope<Page<Discussion>>`. |
| Direct errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 500 `DESIGN_INTERNAL_ERROR`. |
| AC-37 step | Mở queue → đọc reports + discussion summary → mở API #98 detail. |
| Runtime state | Wired locally; 15 focused HTTP tests pass. Report migration is a DERIVED candidate; live schema/deployment and report ingestion are unverified. |
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
| `discussion_reports` | Xác định reported state, reason/severity filter và thứ tự queue | Study-local BIGINT migration fallback; report state/filter policy `DERIVED`; live deployment and writer are unverified. |
| `discussions` | Discussion summary | Legacy DDL candidate; `title` is derived from normalized content; nullable course/user fields cause safe 500 projection failure. |
| `users` | Author projection | Legacy join `users.id = discussions.user_id`; live schema unverified. |
| `discussions` self-reference | Comments | Queue summary returns `comments=[]`; #98 owns full thread detail. |

## Tables write

- N/A — GET read-only; không có INSERT/UPDATE/DELETE hoặc provider side effect.

## Mục chú ý

- `reason` và `severity` dùng exact-match AND trên cùng report đang `OPEN` hoặc `IN_REVIEW`; không giới hạn taxonomy.
- `page` mặc định `1`, size cố định `20`, count theo Discussion duy nhất, sort theo report mới nhất rồi `discussion_id` giảm dần; các quy tắc này là `DERIVED`.
- AC-37 diagram yêu cầu đọc report cùng summary, còn `Discussion` không có report fields. Không thêm trường response ngoài catalog.
- Reusable `Discussion.title` được tạo từ nội dung đã gộp whitespace, tối đa 120 ký tự; comment không được nạp trong list summary.
- `014_discussion_reports.sql` là schema fallback trong Study DB; chưa có endpoint ghi report trong phạm vi #97.

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
