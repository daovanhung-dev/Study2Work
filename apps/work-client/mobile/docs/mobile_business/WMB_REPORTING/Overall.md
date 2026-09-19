# WMB_REPORTING / Thống kê và báo cáo

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

- **Mục đích:** Hiển thị báo cáo/thống kê doanh nghiệp bằng local presentation data.
- **Actor:** Doanh nghiệp
- **Trong phạm vi:** View/controller/helper/model trace và side effect đã có evidence.
- **Ngoài phạm vi:** API/schema mới, migration, runtime implementation và production behavior chưa được chốt.
- **Boundary:** TrangChu → EmployeeReportUI active report; ThongKeScreen legacy.

## Current data flow

| Nhóm | Evidence |
|---|---|
| Data | EmployeeReportUI dùng fl_chart/local data; ThongKeScreen là legacy. |
| Integration | `lib/views/trang_chu/tien_ich/Thong_ke/thong_ke_bao_cao.dart`; `lib/views/trang_chu/tien_ich/Thong_ke/thong_ke.dart`; `lib/views/trang_chu/main/trang_chu.dart` |
| Side effect | TrangChu → EmployeeReportUI active report; ThongKeScreen legacy. |
| Security | Không ghi credential literal; direct client data access là prototype boundary. |

## WMB_REPORTING-BR01 — Current source rule

Report hiện là presentation surface; source chưa chứng minh metric backend contract.

- Cách kiểm tra: đối chiếu exact source paths trong [Import_File.md](Import_File.md).
- Status: CURRENT_SOURCE_RULE, chưa phải approved business requirement.

## Open questions

- **OPEN QUESTION:** Cần chốt metric definition, source data, date range, export và access control.
- BA/PO phải chốt các rule chưa có evidence trước khi code feature mới.

## Traceability

| Requirement/evidence | Feature | Rule | Functions | Views | Source | Tests |
|---|---|---|---|---|---|---|
| User request + current source inventory | WMB_REPORTING-F01 | WMB_REPORTING-BR01 | WMB_REPORTING-FN01..FN02 | WMB_REPORTING-V01..V02 | [Import_File.md](Import_File.md) | WMB_REPORTING-TC01..TC02 |

