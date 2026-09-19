# View inventory — WMS_JOB_SEARCH_APPLICATION

Mỗi view được ghi đúng một lần; status phản ánh current source, không phải business approval.

| View ID | Widget | Source file | Status | Current behavior |
|---|---|---|---|---|
| WMS_JOB_SEARCH_APPLICATION-V01 | `TimKiemViecView` | `lib/views/tim_kiem_cong_viec/tim_kiem_job.dart` | WIRED | Load all JD, lọc keyword/location/type, mở detail/apply. |
| WMS_JOB_SEARCH_APPLICATION-V02 | `XemChiTietView` | `lib/views/trang_chu/main/xem_chi_tiet_view.dart` | WIRED | JD detail FutureBuilder và application path. |
| WMS_JOB_SEARCH_APPLICATION-V03 | `DangTinTuyenDung` | `lib/views/trang_chu/main/dang_tin_tuyen_dung.dart` | UNWIRED/LEGACY | Student copy dùng out-meta business helper nhưng không nằm trong active menu graph. |

## WMS_JOB_SEARCH_APPLICATION-V01 — TimKiemViecView

- **Source:** `lib/views/tim_kiem_cong_viec/tim_kiem_job.dart`
- **Status:** WIRED
- **Function:** WMS_JOB_SEARCH_APPLICATION-FN01
- **Current behavior:** Load all JD, lọc keyword/location/type, mở detail/apply.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMS_JOB_SEARCH_APPLICATION-V02 — XemChiTietView

- **Source:** `lib/views/trang_chu/main/xem_chi_tiet_view.dart`
- **Status:** WIRED
- **Function:** WMS_JOB_SEARCH_APPLICATION-FN02
- **Current behavior:** JD detail FutureBuilder và application path.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMS_JOB_SEARCH_APPLICATION-V03 — DangTinTuyenDung

- **Source:** `lib/views/trang_chu/main/dang_tin_tuyen_dung.dart`
- **Status:** UNWIRED/LEGACY
- **Function:** WMS_JOB_SEARCH_APPLICATION-FN03
- **Current behavior:** Student copy dùng out-meta business helper nhưng không nằm trong active menu graph.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

