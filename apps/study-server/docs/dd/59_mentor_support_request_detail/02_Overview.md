---
title: "Overview"
order: 2
dd_id: "59"
api_name: "Lấy nội dung request/thread"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 59 |
| Module | MENTOR / TEACHING & SUPPORT |
| Method | GET |
| Endpoint | /api/v1/mentor/support/{request_id} |
| Purpose | Đọc một support request và toàn bộ conversation trong phạm vi Mentor. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Shared role `MENTOR`; request thuộc course có `courses.mentor_id` bằng JWT `sub`. Fallback DERIVED từ API #58 và Mentor APIs hiện có. |
| Basis | Method/path/response/error set là DIRECT từ catalog/AC-24; BIGINT schema, access predicate, message order/visibility và asset resolver là DERIVED từ API #58 local implementation. |
| Status | Draft — Needs Confirmation |
| Transaction | READ-ONLY; không commit. |
| Side effects | Không có mutation. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md).
- [AC/API index, AC-24](../../diagrams/AC_UNICA/00_AC_API_INDEX.md).
- [AC-24 diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio).
- [Legacy DB.sql](../../../../../infra/postgres/study-server/DB.sql).
- [Support fallback migration 008](../../../../../infra/postgres/study-server/migrations/008_support_requests.sql).
- [API #58 DD](../58_mentor_support_requests/02_Overview.md).
- [API #58 module](../../../../../apps/study-server/app/modules/mentor/api_58_mentor_support_requests/).
- [API #48 direct-owner detail pattern](../../../../../apps/study-server/app/modules/mentor/api_48_mentor_lecture_detail/).
- [API #55 signed-int64 detail pattern](../../../../../apps/study-server/app/modules/mentor/api_55_mentor_submissions_detail/).
- [API Guidelines](../../../../../contracts/api-guidelines/README.md).

## Tables read

- `support_requests`, `support_messages`, `support_message_uploads`, `courses`, `users`, and `uploads`.
- These are the legacy BIGINT fallback selected by API #58; checked-in DDL/migration are not proof of live schema availability.
- V1-PILOT UUID `support_tickets`/`support_messages` is not queried by this local implementation.

## Tables write

- N/A — READ-ONLY API. API #60 owns message insert; API #61 owns request status update.

## Mục chú ý

- Catalog giữ response object đơn `ApiEnvelope<SupportRequest>`; không đổi contract của API #58 collection.
- `request_id` là int64. Route nhận raw path text để giữ lỗi malformed/overflow trong catalog 404 thay vì thêm 422.
- Request lookup trả 404 nếu ID không tồn tại; request có course owner khác trả 403. Đây là fallback theo API #48/#55 và lộ resource existence theo catalog semantics.
- Dùng toàn bộ messages theo thứ tự `created_at ASC, id ASC`; không có page/limit. Thread rỗng trả `messages: []`.
- Fallback schema `support_messages` không có cờ `is_internal`; mọi message được lưu theo schema này đều được trả. Đây là giới hạn DERIVED, không phải xác nhận policy nội bộ cho hệ thống khác.
- Attachments dùng `support_message_uploads` theo `asset_position`, rồi đọc `uploads` nếu khớp cùng author, course, role-purpose và `UPLOADED`.
- Optional `avatar_url` và `resolved_at` bị omit khi NULL, theo model/API #58 hiện tại.

## Assumptions

- Request access được giới hạn bằng direct `courses.mentor_id`, không dùng pilot assignment UUID hoặc enrollment; `DERIVED`.
- ID path malformed, âm, zero hoặc ngoài signed-int64 lookup không có row phù hợp và trả 404 theo API #48 pattern; không thêm 422.
- Mọi message trong selected legacy table đều hiển thị; schema fallback không có internal flag.
- Projection/link không hợp lệ được coi là lỗi nội bộ 500, không trả thread/asset một phần.

## Conflicts

- API #59 DD cũ đánh dấu support schema và mapping là `SOURCE_REQUIRED`. API #58 sau đó thêm local BIGINT support schema; #59 kế thừa schema đó cho local source, nhưng live DB vẫn `NOT_VERIFIED_HERE`.
- V1-PILOT UUID model có `is_internal` và khác keys; không được dùng lẫn với BIGINT fallback.
- API #59 catalog giữ 401/403/404/500; malformed path theo fallback 404, không thêm business code mới.

## Security note

- Shared guard xác thực Bearer/JWT/role `MENTOR` trước path và DB lookup.
- Dùng ID request chỉ để lookup; mọi request/message query tiếp tục ràng buộc trực tiếp `courses.mentor_id = :mentor_id`.
- Asset URL chỉ trả khi link và upload metadata thỏa owner/course/purpose/status; không trả row ngoài scope hoặc storage key.
- Thứ tự 404-missing rồi 403-other-owner theo API #48/#55; resource enumeration policy chưa có xác nhận riêng.

## Performance note

- Không có pagination/message limit trong contract; toàn bộ thread được tải như API #58.
- Q2 tải thread và asset metadata theo một bulk query để tránh query theo từng message.
- Query plan và payload bounds trên live PostgreSQL chưa kiểm chứng.

## Trạng thái liên quan

- [Plan, source matrix và quyết định DERIVED](./PLAN_RESULT.md).
- [Open Questions](./OPEN_QUESTIONS.md).
- [Verification report](./VERIFICATION_REPORT.md).
- #59 hiện reuse schema/projection của #58; #60/#61 giữ quyền sở hữu mutation và chưa được triển khai trong phiên này.

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
