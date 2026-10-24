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
| Authorization | Role Admin theo catalog; Admin guard/policy chưa có trong Study source. |
| Direct request | Path `content_id:int64!`; không body/query. |
| Direct response | HTTP 200 `ApiEnvelope<Content>` theo catalog. |
| Direct errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR`. |
| AC-33 sequence | #78 queue → #79 detail → #80 approve hoặc #81 reject → reload #78. |
| Runtime state | `UNWIRED / NOT_FOUND`; route/module/test chưa có. |
| Side effects | Read-only; không quyết định duyệt, ghi decision/audit hoặc đổi Content status. |

### Discrepancy: metadata review so với response schema

AC-33 node n6 yêu cầu backend đọc `content/version/author`. Catalog #79 trả `Content`; reusable schema có tám field Content nhưng không định nghĩa version hoặc author. DD giữ response trực tiếp đúng catalog. Không thêm metadata vào `data` hoặc giả định rằng các metadata nằm trong `payload`. Cần xác nhận metadata chỉ là dữ liệu nội bộ hay catalog cần một projection response khác.

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — row #79, Content fields và exact errors.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-33 actor, precondition và endpoint sequence.
- [AC-33 moderation diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — n5 gọi #79; n6 đọc content/version/author; n7 rẽ sang #80/#81.
- [DD #78 — pending queue](../78_admin_content_pending/02_Overview.md), [mapping](../78_admin_content_pending/05_Data_Mapping.md), [open questions](../78_admin_content_pending/OPEN_QUESTIONS.md) — queue predicate và revision identity chưa chốt.
- [DD #69 — Admin user detail](../69_admin_user_detail/04_Response.md) — giữ singleton response ApiEnvelope<UserProfile> theo catalog; không dùng schema user làm Content precedent.
- [DD #74 — Admin course detail](../74_admin_course_detail/04_Response.md) — Page singleton là proposal của API #74 vì catalog khai báo Page, không áp dụng cho #79.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) và [legacy DB table guide](../../diagrams/DB_UNICA_TABLES.md) — không có generic Content/version/author relation.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID content blocks/version/decision artifacts; không map trực tiếp sang Content BIGINT.
- [Current router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py) — endpoint absent, shared guard Student-only, allowlist/error envelope discrepancy.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — envelope và error data convention.

## Tables read

| Logical/physical source | Mục đích | Basis/status |
|---|---|---|
| Logical Content | Candidate item theo path content_id | GET detail; physical relation SOURCE_REQUIRED. |
| Logical Content version | Diagram yêu cầu đọc revision/version | Direct read intent; selector/table/key SOURCE_REQUIRED. |
| Logical Content author | Diagram yêu cầu đọc tác giả | Direct read intent; author identity/relation SOURCE_REQUIRED. |
| Legacy courses, lessons, resources | Kiểm tra khả năng mapping | Không có generic Content hay version/author relation tương thích. |
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

- Candidate Q1 tìm logical Content theo ID bằng path param và trả status hiện tại trong Content; không áp dụng thêm status filter cho #79. Đây là DERIVED, cần chốt cùng stale queue behavior.
- Không có count, pagination, Page, write, audit hoặc extra business code.
- Error data:null theo guideline là expected; helper hiện tại mặc định {} khi không truyền data.

## Conflicts

- “Metadata review”/AC-33 n6 yêu cầu content/version/author, trong khi direct response là ApiEnvelope<Content> không có version/author.
- Legacy DB thiếu generic Content; V1-PILOT dùng UUID versioned course/lesson/content block model, khác Content BIGINT.
- Stable identity của queue row, detail và approve/reject giữa các revision chưa được xác định.
- Admin guard chưa có; middleware allowlist chưa có path #79; error helper data mặc định {}.

## Security note

- Xác thực Bearer và role Admin trước mọi Content/version/author read.
- Không trả raw review comments, reviewer identity, author PII hoặc database errors ngoài contract.
- Version/author projection phải có field allowlist và authorization policy trước khi đưa vào response.

## Performance note

- Candidate detail lookup là một resource theo ID; không cần pagination/count.
- Không thể chốt index/join plan khi Content/version relations và live schema chưa được xác nhận.

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
