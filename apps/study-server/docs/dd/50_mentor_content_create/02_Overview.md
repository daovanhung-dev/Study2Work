---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "50"
api_name: "Tạo nội dung mới Conditional"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #50 |
| Tên | Tạo nội dung mới Conditional |
| Endpoint | `POST /api/v1/mentor/content` |
| Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Mentor cần quyền quản lý course theo AC-22; principal-to-course check chưa có implementation source. |
| Success | HTTP 201 `DESIGN_RESOURCE_CREATED`; `ApiEnvelope<Content>`. |
| Errors | Đúng catalog: 401, 403, 422, 500 với `DESIGN_*` tương ứng. |
| Runtime | Chưa có route/module/test API #50 (`UNWIRED` / `NOT_FOUND`). |

## Mục tiêu và ranh giới

Tạo một logical Content gắn với `course_id` trong request. Không đặc tả thay API #49 (đọc cây), #51 (cập nhật), #52 (publish/unpublish), hoặc #53 (xóa). AC-22 mô tả POST → `INSERT Content` → reload cây nội dung.

AC-33 có precondition là đã có content `PENDING_REVIEW` trong hàng đợi duyệt. Vì vậy DD ghi `PENDING_REVIEW` là trạng thái ban đầu đề xuất (`DERIVED`); AC-33 không chỉ ra physical schema. Quy tắc root placement và order được ghi là `DERIVED` đề xuất vì request không có `parent_id`/`order`.

## Luồng mức cao

1. Đọc Bearer JWT và body theo catalog.
2. Yêu cầu principal có role Mentor; kiểm tra quyền quản lý course theo AC-22. Binding principal và quan hệ assignment chưa được source xác nhận.
3. Validate kiểu/required fields theo contract. Chi tiết enum `ContentType` và schema `payload` cần nguồn.
4. Tạo logical Content ở trạng thái `PENDING_REVIEW`. Candidate đơn giản: `parent_id=null`, `order` nối tiếp trong nhóm root của course; cả hai là `DERIVED`, chưa được approved.
5. Persist một Content và trả HTTP 201 `ApiEnvelope<Content>` theo đúng business code.
6. AC-22 mô tả reload cây; đó là bước consumer sau create, không phải response thứ hai của API này.

## Quy ước bằng chứng

- `DIRECT`: catalog/diagram nêu trực tiếp.
- `DERIVED`: đề xuất đơn giản từ flow, cần xác nhận trước implementation.
- `SOURCE_REQUIRED`: thiếu schema hoặc quy tắc nguồn; không giả lập SQL.
- `UNWIRED` / `NOT_FOUND`: chưa có route/module/test trong source hiện tại.

## Discrepancy cần lưu ý khi implementation

Nếu route được nối mà chưa được thêm vào `DESIGN_CONTRACT_PATHS`, middleware hiện có thể phát `VALIDATION_ERROR` hoặc `INTERNAL_SERVER_ERROR` thay cho business code `DESIGN_*` mà catalog yêu cầu. Đây là rủi ro tích hợp có điều kiện; API #50 hiện chưa có behavior runtime.

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
