# WMS_COMPATIBILITY / Màn hình compatibility chưa wired

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

- **Mục đích:** Inventory các view tồn tại nhưng chưa có active caller evidence trong student route graph.
- **Actor:** Sinh viên
- **Trong phạm vi:** View/controller/helper/model trace và side effect đã có evidence.
- **Ngoài phạm vi:** API/schema mới, migration, runtime implementation và production behavior chưa được chốt.
- **Boundary:** EmployeeSearchUI → out-meta CV/AI helper path theo source; không có clear active home route.

## Current data flow

| Nhóm | Evidence |
|---|---|
| Data | Out-meta helper/model và UI surface tồn tại; active caller chưa xác nhận. |
| Integration | `lib/views/trang_chu/tien_ich/Tim_kiem_nhan_su/tim_kiem_nhan_su.dart`; `lib/controllers/trang_chu/timkiemctrl.dart`; `lib/controllers/AI/ai_service.dart` |
| Side effect | EmployeeSearchUI → out-meta CV/AI helper path theo source; không có clear active home route. |
| Security | Không ghi credential literal; direct client data access là prototype boundary. |

## WMS_COMPATIBILITY-BR01 — Current source rule

Không nâng view lên active feature chỉ vì file tồn tại.

- Cách kiểm tra: đối chiếu exact source paths trong [Import_File.md](Import_File.md).
- Status: CURRENT_SOURCE_RULE, chưa phải approved business requirement.

## Open questions

- **OPEN QUESTION:** Cần owner quyết định loại bỏ, nối route hay chuyển thành feature chính thức.
- BA/PO phải chốt các rule chưa có evidence trước khi code feature mới.

## Traceability

| Requirement/evidence | Feature | Rule | Functions | Views | Source | Tests |
|---|---|---|---|---|---|---|
| User request + current source inventory | WMS_COMPATIBILITY-F01 | WMS_COMPATIBILITY-BR01 | WMS_COMPATIBILITY-FN01..FN01 | WMS_COMPATIBILITY-V01..V01 | [Import_File.md](Import_File.md) | WMS_COMPATIBILITY-TC01..TC01 |

