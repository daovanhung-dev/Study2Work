# WMB_INTERNSHIP / Chương trình thực tập

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

- **Mục đích:** Hiển thị listing/form chương trình thực tập hiện có.
- **Actor:** Doanh nghiệp
- **Trong phạm vi:** View/controller/helper/model trace và side effect đã có evidence.
- **Ngoài phạm vi:** API/schema mới, migration, runtime implementation và production behavior chưa được chốt.
- **Boundary:** TrangChu → ChuongTrinhThucTapPage → local listing/form; ThucTapScreen là legacy.

## Current data flow

| Nhóm | Evidence |
|---|---|
| Data | Local page/form state; chưa có backend persistence. |
| Integration | `lib/views/trang_chu/tien_ich/Chuong_trinh_thuc_te/chuong_trinh_thuc_tap_page.dart`; `lib/views/trang_chu/tien_ich/Chuong_trinh_thuc_te/chuong_trinh_thuc_tap.dart`; `lib/views/trang_chu/main/trang_chu.dart` |
| Side effect | TrangChu → ChuongTrinhThucTapPage → local listing/form; ThucTapScreen là legacy. |
| Security | Không ghi credential literal; direct client data access là prototype boundary. |

## WMB_INTERNSHIP-BR01 — Current source rule

Page là active theo composition; legacy screen ngoài active route.

- Cách kiểm tra: đối chiếu exact source paths trong [Import_File.md](Import_File.md).
- Status: CURRENT_SOURCE_RULE, chưa phải approved business requirement.

## Open questions

- **OPEN QUESTION:** Cần chốt entity, owner, persistence, approval và notification flow.
- BA/PO phải chốt các rule chưa có evidence trước khi code feature mới.

## Traceability

| Requirement/evidence | Feature | Rule | Functions | Views | Source | Tests |
|---|---|---|---|---|---|---|
| User request + current source inventory | WMB_INTERNSHIP-F01 | WMB_INTERNSHIP-BR01 | WMB_INTERNSHIP-FN01..FN02 | WMB_INTERNSHIP-V01..V02 | [Import_File.md](Import_File.md) | WMB_INTERNSHIP-TC01..TC02 |
