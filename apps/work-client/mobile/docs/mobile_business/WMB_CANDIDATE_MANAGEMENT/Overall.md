# WMB_CANDIDATE_MANAGEMENT / Ứng viên và lọc CV

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

- **Mục đích:** Tìm kiếm, xem và thao tác với ứng viên/CV trong phạm vi doanh nghiệp.
- **Actor:** Doanh nghiệp
- **Trong phạm vi:** View/controller/helper/model trace và side effect đã có evidence.
- **Ngoài phạm vi:** API/schema mới, migration, runtime implementation và production behavior chưa được chốt.
- **Boundary:** UngVien/EmployeeSearchUI → controller/helper CV → CV/UngVien → status/delete/conversation/notification.

## Current data flow

| Nhóm | Evidence |
|---|---|
| Data | CV/UngVien/DoanChat/Chat qua Neon; LocCV local filter; AI helper có response contract incomplete. |
| Integration | `lib/views/ung_vien/ung_vien.dart`; `lib/views/trang_chu/tien_ich/Tim_kiem_nhan_su/tim_kiem_nhan_su.dart`; `lib/views/trang_chu/tien_ich/Loc_cv/loc_cv_filter.dart` |
| Side effect | UngVien/EmployeeSearchUI → controller/helper CV → CV/UngVien → status/delete/conversation/notification. |
| Security | Không ghi credential literal; direct client data access là prototype boundary. |

## WMB_CANDIDATE_MANAGEMENT-BR01 — Current source rule

Status mutation có thể tạo DoanChat và Chat notification; filter chưa persistence.

- Cách kiểm tra: đối chiếu exact source paths trong [Import_File.md](Import_File.md).
- Status: CURRENT_SOURCE_RULE, chưa phải approved business requirement.

## Open questions

- **OPEN QUESTION:** Cần chốt status machine, quyền xem CV, AI output và privacy/retention.
- BA/PO phải chốt các rule chưa có evidence trước khi code feature mới.

## Traceability

| Requirement/evidence | Feature | Rule | Functions | Views | Source | Tests |
|---|---|---|---|---|---|---|
| User request + current source inventory | WMB_CANDIDATE_MANAGEMENT-F01 | WMB_CANDIDATE_MANAGEMENT-BR01 | WMB_CANDIDATE_MANAGEMENT-FN01..FN04 | WMB_CANDIDATE_MANAGEMENT-V01..V04 | [Import_File.md](Import_File.md) | WMB_CANDIDATE_MANAGEMENT-TC01..TC04 |

