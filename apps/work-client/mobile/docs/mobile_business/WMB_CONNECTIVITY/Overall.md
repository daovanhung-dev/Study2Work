# WMB_CONNECTIVITY / Kiểm tra kết nối

## Evidence và status

| Trục | Giá trị |
|---|---|
| Lifecycle | Current |
| DD decision | Draft |
| Implementation | Source-only |
| Verification | Static-verified; Runtime-unverified |
| Source baseline | 212455f627846c0a3dc56107ee162415014d85b5 |
| Evidence | User request, mobile-work context và exact Flutter source |
| Business source | Chưa có BD/BRD mobile; unresolved decisions là OPEN QUESTION |

## Mục đích và boundary

- **Mục đích:** Hiển thị connectivity và cho phép retry/exit về login.
- **Actor:** Doanh nghiệp
- **Trong phạm vi:** View/controller/helper/model trace và side effect đã có evidence.
- **Ngoài phạm vi:** API/schema mới, migration, runtime implementation và production behavior chưa được chốt.
- **Boundary:** KiemTraWifiView → connectivity check → retry hoặc route về DangNhap.

## Current data flow

| Nhóm | Evidence |
|---|---|
| Data | Connectivity listener/check trong view; chưa có storage/backend contract. |
| Integration | `lib/views/kiem_tra_wifi.dart`; `lib/views/dang_nhap/dang_nhap.dart`; `lib/main.dart` |
| Side effect | KiemTraWifiView → connectivity check → retry hoặc route về DangNhap. |
| Security | Không ghi credential literal; direct client data access là prototype boundary. |

## WMB_CONNECTIVITY-BR01 — Current source rule

View không có caller từ main.dart/menu.dart nên không claim active startup route.

- Cách kiểm tra: đối chiếu exact source paths trong [Import_File.md](Import_File.md).
- Status: CURRENT_SOURCE_RULE, chưa phải approved business requirement.

## Open questions

- **OPEN QUESTION:** Cần quyết định có đưa vào startup/error boundary hay giữ compatibility-only.
- BA/PO phải chốt các rule chưa có evidence trước khi code feature mới.

## Traceability

| Requirement/evidence | Feature | Rule | Functions | Views | Source | Tests |
|---|---|---|---|---|---|---|
| User request + current source inventory | WMB_CONNECTIVITY-F01 | WMB_CONNECTIVITY-BR01 | WMB_CONNECTIVITY-FN01..FN01 | WMB_CONNECTIVITY-V01..V01 | [Import_File.md](Import_File.md) | WMB_CONNECTIVITY-TC01..TC01 |

