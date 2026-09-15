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
| API ID | `9` |
| Module | `GUEST / ACCOUNT & DISCOVERY` |
| Method | `GET` |
| Endpoint | `/api/v1/courses/{course_id}/curriculum` |
| Purpose | `Lấy danh sách chương/bài học public theo thứ tự trong một course` |
| Consumer/Actor | `Guest / course detail UI` |
| Authentication | `Public; không yêu cầu Bearer token` |
| Authorization | `N/A — public course access` |
| Basis | `DIRECT — approved API contract + AC-05 + DB_UNICA_ERD` |
| Status | `Draft — Needs Confirmation` |
| Transaction | `N/A — read-only API` |
| Side effects | `N/A — không có mutation hoặc external side effect` |

## Sources

- [`docs/lists/list_api.md`](../../../docs/lists/list_api.md) — API #9 endpoint, input, `ApiEnvelope<Page<Lesson>>` và status/error contract.
- [`AC_01_GUEST_ACCOUNT.drawio`](../../../docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio) — AC-05 precondition course hợp lệ/public và bước đọc curriculum theo thứ tự.
- [`DB_UNICA_ERD.drawio`](../../../docs/diagrams/DB_UNICA_ERD.drawio) — quan hệ `courses.id → lessons.course_id` và các cột `courses`/`lessons` được dùng trong mapping.
- [`createDD-markdown template`](../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/) — cấu trúc 8 file DD.

## Tables read

- `courses` — kiểm tra `id` và chỉ cho phép course có `status = 'PUBLISHED'`.
- `lessons` — đọc curriculum thuộc course, chỉ lấy `status = 'PUBLISHED'` và sắp xếp theo `sort_order`.

## Tables write

- `N/A — read-only API; không có DB mutation.`

## Mục chú ý

- API được gọi trong AC-05 sau khi UI mở Course Detail và course đã được xác nhận là public.
- Endpoint không nhận pagination query; toàn bộ lesson public được trả trong một `Page<Lesson>` duy nhất.
- Curriculum không có lesson public vẫn là kết quả thành công `200` với `data.items = []`.

## Assumptions

- `lessons.status = 'PUBLISHED'` là quy tắc visibility design-only để không lộ lesson draft/private cho Guest.
- `lessons.name` map sang contract field `Lesson.title` và `lessons.sort_order` map sang `Lesson.order`.
- Pagination một page dùng `page = 1`, `size = total`, `total = total`; `total_pages = 1` khi `total > 0`, và `0` khi curriculum rỗng.
- Khi nhiều lesson có cùng `sort_order`, dùng `id ASC` làm tie-breaker xác định.

## Conflicts

- `DISCREPANCY/TBD: Study server không có schema/migration runtime trong working tree; `DB_UNICA_ERD.drawio` chỉ là design source.`
- `DISCREPANCY/TBD: Contract không nêu rõ lesson visibility filter hoặc pagination metadata; các quy tắc trên là assumption của DD và cần confirmation.`
- `RUNTIME_STATUS: chưa runtime/OpenAPI verified; tài liệu là design-only.`

## Security note

- Chỉ trả curriculum của course `PUBLISHED` và lesson `PUBLISHED`.
- Không trả draft/private lesson, raw SQL, stack trace hoặc storage detail.

## Performance note

- Course gate dùng `courses.id` và `courses.status`.
- Curriculum lookup dùng `lessons.course_id`, `lessons.status`, `lessons.sort_order`.
- Index/cache policy chưa được source xác nhận.

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Overview`
- Dimension: `A1:BA10`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `4`
- Số vùng merge: `0`
