# View inventory — WMB_SCHOOL_LINK

Mỗi view được ghi đúng một lần; status phản ánh current source, không phải business approval.

| View ID | Widget | Source file | Status | Current behavior |
|---|---|---|---|---|
| WMB_SCHOOL_LINK-V01 | `LienKetScreen` | `lib/views/trang_chu/tien_ich/Lien_ket_nha_truong/lien_ket_nha_truong.dart` | WIRED | University-linking UI shell; no backend contract. |

## WMB_SCHOOL_LINK-V01 — LienKetScreen

- **Source:** `lib/views/trang_chu/tien_ich/Lien_ket_nha_truong/lien_ket_nha_truong.dart`
- **Status:** WIRED
- **Function:** WMB_SCHOOL_LINK-FN01
- **Current behavior:** University-linking UI shell; no backend contract.
- **UI states:** ghi loading/empty/error/success hoặc static theo exact widget tree; không suy ra state mới.
- **Navigation/side effect:** xem function tương ứng trong [Function_List.md](Function_List.md).

