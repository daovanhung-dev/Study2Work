# WMS_HOME_DASHBOARD / Trang chủ và thông tin sinh viên

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

- **Mục đích:** Student home, thông báo, profile/detail presentation và route tới utilities.
- **Actor:** Sinh viên
- **Trong phạm vi:** View/controller/helper/model trace và side effect đã có evidence.
- **Ngoài phạm vi:** API/schema mới, migration, runtime implementation và production behavior chưa được chốt.
- **Boundary:** Menu → TrangChu → notifications/CV/interview/support/course/news/search; route tới `XemChiTietView` được đặc tả tại `WMS_JOB_SEARCH_APPLICATION`.

## Current data flow

| Nhóm | Evidence |
|---|---|
| Data | Top JD/SQLite profile cache và local static presentations; active JD detail có Neon path. |
| Integration | `lib/views/trang_chu/main/trang_chu.dart`; `lib/views/trang_chu/main/thong_bao.dart`; `lib/views/trang_chu/main/thong_tin_chi_tiet.dart` |
| Side effect | Menu → TrangChu → JD detail/notifications/CV/interview/support/course/news/search. |
| Security | Không ghi credential literal; direct client data access là prototype boundary. |

## WMS_HOME_DASHBOARD-BR01 — Current source rule

XemChiTiet legacy tồn tại song song XemChiTietView active; static screens không claim backend.

- Cách kiểm tra: đối chiếu exact source paths trong [Import_File.md](Import_File.md).
- Status: CURRENT_SOURCE_RULE, chưa phải approved business requirement.

## Open questions

- **OPEN QUESTION:** Cần chốt notification/profile source, home content ownership và legacy policy.
- BA/PO phải chốt các rule chưa có evidence trước khi code feature mới.

## Traceability

| Requirement/evidence | Feature | Rule | Functions | Views | Source | Tests |
|---|---|---|---|---|---|---|
| User request + current source inventory | WMS_HOME_DASHBOARD-F01 | WMS_HOME_DASHBOARD-BR01 | WMS_HOME_DASHBOARD-FN01..FN04 | WMS_HOME_DASHBOARD-V01..V04 | [Import_File.md](Import_File.md) | WMS_HOME_DASHBOARD-TC01..TC04 |
