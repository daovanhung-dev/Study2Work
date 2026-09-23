# WMB_JOB_MANAGEMENT / Đăng và quản lý tin tuyển dụng

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

- **Mục đích:** Tạo, liệt kê và xem chi tiết JD thuộc doanh nghiệp hiện tại.
- **Actor:** Doanh nghiệp
- **Trong phạm vi:** View/controller/helper/model trace và side effect đã có evidence.
- **Ngoài phạm vi:** API/schema mới, migration, runtime implementation và production behavior chưa được chốt.
- **Boundary:** TrangChu → DangTinTuyenDung hoặc QuanLyJob → helper insert/get/detail → JD model.

## Current data flow

| Nhóm | Evidence |
|---|---|
| Data | JD trong Neon; company id từ SQLite cache; form map chuyển thành parameterized SQL. |
| Integration | `lib/views/trang_chu/main/dang_tin_tuyen_dung.dart`; `lib/views/trang_chu/tien_ich/Quan_ly_job/quan_ly_job.dart`; `lib/views/trang_chu/tien_ich/Quan_ly_job/chi_tiet_job.dart` |
| Side effect | TrangChu → DangTinTuyenDung hoặc QuanLyJob → helper insert/get/detail → JD model. |
| Security | Không ghi credential literal; direct client data access là prototype boundary. |

## WMB_JOB_MANAGEMENT-BR01 — Current source rule

Danh sách job scope theo doanh nghiệp hiện tại; helper dùng Neon parameterized SQL.

- Cách kiểm tra: đối chiếu exact source paths trong [Import_File.md](Import_File.md).
- Status: CURRENT_SOURCE_RULE, chưa phải approved business requirement.

## Open questions

- **OPEN QUESTION:** Cần chốt edit/delete UX, validation fields và JD lifecycle.
- BA/PO phải chốt các rule chưa có evidence trước khi code feature mới.

## Traceability

| Requirement/evidence | Feature | Rule | Functions | Views | Source | Tests |
|---|---|---|---|---|---|---|
| User request + current source inventory | WMB_JOB_MANAGEMENT-F01 | WMB_JOB_MANAGEMENT-BR01 | WMB_JOB_MANAGEMENT-FN01..FN03 | WMB_JOB_MANAGEMENT-V01..V03 | [Import_File.md](Import_File.md) | WMB_JOB_MANAGEMENT-TC01..TC03 |

