# WMB_HOME_DASHBOARD / Trang chủ và thông tin doanh nghiệp

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

- **Mục đích:** Dashboard doanh nghiệp, thông báo và các màn hình thông tin/detail.
- **Actor:** Doanh nghiệp
- **Trong phạm vi:** View/controller/helper/model trace và side effect đã có evidence.
- **Ngoài phạm vi:** API/schema mới, migration, runtime implementation và production behavior chưa được chốt.
- **Boundary:** Menu → TrangChu → utility/detail routes; notification route mở ThongBao; active detail dùng XemChiTietView.

## Current data flow

| Nhóm | Evidence |
|---|---|
| Data | Dashboard đọc cache/CV projection và dữ liệu local presentation; detail có controller Neon path. |
| Integration | `lib/views/trang_chu/main/trang_chu.dart`; `lib/views/trang_chu/main/thong_bao.dart`; `lib/views/trang_chu/main/thong_tin_chi_tiet.dart` |
| Side effect | Menu → TrangChu → utility/detail routes; notification route mở ThongBao; active detail dùng XemChiTietView. |
| Security | Không ghi credential literal; direct client data access là prototype boundary. |

## WMB_HOME_DASHBOARD-BR01 — Current source rule

XemChiTiet legacy tồn tại song song với XemChiTietView; không claim legacy là active.

- Cách kiểm tra: đối chiếu exact source paths trong [Import_File.md](Import_File.md).
- Status: CURRENT_SOURCE_RULE, chưa phải approved business requirement.

## Open questions

- **OPEN QUESTION:** Cần chốt source of truth cho notification/profile/detail và legacy policy.
- BA/PO phải chốt các rule chưa có evidence trước khi code feature mới.

## Traceability

| Requirement/evidence | Feature | Rule | Functions | Views | Source | Tests |
|---|---|---|---|---|---|---|
| User request + current source inventory | WMB_HOME_DASHBOARD-F01 | WMB_HOME_DASHBOARD-BR01 | WMB_HOME_DASHBOARD-FN01..FN05 | WMB_HOME_DASHBOARD-V01..V05 | [Import_File.md](Import_File.md) | WMB_HOME_DASHBOARD-TC01..TC05 |

