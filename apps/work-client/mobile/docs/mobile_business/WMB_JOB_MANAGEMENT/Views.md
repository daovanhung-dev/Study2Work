# View inventory — WMB_JOB_MANAGEMENT

Mỗi view được ghi đúng một lần; status phản ánh current source, không phải business approval.

| View ID | Widget | Source file | Status | Current behavior |
|---|---|---|---|---|
| WMB_JOB_MANAGEMENT-V01 | `DangTinTuyenDung` | `lib/views/trang_chu/main/dang_tin_tuyen_dung.dart` | WIRED | Form đăng tin, tạo map JD và insert bằng company id. |
| WMB_JOB_MANAGEMENT-V02 | `QuanLyJob` | `lib/views/trang_chu/tien_ich/Quan_ly_job/quan_ly_job.dart` | WIRED | Danh sách JD theo company và route detail/post form. |
| WMB_JOB_MANAGEMENT-V03 | `XemChiTietJD` | `lib/views/trang_chu/tien_ich/Quan_ly_job/chi_tiet_job.dart` | WIRED | FutureBuilder load JD detail bằng helper Neon. |

## WMB_JOB_MANAGEMENT-V01 — DangTinTuyenDung

- **Source:** `lib/views/trang_chu/main/dang_tin_tuyen_dung.dart`
- **Status:** WIRED
- **Function:** WMB_JOB_MANAGEMENT-FN01
- **Current behavior:** Form đăng tin, tạo map JD và insert bằng company id.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMB_JOB_MANAGEMENT-V02 — QuanLyJob

- **Source:** `lib/views/trang_chu/tien_ich/Quan_ly_job/quan_ly_job.dart`
- **Status:** WIRED
- **Function:** WMB_JOB_MANAGEMENT-FN02
- **Current behavior:** Danh sách JD theo company và route detail/post form.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

## WMB_JOB_MANAGEMENT-V03 — XemChiTietJD

- **Source:** `lib/views/trang_chu/tien_ich/Quan_ly_job/chi_tiet_job.dart`
- **Status:** WIRED
- **Function:** WMB_JOB_MANAGEMENT-FN03
- **Current behavior:** FutureBuilder load JD detail bằng helper Neon.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

