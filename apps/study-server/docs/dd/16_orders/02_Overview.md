---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 16 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | POST |
| Endpoint | /api/v1/orders |
| Purpose | Tạo logical Order cho nhánh paid course trong AC-12 |
| Consumer/Actor | Student |
| Authentication | Bearer JWT |
| Authorization | Role=Student |
| Basis | DIRECT — approved design contract; flow context từ AC-12 |
| Status | Draft — Needs Confirmation |
| Completion | PARTIALLY COMPLETED |
| Decision status | NEEDS USER DECISION |
| Transaction | SOURCE_REQUIRED — AC-12 không xác định transaction boundary hoặc rollback |
| Side effects | AC-12 yêu cầu tạo Order ở trạng thái PENDING; physical persistence chưa có nguồn xác nhận |

## Sources

- [list_api.md](../../../../../docs/lists/list_api.md) — method, endpoint, auth, request, response và HTTP/business codes API #16.
- [AC_02_STUDENT_LEARNING.drawio](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — AC-12; API #16 nằm sau nhánh paid course và trước API #17.
- [DB_UNICA_TABLES.md](../../diagrams/DB_UNICA_TABLES.md) — ERD V1 không có bảng `orders`; API #17 payment là thiết kế riêng.
- [DB_UNICA_ERD.drawio](../../diagrams/DB_UNICA_ERD.drawio) — V1 simplification không tách `orders`.
- [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — checked-in SQL hiện có bảng `payments`, không có bảng `orders`.
- [v1.py](../../../app/api/v1.py) — composition root hiện hành; không có route API #16.
- [responses.py](../../../app/core/responses.py) — current envelope factory; chỉ là current convention, không chứng minh API #16 đã dùng.
- [declared-routes.md](../../../../../.agents/server-study/apis/declared-routes.md) — API #16 chưa wired trong current route surface.

## Tables read

- `SOURCE_REQUIRED` — API #16 không có query/table read được xác định trong contract.
- AC-12 đặt API #8 course detail và API #15 enrollment-status trước bước gọi API #16; diagram không xác nhận API #16 tự lặp lại các truy vấn đó.

## Tables write

- Logical `Order` — AC-12 ghi tạo Order = PENDING.
- Physical table, columns, constraints và persistence mapping: `SOURCE_REQUIRED`.
- Không dùng `payments` làm bảng Order; API #17 là bước payment riêng.

## Mục chú ý

- API catalog là `APPROVED_DESIGN_CONTRACT`, chưa runtime-verified.
- API #16 chỉ được đặt trong nhánh paid course của AC-12; không suy ra xử lý direct call cho free course, course không hợp lệ hoặc đã enrolled.
- `Order` contract gồm `id`, `course_id`, `user_id`, `amount`, `currency`, `status`, `created_at`; không có persistence schema tương ứng được xác nhận.
- Request có `payment_provider`, nhưng schema `Order` không có field này và API #17 cũng nhận provider riêng.
- Không tự thêm HTTP 404/409 hoặc business code ngoài catalog API #16.

## Assumptions

- API #16 được dùng trong paid-course branch như AC-12 mô tả.
- Giá trị `PENDING` là trạng thái ban đầu của Order theo AC-12; không suy ra các trạng thái Order khác.
- `user_id`, amount, currency và created_at chưa có mapping physical source được xác nhận.

## Conflicts

- `SOURCE_REQUIRED`: Contract có logical `Order`; DB_UNICA ERD V1 nêu không tách `orders`, DB_UNICA_TABLES ghi bảng `orders` không tồn tại trong ERD, và checked-in DB.sql không khai báo bảng này.
- `SOURCE_REQUIRED`: Không có enum catalog cho `PaymentProvider` hoặc `OrderStatus`.
- `UNWIRED / NOT_FOUND`: Current Study route/module/query/test không có API #16.

## Security note

- Giữ yêu cầu Student Bearer JWT theo contract.
- Không tự chốt claim lấy `user_id` hoặc thêm rule ownership ngoài nguồn.
- Không đưa dữ liệu thanh toán nhạy cảm vào response ngoài schema Order đã khai báo.

## Performance note

- Contract không quy định query plan, index, cache hoặc idempotency.
- Không đề xuất index hoặc lưu trữ thay thế khi physical Order model chưa được xác nhận.

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/02_Overview.md.
- Sheet logic: Overview.

