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
| API ID | `11` |
| Module | `GUEST / ACCOUNT & DISCOVERY` |
| Method | `GET` |
| Endpoint | `/api/v1/courses/{course_id}/resources` |
| Purpose | `Lấy tài nguyên thuộc một khóa học công khai để hiển thị hoặc chuyển sang bước mở/tải tài nguyên.` |
| Consumer/Actor | `Guest / course detail UI` |
| Authentication | `Public; không yêu cầu Bearer token` |
| Authorization | `N/A — public endpoint; course phải ở trạng thái PUBLISHED` |
| Basis | `DIRECT — approved API contract + AC-06 + DB_UNICA_ERD` |
| Status | `Draft — Needs Confirmation` |
| Transaction | `N/A — read-only API` |
| Side effects | `N/A — không có mutation hoặc external side effect` |

## Sources

- [`docs/lists/list_api.md`](../../../docs/lists/list_api.md) — API #11, path `course_id`, `ApiEnvelope<Resource>` và status/error contract.
- [`AC_01_GUEST_ACCOUNT.drawio`](../../../docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio) — AC-06, actor Guest và flow đọc resource theo course.
- [`DB_UNICA_ERD.drawio`](../../../docs/diagrams/DB_UNICA_ERD.drawio) — bảng `courses`, `lessons`, `resources` và quan hệ `lesson_id`.
- [`createDD-markdown template`](../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/) — cấu trúc 8 file DD.

## Tables read

- `courses` — kiểm tra `course_id` tồn tại và có `status = 'PUBLISHED'`.
- `lessons` — nối resource về course qua `lessons.course_id`.
- `resources` — đọc metadata resource.

## Tables write

- `N/A — read-only API; không có DB mutation.`

## Mục chú ý

- `API #11 không tạo signed URL; client chuyển resource đã chọn sang API #12 khi cần metadata/signed URL.`
- `Contract dùng ApiEnvelope<Resource> dù tên API là “Lấy danh sách tài nguyên”.`
- `Không có query hoặc pagination trong contract.`

## Assumptions

- `Course phải được xác nhận PUBLISHED trước khi đọc resource để không expose resource của course draft/private.`
- `resources.lesson_id` là khóa nối trực tiếp tới `lessons.id`; `lessons.course_id` dùng để scope theo path.`
- `resource_type` map sang field contract `type` theo alias logic.`
- `Kết quả nhiều resource được giữ ở mức query row trong Data Mapping; không tự chọn row đầu tiên hoặc đổi response thành Page/array.`

## Conflicts

- `DISCREPANCY/TBD: endpoint mang nghĩa danh sách và ERD cho phép quan hệ 1:N, nhưng list_api.md khai báo data là Resource đơn; chưa có quy tắc cardinality/selection.`
- `DISCREPANCY/TBD: Resource.visibility là field bắt buộc trong contract nhưng ERD resources không có cột visibility; không tự tạo cột hoặc predicate.`
- `DISCREPANCY: AC-06 mô tả public hoặc user có quyền truy cập và diagram API #12 có nhánh 403, nhưng API #11 trong list_api.md chỉ khai báo 404/500 và là public.`
- `RUNTIME_STATUS: chưa runtime/OpenAPI verified; tài liệu là design-only.`

## Security note

- `Chỉ đọc resource thuộc course PUBLISHED theo nguồn hiện có; không trả token, credential, raw SQL hoặc storage internals.`
- `Resource-level visibility/access chưa thể xác định do ERD thiếu cột visibility; cần chốt trước implementation.`

## Performance note

- `Scope resource bằng quan hệ lesson/course; không thêm index, cache hoặc order policy khi nguồn chưa xác nhận.`
- `Query không có pagination contract; cardinality response cần được chốt trước khi triển khai.`

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
