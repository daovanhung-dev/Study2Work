# WMS_CV_MANAGEMENT / Quản lý CV sinh viên

## Evidence và status

| Trục | Giá trị |
|---|---|
| Lifecycle | Current |
| DD decision | Draft |
| Implementation | Implemented |
| Verification | Static-verified; Runtime-unverified |
| Source baseline | 212455f627846c0a3dc56107ee162415014d85b5 |
| Evidence | User request, mobile-work context và exact Flutter source |
| Business source | Chưa có BD/BRD mobile; unresolved decisions là OPEN QUESTION |

## Mục đích và boundary

- **Mục đích:** Tải, hiển thị và cập nhật CV của sinh viên hiện tại.
- **Actor:** Sinh viên
- **Trong phạm vi:** View/controller/helper/model trace và side effect đã có evidence.
- **Ngoài phạm vi:** API/schema mới, migration, runtime implementation và production behavior chưa được chốt.
- **Boundary:** QuanLyCVView → CVCtrl.getCVById/update → helper student → Neon Cv → form result.

## Current data flow

| Nhóm | Evidence |
|---|---|
| Data | Cached student id từ SQLite; CV đọc/cập nhật qua Neon và model CV. |
| Integration | `lib/views/trang_chu/tien_ich/Quan_ly_CV/quan_ly_cv.dart`; `lib/controllers/trang_chu/quan_ly_CV/quan_ly_job_cv.dart`; `lib/helper_db/sinh_vien/helper_supabase.dart` |
| Side effect | QuanLyCVView → CVCtrl.getCVById/update → helper student → Neon Cv → form result. |
| Security | Không ghi credential literal; direct client data access là prototype boundary. |

## WMS_CV_MANAGEMENT-BR01 — Current source rule

CV scope theo cached student id; JSONB/date mapping nằm ở model/helper source.

- Cách kiểm tra: đối chiếu exact source paths trong [Import_File.md](Import_File.md).
- Status: CURRENT_SOURCE_RULE, chưa phải approved business requirement.

## Open questions

- **OPEN QUESTION:** Cần chốt create/delete/search CV ngoài active edit flow và validation required fields.
- BA/PO phải chốt các rule chưa có evidence trước khi code feature mới.

## Traceability

| Requirement/evidence | Feature | Rule | Functions | Views | Source | Tests |
|---|---|---|---|---|---|---|
| User request + current source inventory | WMS_CV_MANAGEMENT-F01 | WMS_CV_MANAGEMENT-BR01 | WMS_CV_MANAGEMENT-FN01..FN01 | WMS_CV_MANAGEMENT-V01..V01 | [Import_File.md](Import_File.md) | WMS_CV_MANAGEMENT-TC01..TC01 |

