# WMB_INTERVIEW / Lịch phỏng vấn

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

- **Mục đích:** Hiển thị và thao tác local interview schedule/form.
- **Actor:** Doanh nghiệp
- **Trong phạm vi:** View/controller/helper/model trace và side effect đã có evidence.
- **Ngoài phạm vi:** API/schema mới, migration, runtime implementation và production behavior chưa được chốt.
- **Boundary:** TrangChu → LichPV; LichPhongVanScreen là legacy; form đổi state local.

## Current data flow

| Nhóm | Evidence |
|---|---|
| Data | Local state/dialog; chưa thấy persistence/backend contract. |
| Integration | `lib/views/trang_chu/tien_ich/Lich_phong_van/lich_pv_page.dart`; `lib/views/trang_chu/tien_ich/Lich_phong_van/lich_phong_van.dart`; `lib/views/trang_chu/main/trang_chu.dart` |
| Side effect | TrangChu → LichPV; LichPhongVanScreen là legacy; form đổi state local. |
| Security | Không ghi credential literal; direct client data access là prototype boundary. |

## WMB_INTERVIEW-BR01 — Current source rule

LichPV active theo composition; legacy screen không claim active.

- Cách kiểm tra: đối chiếu exact source paths trong [Import_File.md](Import_File.md).
- Status: CURRENT_SOURCE_RULE, chưa phải approved business requirement.

## Open questions

- **OPEN QUESTION:** Cần chốt entity, persistence, timezone, reminder và quyền sửa lịch.
- BA/PO phải chốt các rule chưa có evidence trước khi code feature mới.

## Traceability

| Requirement/evidence | Feature | Rule | Functions | Views | Source | Tests |
|---|---|---|---|---|---|---|
| User request + current source inventory | WMB_INTERVIEW-F01 | WMB_INTERVIEW-BR01 | WMB_INTERVIEW-FN01..FN02 | WMB_INTERVIEW-V01..V02 | [Import_File.md](Import_File.md) | WMB_INTERVIEW-TC01..TC02 |

