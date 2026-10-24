---
title: "Overview"
order: 2
dd_id: "98"
api_name: "Lấy đầy đủ thread + report detail"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #98 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-37 |
| Method | GET |
| Endpoint | `/api/v1/admin/discussions/{discussion_id}` |
| Purpose | Đọc thread discussion và report detail để Admin quyết định giữ, ẩn, khóa hoặc chuyển sang API moderation/delete. |
| Consumer/Actor | Admin |
| Authentication | Bearer JWT |
| Authorization | Role Admin là DIRECT theo catalog; guard/claim/policy chưa có trong Study source. |
| Direct request | Path `discussion_id:int64!`; không body/query. |
| Direct response | HTTP 200 `ApiEnvelope<Page<Discussion>>`. |
| Direct errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR`. |
| AC-37 position | Sau queue #97; đọc discussion/comments/reports trước policy decision và nhánh #99/#100. |
| Runtime state | `UNWIRED / NOT_FOUND`; không có route/module/test #98. |
| Side effects | Read-only; không dismiss report, moderate, delete hoặc ghi audit. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — #98, `PageMeta`, `Page<Discussion>`, `Discussion`, `DiscussionComment`, `UserSummary`, analytics `Report`.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, precondition, postcondition và AC-37 mapping.
- [AC-37 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — #97 queue → #98 detail → read discussion/comments/reports → decision → #99/#100.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md), [DB ERD](../../diagrams/DB_UNICA_ERD.drawio), [legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate discussion/self-reference/users fields; không chứng minh live schema.
- [API #97 DD](../97_admin_discussions_reported/00_Cover.md) — queue contract, report source/response gap and pending cross-API review.
- [API #42 DD](../42_discussions_detail/00_Cover.md) — `Page<Discussion>` one-thread proposal and direct-child comment precedent; Student ACTIVE filters do not transfer to Admin moderation.
- [Admin moderation DDs #78–#81](../78_admin_content_pending/00_Cover.md) — Admin guard/source boundary and logical-vs-physical mapping.
- [Current router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py) — route/auth/error boundary.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — envelope/error representation.

## Tables read

| Relation/source | Mục đích | Basis/status |
|---|---|---|
| Logical discussion report | AC-37 report detail | Diagram logical read; physical relation/key `SOURCE_REQUIRED`. |
| `discussions` | Candidate target and thread rows | Legacy DDL only; title absent; nullable FK; live status unverified. |
| `users` | Candidate `UserSummary` projection | Legacy schema candidate; author join/null behavior unresolved. |
| `discussions` self-reference | Candidate direct comments | `parent_id` design; target root/reply and comment extent unresolved. |

## Tables write

- N/A — GET read-only; không có INSERT/UPDATE/DELETE hoặc audit/provider side effect.

## Mục chú ý

- AC-37 node n5 yêu cầu đọc reports, nhưng catalog response chỉ là `Page<Discussion>`. `Discussion` không có reason/severity/reporter/report timestamp.
- Catalog `Report` là schema analytics (`period`, `metrics`, `generated_at`), không phải discussion-report schema; không dùng thay thế.
- `PageMeta` cần page/size/total/total_pages dù request chỉ có path ID. Đề xuất one-item page theo #42 được gắn `DERIVED`.
- Discussion `title` bắt buộc nhưng không có cột trong legacy DB guide/DDL; không suy từ content.
- Không sao chép `ACTIVE` filter của Student #42 sang Admin. AC-37 phải cho phép Admin kiểm tra nội dung đang cần moderation; exact status eligibility vẫn cần xác nhận.

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
