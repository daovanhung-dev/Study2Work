---
title: "Overview"
order: 2
dd_id: "34"
api_name: "Upload file"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 34 |
| Module | STUDENT / LEARNING & INTERACTION; MENTOR / TEACHING & SUPPORT |
| Method | POST |
| Endpoint | /api/v1/uploads |
| Purpose | Nhận file từ Student hoặc Mentor và lưu file vào Object Storage để các API tiếp theo tham chiếu. |
| Runtime status | UNWIRED / NOT_FOUND — chưa có route/module/test API #34 trong Study Server hiện tại. |
| Consumer/Actor | Student; Mentor |
| Authentication | Bearer JWT bắt buộc theo API catalog. |
| Authorization | Role thuộc Student hoặc Mentor; quyền theo purpose/course chưa được định nghĩa. |
| Basis | DIRECT — API catalog, AC-17 và AC-21; các chi tiết upload còn thiếu được giữ là SOURCE_REQUIRED. |
| Status | Draft — Needs Confirmation |
| Transaction | Không có DB transaction được xác định; Object Storage là side effect ngoài hệ thống. |
| Side effects | AC-17/AC-21 mô tả lưu file vào Object Storage; không có mutation DB được chỉ định. |

## Sources

- [API catalog](../../../../../docs/lists/list_api.md) — API #34, UploadAsset và error-code set.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — liên kết endpoint với AC-17 và AC-21.
- [AC-17 submission flow](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — Student chọn file, gọi upload, Object Storage lưu file submission.
- [AC-21 lecture flow](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — Mentor chọn course/file, gọi upload, Object Storage lưu media.
- [DB table notes](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — không có bảng Uploads trong ERD V1; có ghi chú URL nhưng chưa có mapping vật lý.
- [Checked-in DDL](../../../../../infra/postgres/study-server/DB.sql) — physical DDL evidence; không xác nhận live schema.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — envelope, error data và trace ID.
- [API #13 DD](../13_users_me_avatar/02_Overview.md) và [Object Storage adapter](../../../app/service/object_storage/avatar.py) — chỉ là implementation tham chiếu cho avatar, không phải contract của API #34.
- [Current Study router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), route/module/test inventory — đối chiếu trạng thái runtime hiện tại.

## Tables read

- Không có bảng DB read nào được catalog hoặc AC-17/AC-21 chỉ định.
- Nếu cần đọc course để kiểm tra quyền theo course_id, bảng/query/predicate là SOURCE_REQUIRED.

## Tables write

- Không có bảng DB write nào được catalog hoặc AC-17/AC-21 chỉ định.
- Object Storage là external write theo hai flow AC; key, metadata và provider response chưa được xác định.

## Mục chú ý

- Contract yêu cầu multipart với file binary bắt buộc, purpose UploadPurpose bắt buộc, course_id int64 tùy chọn; response là ApiEnvelope<UploadAsset>.
- UploadAsset có id, name, url, content_type, size_bytes, status; UploadStatus chưa có định nghĩa giá trị.
- Tên API trong catalog ghép nhiều nhãn hiển thị thành một chuỗi; DD dùng “Upload file” để định danh endpoint, không bổ sung điều kiện “nếu có”.
- API #34 là upload độc lập; tạo submission hoặc lecture là các API tiếp theo trong AC, không thuộc endpoint này.

## Assumptions

- Giữ nguyên request fields, roles, success response và error codes của API catalog.
- Không thêm giá trị enum, giới hạn MIME/size, object key, URL policy hoặc bảng uploads khi nguồn chưa xác định.
- 07_table.md giữ cấu trúc template nhưng ghi N/A vì không có DB table mapping được xác nhận.

## Conflicts

- API catalog dùng UploadPurpose và UploadStatus nhưng không định nghĩa enum values.
- DB ERD footer ghi “Uploads lưu URL” nhưng không có entity/table Uploads; DB table notes xác nhận uploads không nằm trong 16 bảng ERD V1.
- Current Study runtime không có API #34; trạng thái hiện tại là UNWIRED / NOT_FOUND. API #13 là flow avatar riêng: JSON Data URL, Student-only, giới hạn 5 MiB, fixed object key và lỗi storage 500; không áp dụng các lựa chọn đó cho API #34, vốn khai báo multipart, Student/Mentor và thêm 503.

## Security note

- Contract chỉ cho phép Bearer JWT; không nhận user_id hoặc object key từ request.
- Vai trò hợp lệ là Student/Mentor theo catalog; quyền upload theo purpose, quan hệ với course và ownership chưa được đặc tả.
- Quy tắc kiểm tra nội dung file, tên file và URL truy cập chưa có nguồn; cần được xác nhận trước khi DD chuyển Final hoặc API được triển khai.

## Performance note

- Upload truyền binary tới Object Storage nên phụ thuộc dung lượng file và độ trễ provider.
- Kích thước tối đa, streaming/buffering, timeout, retry, concurrency và cleanup chưa được quy định.
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
