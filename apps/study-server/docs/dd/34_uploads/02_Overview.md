---
title: "Overview"
order: 2
dd_id: "34"
api_name: "Upload file"
source_sheet: "Overview"
status: "Draft — Ready for Review"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 34 |
| Module | STUDENT / LEARNING & INTERACTION; MENTOR / TEACHING & SUPPORT |
| Method | POST |
| Endpoint | /api/v1/uploads |
| Purpose | Upload binary lên S3-compatible storage và lưu metadata UploadAsset có ID BIGINT để consumer tham chiếu. |
| Consumer/Actor | Student; Mentor |
| Authentication | Bearer JWT bắt buộc. |
| Authorization | Student chỉ dùng SUBMISSION; Mentor chỉ dùng LECTURE. Student gửi course_id thì cần enrollment ACTIVE; Mentor bắt buộc course_id và phải là courses.mentor_id trực tiếp. |
| Basis | API catalog/AC-17/AC-21 và quyết định được người dùng duyệt ngày 2026-10-25. |
| Status | Draft — Ready for Review |
| Runtime status | SOURCE_BACKED — route, module, provider và HTTP tests có trong Study Server; migration mới được thêm vào source, live DB chưa xác minh/áp dụng. |
| Transaction | Upload object trước; sau đó INSERT uploads và commit. Nếu DB ghi lỗi, rollback và best-effort delete object. |
| Side effects | Tạo object key UUID dưới uploads/ và một row uploads trạng thái UPLOADED. |

## Sources

- [API catalog](../../../../../docs/lists/list_api.md) — method, path, roles, multipart shape, UploadAsset schema và error set.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-17 và AC-21 sử dụng API upload.
- [AC-17 submission flow](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) và [AC-21 lecture flow](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — ngữ cảnh consumer.
- [API #34 router](../../../app/api/v1.py), [view](../../../app/modules/student/api_34_uploads/view.py), [storage provider](../../../app/service/object_storage/upload.py) và [tests](../../../tests/modules/student/api_34_uploads/test_uploads.py) — current source/test.
- [Legacy bootstrap DDL](../../../../../infra/postgres/study-server/DB.sql) và [migration 004](../../../../../infra/postgres/study-server/migrations/004_uploads.sql) — checked-in schema artifacts, chưa áp dụng lên live DB.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — envelope, trace ID và error data.

## Tables read

- courses — direct owner lookup dùng `courses.id` và `courses.mentor_id` cho LECTURE.
- enrollments — Student SUBMISSION có `course_id` chỉ được tiếp tục khi `user_id`, `course_id` và `status = 'ACTIVE'` khớp.

## Tables write

- uploads — insert owner, purpose, nullable course, storage key, filename, URL, content type, byte size và `UPLOADED` status.

## Mục chú ý

- Purpose enum là `SUBMISSION` hoặc `LECTURE`; status trả về là `UPLOADED`.
- Chấp nhận mọi loại bytes và MIME; không đặt allowlist hoặc giới hạn dung lượng trong ứng dụng.
- Kích thước được đo từ stream đã nhận; object key là UUID do server tạo, không nhận từ client.
- Thiếu filename dùng `upload`; thiếu part Content-Type dùng `application/octet-stream`.
- URL là public URL dựng từ `OBJECT_STORAGE_PUBLIC_BASE_URL` và key.
- Response ID là `uploads.id` BIGSERIAL; migration là source artifact, không chứng minh live schema.

## Assumptions

- DDL target theo lựa chọn người dùng là legacy BIGINT `users`, `courses`, `enrollments`; không gộp V1-PILOT UUID schema.
- Filename multipart được lưu như client gửi; fallback chỉ áp dụng khi filename thiếu/rỗng.
- Content type lấy từ multipart header, không sniff hoặc kiểm tra allowlist.
- Course không tồn tại hoặc không khớp enrollment/direct owner trả 403 theo error set API #34; không thêm 404.

## Conflicts

- ERD V1 trước đây không có uploads table; quyết định hiện tại bổ sung bảng legacy BIGINT riêng và cập nhật checked-in DDL/migration. Live schema vẫn chưa xác minh.
- API #47 vẫn UNWIRED cho đến khi người dùng chốt nghĩa `content:int64`; API #34 không phụ thuộc việc triển khai #47.

## Security note

- Lấy owner ID và role từ access JWT đã xác thực; không nhận owner ID, bucket hoặc storage key từ request.
- Object key UUID tách khỏi filename client, tránh dùng tên file làm đường dẫn storage.
- Error response không trả raw provider/DB exception hoặc credential.

## Performance note

- Dùng `UploadFile` spool stream và boto3 `upload_fileobj`; không đọc toàn bộ file vào application bytes buffer.
- Không có application size cap; proxy/framework infrastructure limits, nếu có, nằm ngoài contract/source này.

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
