---
title: "Overview"
order: 2
dd_id: "22"
api_name: "Kiểm tra quyền truy cập lesson"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 22 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | GET |
| Endpoint | /api/v1/lessons/{lesson_id}/access |
| Purpose | Kiểm tra quyền truy cập lesson trước khi tiếp tục luồng học AC-14. |
| Consumer/Actor | Student |
| Authentication | Bearer JWT |
| Authorization | role=Student; AC-14 yêu cầu kiểm tra enrollment/prerequisite, điều kiện cụ thể chưa chốt. |
| Basis | DIRECT — API catalog và AC-14 |
| Status | Draft — Needs Confirmation |
| Transaction | N/A — GET; không có transaction hoặc mutation được contract mô tả. |
| Side effects | N/A — không có side effect được mô tả cho API #22. |

## Sources

- [API #22 catalog row](../../../../../docs/lists/list_api.md) — method, path, actor, request, response và status/business codes.
- [AC-14 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, precondition, postcondition và API sequence.
- [AC-14 diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — abstract enrollment/prerequisite check; denial branch ghi 403 + reason.
- [DB design](../../diagrams/DB_UNICA_TABLES.md) — lessons và enrollments là bảng thiết kế; table-specific runtime method chưa có.
- [Checked-in DDL](../../../../../infra/postgres/study-server/DB.sql) — cấu trúc thiết kế hiện tại; live schema chưa xác minh.
- [Current router](../../../app/api/v1.py) — không có route API #22.
- [Current auth helper](../../../app/utils/auth.py) — helper Student/JWT dùng cho các route hiện có; chưa được API #22 gọi.

## Tables read

- `lessons` — candidate nguồn Lesson theo DB design; query API #22 chưa được xác nhận.
- `enrollments` — candidate nguồn điều kiện enrollment theo AC-14 và DB design; status predicate chưa được xác nhận.

## Tables write

- N/A — không có write operation được API #22 hoặc AC-14 mô tả.

## Mục chú ý

- AC-14 mô tả API #22 trước API #23 `POST /api/v1/lessons/{lesson_id}/start`; không gộp side effect của API #23 vào API #22.
- API catalog và diagram đều khai báo success payload `ApiEnvelope<Lesson>`.
- Diagram ghi nhánh từ chối `403 + lý do`; catalog chỉ xác định `DESIGN_ACCESS_DENIED`, chưa định nghĩa nơi hoặc cấu trúc wire của lý do.
- AC-15 có bước kiểm tra access và trạng thái publish cho endpoint nội dung riêng; không chuyển predicate đó sang API #22 khi chưa có nguồn xác nhận.

## Assumptions

- Không có business assumption được chốt trong DD này; điểm cần quyết định được ghi trong [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

## Expected behavior

- Student gửi Bearer JWT và `lesson_id` dạng int64 bắt buộc.
- AC-14 yêu cầu kiểm tra enrollment/prerequisite; nếu bị từ chối, sơ đồ chỉ định HTTP 403 và “lý do”.
- Khi được phép, contract khai báo HTTP 200 `DESIGN_RESOURCE_RETRIEVED` với `ApiEnvelope<Lesson>`.
- Contract khai báo 401, 403, 404 và 500; ý nghĩa chi tiết 404 chưa được nêu.

## Current behavior

- `app/api/v1.py` không khai báo `/lessons/{lesson_id}/access`; module và focused test API #22 không có trong inventory hiện tại.
- `app/utils/auth.py` hiện có helper đọc Bearer/JWT, chuẩn hóa `sub` thành user ID số và kiểm tra role STUDENT; API #22 chưa gọi helper này.
- `lessons` và `enrollments` có trong DDL checked-in; live database metadata chưa xác minh.
- Trạng thái endpoint: `UNWIRED / NOT_FOUND`; contract/diagram chưa phải bằng chứng runtime.

## Conflicts

- `DISCREPANCY`: AC-14 diagram yêu cầu 403 “kèm lý do”, trong khi catalog chỉ liệt kê business code `DESIGN_ACCESS_DENIED`; payload/message của lý do chưa được định nghĩa.
- Không có route, module, query hoặc test runtime API #22 để đối chiếu expected behavior.

## Security note

- Contract giới hạn actor ở Student Bearer JWT; kiểm tra role hiện có trong shared helper không tự xác định entitlement enrollment/prerequisite của API #22.
- Không dùng ID do client gửi ngoài `lesson_id` để thay thế identity từ token; cách bind token subject với enrollment cần được xác nhận trước khi chốt query.

## Performance note

- Contract không quy định latency, index hoặc query plan. Query access và Lesson retrieval chưa được đặc tả nên chưa đưa ra cam kết hiệu năng.

---
## Phụ lục đối chiếu template Markdown

- Template: [02_Overview.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/02_Overview.md).
- Sheet nguồn: Overview.
