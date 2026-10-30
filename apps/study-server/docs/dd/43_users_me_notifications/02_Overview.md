---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "43"
api_name: "Lấy notification list"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 43 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | `GET` |
| Endpoint | `/api/v1/users/me/notifications` |
| Purpose | Lấy trang thông báo thuộc `Student` hiện đăng nhập để hiển thị trung tâm thông báo/unread badge. |
| Consumer/Actor | `Student` |
| Authentication | Bearer `JWT` |
| `Authorization` | Yêu cầu role `Student`; principal lấy từ `JWT`, không nhận `user_id` từ request. |
| Basis | Approved design contract + AC-20; pagination/order là DERIVED. |
| Status | Draft — Needs Confirmation |
| Current runtime state | UNWIRED / NOT_FOUND — không có route/module/query/test cho API #43 trong Study source hiện tại. |
| Transaction | N/A — `GET` read-only. |
| Side effects | N/A — không có mutation. |

## Sources

- [API catalog](../../../../../docs/lists/list_api.md) — API #43–#45, Page/Notification schemas và `status`/error contract.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, precondition, postcondition và ba API của AC-20.
- [AC-20 activity diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — recipient read, unread badge/list và các nhánh #44/#45.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) — mục notifications và query design-only.
- [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — quan hệ users-to-notifications và physical fields.
- [Checked-in Study DDL](../../../../../infra/postgres/study-server/DB.sql) — định nghĩa notifications; không chứng minh live schema.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — envelope, error body và trace convention.
- Current [Study router](../../../app/api/v1.py), [Student auth helper](../../../app/utils/auth.py) và [response helper](../../../app/core/responses.py) — current source boundary; API #43 chưa gọi các helper này.
- [API #10 pagination precedent](../10_courses_reviews/05_Data_Mapping.md) — fixed size 20, default page 1 và stable sort dưới nhãn design-only.
- [API #38 response precedent](../38_users_me_achievements/04_Response.md) — giữ Page<T> khi pagination input chưa đầy đủ.
- [API #42 read-only table precedent](../42_discussions_detail/07_table.md) — tách candidate read projection khỏi mutation mapping.
- [Canonical DD Markdown template](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/) — tám sheet; fingerprint tại [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).
## Tables read

- notifications — candidate physical source theo DB guide/ERD/DDL.
- `NotificationRecipient` — logical source được AC-20 gọi tên nhưng chưa có physical table trong DB guide/ERD/DDL.

## Tables write

- N/A — API #43 là `GET`/read-only; không có insert, update hoặc delete.

## Expected behavior

- `Student` đăng nhập mở trung tâm thông báo.
- API trả notification list cho `Student` hiện tại và có thể lọc unread.
- Sau khi API #44 hoặc #45 đổi read state, lần tải lại của API #43 phản ánh trạng thái đã lưu.
- Contract giữ `ApiEnvelope<Page<Notification>>` và đúng `status`/error set tại catalog.

## Current behavior

- API #43 chưa có route, module, query hoặc test trong Study Server.
- Diagram yêu cầu đọc `NotificationRecipient` theo user; DB artifacts chỉ có bảng notifications với `user_id` nullable và `is_read`.
- DDL không có các cột `channels`, `status`, `read_at`, `scheduled_at`; live schema chưa xác minh.
- Current shared auth helper hỗ trợ `Student` Bearer/`JWT`, nhưng API #43 chưa được wire tới helper.
- Current error_response() mặc định serialize data thành {}; API guideline mô tả data: null. API #43 chưa dùng helper này.

## Mục chú ý

- API catalog định nghĩa HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; các lỗi được phép là 401, 403 và 500 với business code đúng theo catalog.
- Query dùng notifications.user_id = `principal_id` là đề xuất DERIVED; không đọc các hàng `user_id` NULL khi chưa có mô hình recipient/read state.
- `unread_only`=true đề xuất lọc notifications.is_read = FALSE; false hoặc omitted không thêm predicate này.
- Page size 20, page mặc định 1 và order mới nhất trước (`created_at` DESC, id DESC) là đề xuất DERIVED theo precedent API #10.
- Không thêm query size, sort field, response field hoặc error code ngoài catalog.
- Field `type` không được đồng nhất với `channels`; `is_read` không được đồng nhất với `status` hoặc `read_at`.

## Assumptions

- page omitted dùng page 1.
- Page size cố định là 20 vì request không nhận size.
- `total_pages` = ceil(`total` / 20); khi `total`=0, `total_pages`=0.
- Page vượt phạm vi trả trang rỗng cùng metadata; đây là hành vi DERIVED.
- List sắp xếp `created_at` DESC, id DESC; đây là hành vi DERIVED.
- Chỉ notifications.user_id khớp principal được đưa vào candidate result; hàng NULL/broadcast không được bao gồm cho tới khi có mô hình recipient.
- Các assumption cần xác nhận ở OPEN_QUESTIONS.md.

## Conflicts

- AC-20 dùng logical `NotificationRecipient`, còn DB guide/ERD/DDL chỉ định notifications.user_id.
- Catalog yêu cầu Notification.channels[] và Notification.status, nhưng DDL chỉ có `type` và `is_read`.
- Catalog có optional `read_at` và `scheduled_at`; DDL không có các cột này.
- Diagram #44 nói update `read_at`; diagram #45 nói bulk update unread; DDL chỉ có boolean `is_read`.
- Page response có size nhưng API #43 chỉ nhận page.
- API guideline quy định error data:null, còn current error_response() fallback tạo {}.

## Security note

- Mọi query phải scope bằng user ID đã xác thực từ `Student` `JWT`.
- Không tin user ID do client gửi; contract không có trường đó.
- Không bao gồm notification broadcast (`user_id` IS NULL) khi chưa có rule xác định quyền xem và read state theo recipient.
- Lỗi không được trả SQL, token, stack trace hoặc dữ liệu provider nội bộ.

## Performance note

- Đề xuất giới hạn page nội bộ ở 20 row; không thêm size request field.
- Count query phải áp dụng đúng predicate principal/unread như page query.
- Index phù hợp chưa được nguồn xác nhận; không đề xuất schema/index mới trong DD này.
- Live database/query performance chưa được kiểm tra.
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
