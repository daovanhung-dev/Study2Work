# View inventory — WMS_STUDENT_UTILITIES

Mỗi view được ghi đúng một lần; status phản ánh current source, không phải business approval.

| View ID | Widget | Source file | Status | Current behavior |
|---|---|---|---|---|
| WMS_STUDENT_UTILITIES-V01 | `LichPhongVanView` | `lib/views/trang_chu/tien_ich/Lich_PV/lich_pv.dart` | WIRED | Interview utility UI với local state. |
| WMS_STUDENT_UTILITIES-V02 | `HoTroSinhVienView` | `lib/views/trang_chu/tien_ich/Hotro_SV/ho_tro_sv.dart` | WIRED | Student support UI. |
| WMS_STUDENT_UTILITIES-V03 | `KhoaHocView` | `lib/views/trang_chu/tien_ich/Khoa_hoc/khoa_hoc.dart` | WIRED | Student course UI. |
| WMS_STUDENT_UTILITIES-V04 | `TinTucView` | `lib/views/trang_chu/tien_ich/Tin_Tuc/tin_tuc.dart` | WIRED | Student news UI. |

## WMS_STUDENT_UTILITIES-V01 — LichPhongVanView

- **Source:** `lib/views/trang_chu/tien_ich/Lich_PV/lich_pv.dart`
- **Status:** WIRED
- **Function:** WMS_STUDENT_UTILITIES-FN01
- **Current behavior:** Interview utility UI với local state.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMS_STUDENT_UTILITIES-V02 — HoTroSinhVienView

- **Source:** `lib/views/trang_chu/tien_ich/Hotro_SV/ho_tro_sv.dart`
- **Status:** WIRED
- **Function:** WMS_STUDENT_UTILITIES-FN02
- **Current behavior:** Student support UI.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMS_STUDENT_UTILITIES-V03 — KhoaHocView

- **Source:** `lib/views/trang_chu/tien_ich/Khoa_hoc/khoa_hoc.dart`
- **Status:** WIRED
- **Function:** WMS_STUDENT_UTILITIES-FN03
- **Current behavior:** Student course UI.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMS_STUDENT_UTILITIES-V04 — TinTucView

- **Source:** `lib/views/trang_chu/tien_ich/Tin_Tuc/tin_tuc.dart`
- **Status:** WIRED
- **Function:** WMS_STUDENT_UTILITIES-FN04
- **Current behavior:** Student news UI.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

