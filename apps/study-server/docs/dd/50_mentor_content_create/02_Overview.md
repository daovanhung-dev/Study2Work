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
| Authorization | Shared Bearer/JWT guard yêu cầu role `MENTOR`; current implementation yêu cầu `courses.mentor_id` bằng numeric JWT `sub`. Assigned-course access chưa được source-backed. |
| Success | HTTP 201 `DESIGN_RESOURCE_CREATED`; `ApiEnvelope<Content>`. |
| Errors | Đúng catalog: 401, 403, 422, 500 với `DESIGN_*` tương ứng. |
| Runtime | Route/module và TestClient tests source-backed locally; fake DB tests không xác minh live schema/deployment. |

## Mục tiêu và ranh giới

Tạo một logical Content gắn với `course_id` trong request. Không đặc tả thay API #49 (đọc cây), #51 (cập nhật), #52 (publish/unpublish), hoặc #53 (xóa). AC-22 mô tả POST → `INSERT Content` → reload cây nội dung.

AC-33 queue đọc content `PENDING_REVIEW`. API #50 hiện gán trạng thái này làm lựa chọn `DERIVED` để content mới vào moderation queue. Vì request không có `parent_id`/`order`, implementation tạo root (`parent_id=NULL`) và gán order tiếp theo trong active root siblings, bắt đầu từ 0; course row được khóa trong transaction để tuần tự hóa việc cấp order. Các default này chưa được diagram/catalog xác nhận trực tiếp.

## Luồng mức cao

1. FastAPI parse bốn field bắt buộc; strict signed-int64/string/object types và undeclared fields are rejected.
2. Shared guard yêu cầu Bearer JWT + role Mentor; view khóa course row và dùng `courses.mentor_id` để kiểm tra direct owner.
3. Course không tồn tại hoặc không thuộc Mentor cùng trả 403 `DESIGN_ACCESS_DENIED`; API #50 không thêm 404.
4. Lấy order kế tiếp từ active root siblings (first order 0), insert root Content ở `PENDING_REVIEW` và lưu object payload dưới JSONB.
5. Validate INSERT/RETURNING projection, commit transaction rồi trả HTTP 201 `ApiEnvelope<Content>` với `DESIGN_RESOURCE_CREATED`.
6. AC-22 mô tả reload cây; đó là bước consumer sau create, không phải response thứ hai của API này.

## Quy ước bằng chứng

- `DIRECT`: catalog/diagram nêu trực tiếp.
- `DERIVED`: đề xuất đơn giản từ flow, cần xác nhận trước implementation.
- `SOURCE_REQUIRED`: thiếu schema hoặc quy tắc nguồn; không giả lập SQL.
- `UNWIRED` / `NOT_FOUND`: chưa có route/module/test trong source hiện tại.

## Current source status

Route `/api/v1/mentor/content` hiện nằm trong `DESIGN_CONTRACT_PATHS`, nên framework body errors và unhandled errors dùng `DESIGN_VALIDATION_ERROR`/`DESIGN_INTERNAL_ERROR`. Local route behavior được kiểm tra bằng TestClient; live DB và deployment chưa xác minh.

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
