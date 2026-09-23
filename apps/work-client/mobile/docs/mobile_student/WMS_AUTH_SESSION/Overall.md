# WMS_AUTH_SESSION / Xác thực và phiên sinh viên

## Evidence và status

| Trục | Giá trị |
|---|---|
| Lifecycle | Current |
| DD decision | Draft |
| Implementation | Partial |
| Verification | Static-verified; Runtime-unverified |
| Source baseline | 212455f627846c0a3dc56107ee162415014d85b5 |
| Evidence | User request, mobile-work context và exact Flutter source |
| Business source | Chưa có BD/BRD mobile; unresolved decisions là OPEN QUESTION |

## Mục đích và boundary

- **Mục đích:** Đăng nhập sinh viên, dựng shell điều hướng và kết thúc phiên cục bộ.
- **Actor:** Sinh viên
- **Trong phạm vi:** View/controller/helper/model trace và side effect đã có evidence.
- **Ngoài phạm vi:** API/schema mới, migration, runtime implementation và production behavior chưa được chốt.
- **Boundary:** DangNhap → dangNhapDN → SinhVienSupabaseHelper → Neon → SQLite insert/save majors → Menu; Setting.dangXuat xóa cache.

## Current data flow

| Nhóm | Evidence |
|---|---|
| Data | Neon SinhVien lookup; SQLite sinhvien.db/bannganh cache; autoLogin source-backed nhưng không phải startup path chính. |
| Integration | `lib/main.dart`; `lib/views/dang_nhap/dang_nhap.dart`; `lib/views/dang_nhap/menu.dart` |
| Side effect | DangNhap → dangNhapDN → SinhVienSupabaseHelper → Neon → SQLite insert/save majors → Menu; Setting.dangXuat xóa cache. |
| Security | Không ghi credential literal; direct client data access là prototype boundary. |

## WMS_AUTH_SESSION-BR01 — Current source rule

Login thành công mở Menu; logout xóa cache sinh viên theo source.

- Cách kiểm tra: đối chiếu exact source paths trong [Import_File.md](Import_File.md).
- Status: CURRENT_SOURCE_RULE, chưa phải approved business requirement.

## Open questions

- **OPEN QUESTION:** Cần chốt password recovery, production session/token và auto-login policy.
- BA/PO phải chốt các rule chưa có evidence trước khi code feature mới.

## Traceability

| Requirement/evidence | Feature | Rule | Functions | Views | Source | Tests |
|---|---|---|---|---|---|---|
| User request + current source inventory | WMS_AUTH_SESSION-F01 | WMS_AUTH_SESSION-BR01 | WMS_AUTH_SESSION-FN01..FN04 | WMS_AUTH_SESSION-V01..V04 | [Import_File.md](Import_File.md) | WMS_AUTH_SESSION-TC01..TC04 |

