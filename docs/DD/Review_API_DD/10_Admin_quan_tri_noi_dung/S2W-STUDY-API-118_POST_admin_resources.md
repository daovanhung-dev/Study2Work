# Review API DD — S2W-STUDY-API-118

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-118_POST_admin_resources.xlsx`
- Method + endpoint: `POST /api/v1/admin/resources`
- Kết luận: **CẦN SỬA**

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | DD ghi 44 nguồn/không schema, trong khi có 48 file và SQL schema. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật inventory/schema/precedence. |
| P0 | `2.Response!D9:D11`, `2.Response!A32` | Envelope `{data,meta}`/`{error}` và snake_case không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical success/error và `traceId`. |
| P1 | `2.Response!A21` | Create response có pagination mẫu thừa. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ `meta`; trả resource vừa tạo. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | INSERT `<mapping>` còn placeholder trong khi checklist đã tick không placeholder/review schema. | `docs/BD/base/0. Study2Work_System_Architecture.md:738-752`; SQL `:472-484` | Viết INSERT/relations cụ thể và cập nhật checklist trung thực. |
| P0 | `1.Request!D21:I30`, `7.DB_Insert_Main!B8:I19` | Mapping sai schema: `description`, `usage_rights`, `owner`, `file_id_or_url`, `lesson_ids`, `course_ids`, `created_*` không tồn tại; cột thật là `lesson_id`, `resource_url`, `usage_right_status`. | SQL `:115-132,472-484`; BD-10 `:112-121` | Chốt resource model: một `lessonId` theo schema hiện tại hoặc thêm association tables; map đúng `resource_url/usage_right_status`. |
| P0 | `1.Request!D21:I27` | Enum type thiếu `VIDEO`; `usage_rights` là free String thay vì enum; union `file_id_or_url` mơ hồ giữa asset ID và URL. | SQL `:115-132`; pre-publish rule BD-10 `:146-155,176` | Bổ sung enum đầy đủ; dùng discriminated source `{kind:FILE_ASSET,fileAssetId}` hoặc `{kind:EXTERNAL_URL,url}`; validate usage-right enum. |
| P0 | `1.Request!D26:D27`, `3.Data mapping!C13:G15` | Client tự gửi `owner` String; không có upload authorization, checksum/scan status, signed URL hay SSRF/link validation. Raw URL được persist trực tiếp. | BD-10 `:120,155,176`; architecture security/transaction `docs/BD/base/0. Study2Work_System_Architecture.md:601-628,693-700` | Owner lấy từ authenticated actor/responsible-party ID; dùng FileAsset/upload flow, malware scan, allowlist/SSRF protection và signed short-lived access. |

## Checklist duyệt lại

- [ ] Source/envelope/pagination đã sửa.
- [ ] Material type/usage-right enum đầy đủ.
- [ ] File asset và external URL là union phân biệt rõ.
- [ ] Mapping dùng cột/relations thật.
- [ ] Lesson/course attachment semantics được chốt.
- [ ] Owner lấy từ server và có FK.
- [ ] Upload scan/signed URL/SSRF controls được đặc tả.
- [ ] OpenAPI/test bao phủ invalid rights, bad link, duplicate/retry.
