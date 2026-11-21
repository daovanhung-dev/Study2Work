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
| Authorization | Role Mentor và direct owner match `courses.mentor_id` trong current implementation |
| Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED` |
| Response | `ApiEnvelope<Content[]>` |
| Mutation | Không |
| Trạng thái source hiện tại | Route/module/query/test đã được wire trong Study source; live DB/deployment chưa xác minh |

API được gọi khi Mentor mở màn hình quản lý nội dung. AC-22 mô tả bước đọc cây trước khi chọn CRUD/publish. API #49 chỉ đọc.

## Sources

| Nguồn | Loại | Bằng chứng dùng | Trạng thái |
|---|---|---|---|
| `docs/lists/list_api.md` | Contract | API #49 method/path/actor/input/response/status/errors và reusable Content fields | DIRECT; response đã đồng bộ thành collection |
| `AC_UNICA/00_AC_API_INDEX.md` | Workflow | AC-22 precondition và năm endpoint #49–#53 | DIRECT |
| `AC_03_MENTOR_TEACHING.drawio`, page AC22 | Activity diagram | GET → đọc sections/lessons/content → CRUD/publish; output schema đồng bộ `Content[]` | DIRECT |
| `DB_UNICA_TABLES.md`, `DB_UNICA_ERD.drawio`, `infra/postgres/study-server/DB.sql` | Legacy schema artifacts | `courses.mentor_id` và `contents`; legacy Content table là source artifact sau thay đổi này | CHECKED-IN DDL; live status chưa xác minh |
| `infra/postgres/study-server/migrations/006_contents.sql` | Migration artifact | Tạo bảng `contents`, same-course parent FK và active-tree index | CHECKED-IN; chưa áp dụng live |
| `infra/postgres/02_study_db.sql` | V1-PILOT DDL | UUID `course_versions/chapters/lessons/content_blocks`, model khác runtime legacy | PILOT ARTIFACT; không được trộn vào API #49 |
| Current Study router/module/test | Runtime source | Route #49, Mentor access, query, projection và API tests | SOURCE_BACKED locally; live behavior chưa xác minh |

## Tables read

| Table/source | Mục đích | Trạng thái |
|---|---|---|
| Legacy `courses` | Xác nhận course tồn tại và direct owner `mentor_id` | Source/DDL-backed; principal là numeric authenticated user ID; course được phân công không được cấp quyền bởi endpoint này |
| Legacy `contents` | Đọc Content nodes theo `course_id`, chỉ lấy `deleted_at IS NULL` | Source/DDL/migration-backed locally; live migration chưa xác minh |
| Pilot `chapters`, `lessons`, `content_blocks` | Model học liệu pilot khác | Không map sang API BIGINT `Content` |

## Tables write

N/A — API #49 là read-only; không INSERT/UPDATE/DELETE.

## Mục chú ý

- Response là mảng phẳng `Content[]`; `parent_id` dùng để dựng cây client-side. Không có pagination metadata.
- Nodes được sắp xếp `parent_id NULLS FIRST, content_order ASC, id ASC`; `order` map từ `content_order`.
- API trả mọi `status` hiện lưu; không lọc theo draft/published. Soft-deleted rows bị lọc.
- Course tồn tại nhưng chưa có node trả HTTP 200 `data: []`; course thiếu, path sai format hoặc ngoài signed-int64 trả 404. Mentor khác owner nhận 403.
- `content_type` và `status` giữ open string; `payload` giữ JSON object. Enum members, payload subtype validation, version selection và assigned-course policy chưa được chốt.
- Status tài liệu vẫn Draft — Needs Confirmation. Local DDL/migration không chứng minh DB live đã có bảng `contents`.

## Quyết định triển khai và giới hạn

Catalog ban đầu dùng `ApiEnvelope<Content>` trong khi AC-22 gọi là cây. Để biểu diễn nhiều node mà không tự tạo nested `children[]`, API catalog và node GET trong AC-22 đã được đồng bộ sang `ApiEnvelope<Content[]>`; `parent_id` giữ liên kết phân cấp. Đây là quyết định triển khai cần business/API owner xác nhận.

Legacy BIGINT schema phù hợp ID/runtime của API #46–#48. V1-PILOT UUID/version schema không được dùng làm bảng thay thế. Direct owner access, empty-array semantics, parent ordering và soft-delete filtering là implementation choices, không phải bằng chứng về DB live hoặc policy assignment.

## Conflicts

- Catalog response ban đầu singular so với AC-22 tree purpose: implementation/catalog/diagram đã dùng `Content[]`; cần owner confirmation.
- Reusable Content fields không định nghĩa enum members, payload subtype keys hay version history.
- Active child có parent đã soft-delete không thể dựng thành cây nhất quán; current mapping trả 500 thay vì trả cây một phần. Chính sách dữ liệu này vẫn cần xác nhận.

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
