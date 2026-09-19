# View inventory — WMB_HOME_DASHBOARD

Mỗi view được ghi đúng một lần; status phản ánh current source, không phải business approval.

| View ID | Widget | Source file | Status | Current behavior |
|---|---|---|---|---|
| WMB_HOME_DASHBOARD-V01 | `TrangChu` | `lib/views/trang_chu/main/trang_chu.dart` | WIRED | Dashboard tới jobs, top CV, candidates, internship, interview, school link, reports. |
| WMB_HOME_DASHBOARD-V02 | `ThongBao` | `lib/views/trang_chu/main/thong_bao.dart` | UI-ONLY | Static notification list và detail dialog. |
| WMB_HOME_DASHBOARD-V03 | `ThongTinChiTiet` | `lib/views/trang_chu/main/thong_tin_chi_tiet.dart` | UI-ONLY | Static profile/detail presentation. |
| WMB_HOME_DASHBOARD-V04 | `XemChiTiet` | `lib/views/trang_chu/main/xem_chi_tiet.dart` | LEGACY | Static detail screen retained beside active variant. |
| WMB_HOME_DASHBOARD-V05 | `XemChiTietView` | `lib/views/trang_chu/main/xem_chi_tiet_view.dart` | WIRED | FutureBuilder CV/detail và notification navigation. |

## WMB_HOME_DASHBOARD-V01 — TrangChu

- **Source:** `lib/views/trang_chu/main/trang_chu.dart`
- **Status:** WIRED
- **Function:** WMB_HOME_DASHBOARD-FN01
- **Current behavior:** Dashboard tới jobs, top CV, candidates, internship, interview, school link, reports.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMB_HOME_DASHBOARD-V02 — ThongBao

- **Source:** `lib/views/trang_chu/main/thong_bao.dart`
- **Status:** UI-ONLY
- **Function:** WMB_HOME_DASHBOARD-FN02
- **Current behavior:** Static notification list và detail dialog.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMB_HOME_DASHBOARD-V03 — ThongTinChiTiet

- **Source:** `lib/views/trang_chu/main/thong_tin_chi_tiet.dart`
- **Status:** UI-ONLY
- **Function:** WMB_HOME_DASHBOARD-FN03
- **Current behavior:** Static profile/detail presentation.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMB_HOME_DASHBOARD-V04 — XemChiTiet

- **Source:** `lib/views/trang_chu/main/xem_chi_tiet.dart`
- **Status:** LEGACY
- **Function:** WMB_HOME_DASHBOARD-FN04
- **Current behavior:** Static detail screen retained beside active variant.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMB_HOME_DASHBOARD-V05 — XemChiTietView

- **Source:** `lib/views/trang_chu/main/xem_chi_tiet_view.dart`
- **Status:** WIRED
- **Function:** WMB_HOME_DASHBOARD-FN05
- **Current behavior:** FutureBuilder CV/detail và notification navigation.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

