---
title: "Overview"
order: 2
dd_id: "79"
api_name: "Lấy chi tiết content và metadata review"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #79 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-33 |
| Method | GET |
| Endpoint | `/api/v1/admin/content/{content_id}` |
| Purpose | Đọc chi tiết Content được chọn từ hàng đợi review. |
| Consumer/Actor | Admin |
| Authentication | Bearer JWT |
| Authorization | Catalog yêu cầu role Admin; runtime dùng shared `validate_current_user_request(..., role="ADMIN")`; policy moderation riêng chưa có. |
| Direct request | Path `content_id:int64!`; không body/query. |
| Direct response | HTTP 200 `ApiEnvelope<Content>` theo catalog. |
| Direct errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR`. |
| AC-33 sequence | #78 queue → #79 detail → #80 approve hoặc #81 reject → reload #78. |
| Runtime state | `SOURCE_BACKED_LOCALLY / WIRED`; route/module/focused HTTP tests có trong Study source. |
| Side effects | Read-only; không quyết định duyệt, ghi decision/audit hoặc đổi Content status. |

### Discrepancy: metadata review so với response schema

AC-33 node n6 yêu cầu backend đọc `content/version/author`. Catalog #79 trả `Content`; reusable schema có tám field Content nhưng không định nghĩa version hoặc author. Runtime hiện trả trực tiếp Content theo catalog. Không thêm metadata vào `data` hoặc giả định rằng metadata nằm trong `payload`. `content_versions` lưu snapshot cũ nhưng request #79 không chọn revision; `archived_by` là updater khi snapshot được ghi, không phải tác giả Content. Cần xác nhận metadata chỉ là dữ liệu nội bộ hay catalog cần projection response khác.

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — row #79, Content fields và exact errors.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-33 actor, precondition và endpoint sequence.
- [AC-33 moderation diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — n5 gọi #79; n6 đọc content/version/author; n7 rẽ sang #80/#81.
- [DD #78 — pending queue](../78_admin_content_pending/02_Overview.md), [mapping](../78_admin_content_pending/05_Data_Mapping.md), [open questions](../78_admin_content_pending/OPEN_QUESTIONS.md) — queue predicate và revision identity chưa chốt.
- [DD #69 — Admin user detail](../69_admin_user_detail/04_Response.md) — giữ singleton response ApiEnvelope<UserProfile> theo catalog; không dùng schema user làm Content precedent.
- [DD #74 — Admin course detail](../74_admin_course_detail/04_Response.md) — Page singleton là proposal của API #74 vì catalog khai báo Page, không áp dụng cho #79.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql), migrations 006/007 và [legacy DB table guide](../../diagrams/DB_UNICA_TABLES.md) — có `contents`/`content_versions` candidate; không có Content creator/author field.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID content blocks/version/decision artifacts; không map trực tiếp sang Content BIGINT.
- [Current router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py) — route wired after static #78 route, shared ADMIN guard, middleware path template, error data null.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — envelope và error data convention.

## Tables read

| Logical/physical source | Mục đích | Basis/status |
|---|---|---|
| `contents` | Current Content row theo path content_id | Checked-in legacy candidate; APIs #49–#53 dùng; live availability chưa xác minh. |
| `content_versions` | Snapshot Content state trước update | API #51/migration 007; #79 không có revision selector. |
| Content author | AC-33 yêu cầu đọc tác giả | Không có creator field; `archived_by` là updater, không phải author; mapping SOURCE_REQUIRED. |
| Legacy courses, lessons, resources | So sánh khả năng mapping | Không suy ra author từ course mentor hoặc relation lân cận. |
| V1-PILOT course_versions, lessons, content_blocks | So sánh versioned content model | UUID/version-scoped; là schema artifact, không phải live proof. |
| V1-PILOT content_review_decisions | Phân biệt reviewer/decision với author | Append-only decision log theo UUID resource_version_id; không phải Content detail source. |

## Tables write

Không có. #79 chỉ đọc; approve/reject và audit thuộc #80/#81 theo AC-33.

## Mục chú ý

- Catalog định danh Content bằng content_id:int64; pilot content_blocks.id và resource_version_id dùng UUID.
- AC-33 n6 nói đọc version/author nhưng catalog Content không có hai field này.
- #78 lọc queue bằng status=PENDING_REVIEW; AC-33 không xác định #79 có phải lọc lại status hay trả trạng thái hiện tại của ID.
- #80/#81 chỉ nhận content_id, không có version ID hoặc expected row version trong catalog; quyết định áp dụng lên revision nào chưa rõ.
- Không lấy reviewer_subject_id làm author; đó là metadata người review trong pilot decision log.

## Assumptions

- Candidate Q1 tìm current active `contents` row theo ID và trả status hiện tại; không áp dụng thêm `PENDING_REVIEW` filter cho #79. Đây là DERIVED; stale queue behavior vẫn mở.
- Không có count, pagination, Page, write, audit hoặc extra business code.
- Runtime `error_response()` mặc định error `data` là JSON `null`.

## Conflicts

- “Metadata review”/AC-33 n6 yêu cầu content/version/author, trong khi direct response là ApiEnvelope<Content> không có version/author.
- Legacy `contents`/`content_versions` là checked-in candidates và current APIs #49–#53 dùng chúng; live schema chưa xác nhận. V1-PILOT UUID content blocks không thay thế trực tiếp.
- Stable identity của queue row, detail và approve/reject giữa các revision chưa được xác định.
- Runtime dùng shared ADMIN role guard và allowlist route template #79; moderation permission riêng vẫn SOURCE_REQUIRED.

## Security note

- Xác thực Bearer và shared ADMIN role trước Content read; không query/return version hoặc author khi chưa có selector/identity mapping.
- Không trả raw review comments, reviewer identity, author PII hoặc database errors ngoài contract.
- Nếu owner yêu cầu version/author trong response, cần schema, revision identity, field allowlist và PII policy trước khi thêm.

## Performance note

- Candidate detail lookup là một active `contents` row theo ID; không cần pagination/count.
- Query không join snapshot history, course mentor hoặc user vì response không khai báo version/author và các join đó không xác định tác giả.
- Checked-in DDL không xác minh live schema, index, grants hoặc deployment.

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
