# Function list — WMB_SCHOOL_LINK

## WMB_SCHOOL_LINK-FN01 — LienKetScreen interaction

- **View:** WMB_SCHOOL_LINK-V01
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_SCHOOL_LINK-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** University-linking UI shell; no backend contract.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/trang_chu/tien_ich/Lien_ket_nha_truong/lien_ket_nha_truong.dart`.

## WMB_SCHOOL_LINK-TC01 — LienKetScreen verification case

- **Covers:** WMB_SCHOOL_LINK-FN01 và WMB_SCHOOL_LINK-V01.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## Test matrix

| Test ID | View | Scenario | Result |
|---|---|---|---|
| WMB_SCHOOL_LINK-TC01 | WMB_SCHOOL_LINK-V01 | LienKetScreen happy/error/empty state phù hợp | Runtime-unverified |

