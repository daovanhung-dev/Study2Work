# WMS_STUDENT_UTILITIES / Tiện ích sinh viên

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

- **Mục đích:** Các utility view interview, support, course và news hiện có.
- **Actor:** Sinh viên
- **Trong phạm vi:** View/controller/helper/model trace và side effect đã có evidence.
- **Ngoài phạm vi:** API/schema mới, migration, runtime implementation và production behavior chưa được chốt.
- **Boundary:** TrangChu → utility route → local presentation/state; không claim API/storage.

## Current data flow

| Nhóm | Evidence |
|---|---|
| Data | Local UI/state; chưa có persistence/backend contract được xác nhận. |
| Integration | `lib/views/trang_chu/tien_ich/Lich_PV/lich_pv.dart`; `lib/views/trang_chu/tien_ich/Hotro_SV/ho_tro_sv.dart`; `lib/views/trang_chu/tien_ich/Khoa_hoc/khoa_hoc.dart` |
| Side effect | TrangChu → utility route → local presentation/state; không claim API/storage. |
| Security | Không ghi credential literal; direct client data access là prototype boundary. |

## WMS_STUDENT_UTILITIES-BR01 — Current source rule

Các view là UI/static utility theo source; không biến local state thành backend behavior.

- Cách kiểm tra: đối chiếu exact source paths trong [Import_File.md](Import_File.md).
- Status: CURRENT_SOURCE_RULE, chưa phải approved business requirement.

## Open questions

- **OPEN QUESTION:** Cần chốt owner, source data, persistence và acceptance cho từng utility.
- BA/PO phải chốt các rule chưa có evidence trước khi code feature mới.

## Traceability

| Requirement/evidence | Feature | Rule | Functions | Views | Source | Tests |
|---|---|---|---|---|---|---|
| User request + current source inventory | WMS_STUDENT_UTILITIES-F01 | WMS_STUDENT_UTILITIES-BR01 | WMS_STUDENT_UTILITIES-FN01..FN04 | WMS_STUDENT_UTILITIES-V01..V04 | [Import_File.md](Import_File.md) | WMS_STUDENT_UTILITIES-TC01..TC04 |

