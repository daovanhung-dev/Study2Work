---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "49"
api_name: "Lấy cây nội dung course"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #49 |
| Tên | Lấy cây nội dung course |
| Endpoint | `GET /api/v1/mentor/courses/{course_id}/content` |
| Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Mentor có quyền quản lý course; cách kiểm tra cụ thể cần xác nhận |
| Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED` |
| Response | `ApiEnvelope<Content>` |
| Mutation | Không |
| Trạng thái hiện tại | `UNWIRED / NOT_FOUND` trong Study source |

API được gọi khi Mentor mở màn hình quản lý nội dung. AC-22 mô tả bước đọc `sections/lessons/content`, sau đó mới cho Mentor chọn thao tác CRUD/publish. API này chỉ đọc.

## Sources

| Nguồn | Loại | Bằng chứng dùng | Trạng thái |
|---|---|---|---|
| `docs/lists/list_api.md` | Contract | API #49: method/path/actor/input/response/status/errors; reusable Content fields | DIRECT |
| `AC_UNICA/00_AC_API_INDEX.md` | Workflow | AC-22 precondition và năm endpoint #49–#53 | DIRECT |
| `AC_03_MENTOR_TEACHING.drawio`, page AC22 | Activity diagram | GET → đọc sections/lessons/content → nhánh CRUD/publish | DIRECT |
| `DB_UNICA_TABLES.md`, `DB_UNICA_ERD.drawio` | Legacy schema design | 16 legacy tables; `courses.mentor_id`, `lessons`; không có generic Content/sections table | `DESIGN_ONLY` |
| `infra/postgres/02_study_db.sql` | V1-PILOT DDL | UUID `courses/course_versions/chapters/lessons/content_blocks` | PILOT ARTIFACT; không tương thích trực tiếp ID int64; live status chưa xác minh |
| DD #46–#48 | Related DD | Direct-owner query là candidate; AC-21 lecture workflow không phải AC-22 Content | DERIVED / OPEN |
| Current Study router/modules/tests | Runtime source | Không có Mentor route/module/test cho API #49 | CURRENT: UNWIRED / NOT_FOUND |

## Tables read

| Table/source | Mục đích | Trạng thái |
|---|---|---|
| Legacy `courses` | Candidate lookup course + direct owner `mentor_id` | `DERIVED`; schema/runtime chưa xác nhận, không bao phủ assigned course |
| Content tree source | Đọc sections/lessons/nodes theo course | `SOURCE_REQUIRED`; legacy ERD không có generic Content table, không tạo query giả |
| Pilot `chapters`, `lessons`, `content_blocks` | Có thể liên quan về khái niệm tới cây học liệu | DDL có UUID/versioned schema riêng; không map ngầm sang Content int64 |

## Tables write

N/A — API #49 là read-only; không INSERT/UPDATE/DELETE.

## Mục chú ý

- Giữ response catalog là `ApiEnvelope<Content>`. Không đổi thành `Page<Content>`, array hoặc nested tree.
- Tên “cây nội dung” và diagram đọc nhiều loại node, nhưng response `Content` chỉ khai báo một object cùng `parent_id?`; chưa có `children[]`, root convention, empty-tree rule hoặc pagination.
- Content schema có `id`, `course_id`, `content_type`, `title`, `payload`, `status`, `parent_id?`, `order`. Không có nguồn approved cho generic table, `payload` keys hoặc member values của `ContentType`/`ContentStatus`.
- AC-22 yêu cầu Mentor có quyền quản lý course. Legacy `courses.mentor_id` là direct-owner candidate giống #46/#47; Mentor ID binding và course assignment relation chưa có nguồn.
- Catalog chỉ khai báo lỗi 401/403/404/500. Không thêm error contract khác. Current middleware chưa có path API #49 trong `DESIGN_CONTRACT_PATHS`; nếu future route không được thêm vào allowlist, lỗi parse/unhandled có thể dùng fallback code chung.
- Live schema chưa được kiểm tra; pilot DDL là artifact, không phải bằng chứng schema runtime.

## Assumptions

- Candidate direct-owner predicate có thể được khảo sát trên legacy schema dưới dạng `courses.mentor_id = authenticated mentor ID`; đây là `DERIVED`, không phải quyết định đã duyệt.
- Q1 course existence/ownership và Q2 content-tree retrieval phải được xác nhận riêng; hiện không có cơ sở cho SQL Q2.
- Ví dụ response trong `04_Response.md` chỉ minh họa kiểu dữ liệu; placeholder enum/payload không phải giá trị mặc định hay runnable response.

## Conflicts

- API purpose/diagram biểu đạt một “cây” nhưng catalog trả `Content` đơn lẻ: `DISCREPANCY`.
- Legacy ERD không có `Content`, `sections` hay parent-content relation. Pilot content model dùng UUID và liên kết `course_version → chapter → lesson → content_block`: không đồng nhất với contract BIGINT/`parent_id`.
- Mentor identity/access assignment chưa được ánh xạ tới legacy `users.id/courses.mentor_id`.
- Null/empty/omit, enum, ordering, visibility, version, and empty result behavior chưa có nguồn.

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
