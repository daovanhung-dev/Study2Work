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
| Purpose | Đọc hàng đợi Content chờ Admin review. |
| Consumer/Actor | Admin |
| Authentication | Bearer JWT |
| Authorization | Role Admin theo catalog; Admin guard/policy chưa có trong Study source. |
| Direct request | Query `type?:string`, `course?:int64`, `page?:int32`; không có body. |
| Direct response | HTTP 200 `ApiEnvelope<Content>` theo catalog. |
| Direct errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 500 `DESIGN_INTERNAL_ERROR`. |
| AC-33 queue condition | Đọc Content có `status=PENDING_REVIEW`. |
| Runtime state | `UNWIRED / NOT_FOUND`; API #78 chưa có route/module/test. |
| Side effects | Read-only; không approve/reject, audit-write hoặc cập nhật Content. |

### Discrepancy: danh sách so với response

Tên API “Lấy pending content”, query `page` và AC-33 queue đều hàm ý một tập bản ghi. Catalog hiện trả `ApiEnvelope<Content>` đơn, không có collection hoặc pagination schema. Giữ contract này là DIRECT; `ApiEnvelope<Page<Content>>` chỉ là proposal `DERIVED` cần đồng bộ catalog trước implementation. API #68 có mismatch cùng dạng; API #73 khai báo `Page<Course>` trực tiếp.

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — #78–#81 và `Content`, `Page`, `PageMeta`.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-33 actors, precondition và endpoint sequence.
- [AC-33 moderation diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — queue filter, detail handoff, approve/reject branches và reload.
- [AC-22 content lifecycle diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — Mentor create/update/publish/delete and queue producer context.
- [Legacy DB table guide](../../diagrams/DB_UNICA_TABLES.md) và [legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — không có generic Content table tương thích.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID `content_blocks` và `content_review_decisions`; là schema artifact khác, live DB chưa xác minh.
- [Mentor Content #49](../49_mentor_content_list/02_Overview.md), [#50](../50_mentor_content_create/02_Overview.md), [#51](../51_mentor_content_update/02_Overview.md), [#52](../52_mentor_content_publish/02_Overview.md), [#53](../53_mentor_content_delete/02_Overview.md) — Content projection/lifecycle proposals, giữ trạng thái nguồn mở.
- [Admin user list #68](../68_admin_users_list/04_Response.md) và [Admin course list #73](../73_admin_courses_list/04_Response.md) — precedent cho cardinality mismatch và Page response đã được khai báo trực tiếp.
- [Current router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py) — route absence, Student-only guard và error integration hiện hành.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — envelope/error representation and query guidance.

## Tables read

| Relation/source | Mục đích | Basis/status |
|---|---|---|
| Logical Content pending set | Candidate rows cần review | AC-33 direct; physical relation `SOURCE_REQUIRED`. |
| Legacy `courses`, `lessons`, `resources` | Inventory kiểm tra khả năng mapping | Không có generic Content/queue relation; legacy artifact, không phải live proof. |
| V1-PILOT `content_blocks` | So sánh mô hình content | UUID, lesson-bound, không có `Content` BIGINT trực tiếp. |
| V1-PILOT `content_review_decisions` | So sánh decision history | Append-only UUID review log; không phải pending Content source. |

## Tables write

Không có. API #78 chỉ đọc; approval/rejection/audit thuộc #80/#81 theo AC-33.

## Mục chú ý

- AC-33 trực tiếp yêu cầu queue đọc `status=PENDING_REVIEW`; không tự đưa `APPROVED`, `PUBLISHED` hoặc `REJECTED` vào hàng đợi.
- #79 đọc `content/version/author`; #78 chỉ map reusable `Content`, không thêm author/version/review metadata.
- Query `type` và `course` là direct input; exact equality với `content_type`/`course_id` là proposal, physical mapping chưa có nguồn.
- Query `page` xung đột với response `Content` đơn. Không tạo query `size`, collection response hoặc PageMeta thành direct contract.
- #50 tạo Content ở `PENDING_REVIEW` và #51 revision mới cùng trạng thái chỉ là proposal trong DD trước; producer lifecycle cần xác nhận.
- AC-33 không nói queue filter revision nào, deleted/stale item behavior, thứ tự review hay empty-result shape.
- Pilot `content_review_decisions` ghi quyết định review append-only bằng UUID/resource-version ID; không map sang queue query hoặc catalog Content BIGINT.
- Current Study auth helper chỉ cho Student; không dùng lại làm Admin guard.

## Assumptions

- Nếu catalog được đổi sang Page, page 1-based/default 1, fixed size 20 và stable `id ASC` là phương án đơn giản `DERIVED`, dựa trên precedent #68/#73. Chưa áp dụng vào direct contract.
- Khi response là Page, không có pending row có thể trả HTTP 200 với `items=[]`; điều này cần được xác nhận cùng cardinality.
- Nếu `type` được dùng như filter, exact match với ContentType là proposal `DERIVED`; member/casing chưa xác nhận.

## Conflicts

- API purpose, query `page` và AC-33 list flow không khớp direct response `ApiEnvelope<Content>`.
- Reusable Content yêu cầu BIGINT fields; legacy DDL thiếu generic Content, còn V1-PILOT content/review relations dùng UUID/version model khác.
- `PENDING_REVIEW` là direct queue predicate nhưng POST #50 và revision #51 transition vào queue chỉ là `DERIVED` trong các DD liên quan.
- Current middleware allowlist không chứa endpoint; error helper trả `{}` khi `data` vắng mặt, trong khi API guideline yêu cầu `null`.

## Security note

- Xác thực Bearer và role Admin trước khi đọc Content để tránh tiết lộ queue cho principal trái quyền.
- Không trả JWT, raw review comments/decision history, author fields ngoài Content schema, hoặc nội dung DB lỗi.
- Không sửa trạng thái, ghi audit hoặc thực hiện review trong API read-only này.

## Performance note

- Candidate list cần giới hạn trang nếu contract xác nhận Page; không tải toàn bộ payload lớn theo mặc định.
- Query/filter/index/page plan chưa thể xác nhận khi Content relation và live schema chưa có nguồn.

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
