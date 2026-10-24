---
title: "Overview"
order: 2
dd_id: "60"
api_name: "Gửi phản hồi"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 60 |
| Module | MENTOR / TEACHING & SUPPORT |
| Method | POST |
| Endpoint | /api/v1/mentor/support/{request_id}/reply |
| Purpose | Lưu một phản hồi của Mentor vào conversation của support request. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Role Mentor; AC-24 yêu cầu request thuộc phạm vi phụ trách. Principal và predicate vật lý chưa được xác nhận. |
| Basis | Catalog + AC-24 là DIRECT; request ref encoding và physical insert còn DERIVED/SOURCE_REQUIRED. |
| Status | Draft — Needs Confirmation |
| Transaction | Candidate insert + reload trong một caller-owned transaction; chưa được runtime xác nhận. |
| Side effects | Logical `INSERT SupportMessage`; không upload file hoặc đổi status request tại API #60. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md).
- [AC/API index, AC-24](../../diagrams/AC_UNICA/00_AC_API_INDEX.md).
- [AC-24 flow diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio).
- [AC-17 upload/submission flow](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio).
- [API #34 UploadAsset DD](../34_uploads/02_Overview.md).
- [API #35 file refs DD](../35_assignments_submissions/OPEN_QUESTIONS.md).
- [API #47 asset refs DD](../47_mentor_lectures_create/OPEN_QUESTIONS.md).
- [API #58 support list DD](../58_mentor_support_requests/02_Overview.md).
- [API #59 thread detail DD](../59_mentor_support_request_detail/02_Overview.md).
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql).
- [Current Study router](../../../../../apps/study-server/app/api/v1.py).
- [Current DB helper](../../../../../apps/study-server/app/core/database.py).
- [Current error middleware](../../../../../apps/study-server/app/core/middleware.py).
- [API Guidelines](../../../../../contracts/api-guidelines/README.md).
- [Study API DD workflow](../../../../../.agents/server-study/workflows/README.md).

## Tables read

- Legacy Study DB.sql/ERD không có support message model.
- `support_messages` trong V1-PILOT là candidate, không xác nhận API #60 runtime mapping; các khóa dùng UUID khác contract int64.
- `file_objects` là candidate metadata schema cho file refs; #34 DD chưa xác định persistence hoặc UploadAsset ID binding.

## Tables write

- Logical effect từ AC-24: `INSERT SupportMessage`.
- Candidate physical table: V1-PILOT `support_messages`; chưa được chủ schema chọn làm model runtime.
- Không `UPDATE support_tickets` tại #60; AC-24 dành resolve/status update cho #61.

## Mục chú ý

- API #60 chỉ tạo reply, sau đó AC-24 hỏi vấn đề đã xử lý chưa: YES gọi #61; NO giữ OPEN.
- Success trả `SupportRequest`, nên proposal là reload thread sau insert để `messages[]` có reply mới.
- `attachment refs:string!` giữ nguyên contract label. Proposal đơn giản là wire key `attachment_refs` với danh sách `UploadAsset.id` int64 phân tách bằng dấu phẩy; `""` nghĩa là không có attachment. Đây là DERIVED và cần thống nhất với #35/#47.
- #34 chưa có asset ID registry/ownership resolver. V1-PILOT `file_objects.id` là UUID, không map trực tiếp sang int64 UploadAsset ID.
- Source Study hiện không có route/module/test API #60; Mentor auth cũng chưa có implementation.

## Assumptions

- `message` chỉ bị từ chối nếu rỗng hoặc toàn whitespace (422 proposal); không thêm min/max length và không trim nội dung lưu.
- `author_type=STAFF` và `is_internal=false` là candidate cho Mentor gửi phản hồi cho learner, không phải rule đã phê duyệt.
- Request status không đổi ở #60; post-resolution reply behavior chưa chốt.
- Candidate insert và response reload cùng transaction; lỗi trước commit rollback insert theo caller-owned transaction convention.

## Conflicts

- Contract request/API response dùng int64 IDs nhưng pilot ticket/message/file IDs là UUID.
- #34 không xác nhận UploadAsset.id, metadata persistence hoặc asset ownership lookup; #35/#47 vẫn để reference string format mở.
- Pilot support_messages có `is_internal`; AC-24 không phân biệt public reply với internal note. Candidate `false` cần xác nhận.
- API Guidelines yêu cầu error `data:null`; current helper mặc định `{}` khi data vắng mặt. #60 chưa wired.

## Security note

- Không cho phép Mentor ghi vào request ngoài scope AC-24.
- Không tin request path hoặc attachment refs như bằng chứng quyền. Mỗi file ref cần resolve và kiểm tra ownership/purpose/eligibility trước insert.
- Không trả Storage key hay URL được dựng từ ref. Không lộ nội dung request/message ngoài phạm vi.

## Performance note

- Không có batch size hoặc giới hạn số attachment/message trong catalog.
- Candidate response rehydrates `SupportRequest` và `messages[]`; cần chốt thread bounds khi có schema/contract rõ.
- Không gọi Object Storage upload trong API #60; client phải gọi #34 trước.

## Trạng thái liên quan

- [Plan và ma trận nguồn](./PLAN_RESULT.md).
- [Open Questions](./OPEN_QUESTIONS.md).
- [Verification report](./VERIFICATION_REPORT.md).
- AC-24 macro-review #58–#61 chờ API #61; ref encoding còn cần đối chiếu với #35/#47.

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
