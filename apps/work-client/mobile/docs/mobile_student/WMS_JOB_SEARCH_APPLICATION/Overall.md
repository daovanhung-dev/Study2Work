# WMS_JOB_SEARCH_APPLICATION / Tìm việc và ứng tuyển

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

- **Mục đích:** Tải JD, lọc local, xem chi tiết và gửi application.
- **Actor:** Sinh viên
- **Trong phạm vi:** View/controller/helper/model trace và side effect đã có evidence.
- **Ngoài phạm vi:** API/schema mới, migration, runtime implementation và production behavior chưa được chốt.
- **Boundary:** TimKiemViecView → TimKiemCtrl → JD model → XemChiTietView → UngTuyenCtrl → UngVien Neon.

## Current data flow

| Nhóm | Evidence |
|---|---|
| Data | JD/TopJD trong Neon; filter local; UngVien insert có duplicate check theo helper/controller. |
| Integration | `lib/views/tim_kiem_cong_viec/tim_kiem_job.dart`; `lib/views/trang_chu/main/xem_chi_tiet_view.dart`; `lib/views/trang_chu/main/dang_tin_tuyen_dung.dart` |
| Side effect | TimKiemViecView → TimKiemCtrl → JD model → XemChiTietView → UngTuyenCtrl → UngVien Neon. |
| Security | Không ghi credential literal; direct client data access là prototype boundary. |

## WMS_JOB_SEARCH_APPLICATION-BR01 — Current source rule

Ứng tuyển dùng cached student id, resolve company từ JD và tránh insert duplicate theo source.

- Cách kiểm tra: đối chiếu exact source paths trong [Import_File.md](Import_File.md).
- Status: CURRENT_SOURCE_RULE, chưa phải approved business requirement.

## Open questions

- **OPEN QUESTION:** Cần chốt application status lifecycle, validation CV và error copy.
- BA/PO phải chốt các rule chưa có evidence trước khi code feature mới.

## Traceability

| Requirement/evidence | Feature | Rule | Functions | Views | Source | Tests |
|---|---|---|---|---|---|---|
| User request + current source inventory | WMS_JOB_SEARCH_APPLICATION-F01 | WMS_JOB_SEARCH_APPLICATION-BR01 | WMS_JOB_SEARCH_APPLICATION-FN01..FN03 | WMS_JOB_SEARCH_APPLICATION-V01..V03 | [Import_File.md](Import_File.md) | WMS_JOB_SEARCH_APPLICATION-TC01..TC03 |

