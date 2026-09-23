# Function list — WMB_CANDIDATE_MANAGEMENT

## WMB_CANDIDATE_MANAGEMENT-FN01 — UngVien interaction

- **View:** WMB_CANDIDATE_MANAGEMENT-V01
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_CANDIDATE_MANAGEMENT-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Candidate/application list, status actions, candidate detail.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/ung_vien/ung_vien.dart`.

## WMB_CANDIDATE_MANAGEMENT-TC01 — UngVien verification case

- **Covers:** WMB_CANDIDATE_MANAGEMENT-FN01 và WMB_CANDIDATE_MANAGEMENT-V01.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMB_CANDIDATE_MANAGEMENT-FN02 — EmployeeSearchUI interaction

- **View:** WMB_CANDIDATE_MANAGEMENT-V02
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_CANDIDATE_MANAGEMENT-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Candidate search dùng CV helper và AI prompt helper.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** WIRED, `lib/views/trang_chu/tien_ich/Tim_kiem_nhan_su/tim_kiem_nhan_su.dart`.

## WMB_CANDIDATE_MANAGEMENT-TC02 — EmployeeSearchUI verification case

- **Covers:** WMB_CANDIDATE_MANAGEMENT-FN02 và WMB_CANDIDATE_MANAGEMENT-V02.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMB_CANDIDATE_MANAGEMENT-FN03 — LocCV interaction

- **View:** WMB_CANDIDATE_MANAGEMENT-V03
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_CANDIDATE_MANAGEMENT-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Local project/job/skill filter; chưa remote persistence.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** SOURCE-ONLY, `lib/views/trang_chu/tien_ich/Loc_cv/loc_cv_filter.dart`.

## WMB_CANDIDATE_MANAGEMENT-TC03 — LocCV verification case

- **Covers:** WMB_CANDIDATE_MANAGEMENT-FN03 và WMB_CANDIDATE_MANAGEMENT-V03.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## WMB_CANDIDATE_MANAGEMENT-FN04 — LocCvPlaceholderScreen interaction

- **View:** WMB_CANDIDATE_MANAGEMENT-V04
- **Input/output:** Route entry, user input or local state → widget/model/navigation result.
- **Permission:** Actor Doanh nghiệp; production permission chưa có contract.
- **Rule:** WMB_CANDIDATE_MANAGEMENT-BR01
- **Transaction/idempotency:** Không thêm policy ngoài source; no persistence nếu view không có persistence evidence.
- **Side effect:** Placeholder retained ngoài active route.
- **Failure:** Giữ loading/empty/error/false behavior hiện tại; không thêm fallback chưa có evidence.
- **Status/source:** PLACEHOLDER, `lib/views/trang_chu/tien_ich/Loc_cv/loc_cv_placeholder.dart`.

## WMB_CANDIDATE_MANAGEMENT-TC04 — LocCvPlaceholderScreen verification case

- **Covers:** WMB_CANDIDATE_MANAGEMENT-FN04 và WMB_CANDIDATE_MANAGEMENT-V04.
- **Scenario:** Mở view theo current route/source composition; kiểm tra success và state phù hợp.
- **Expected:** UI/side effect khớp source; không yêu cầu behavior ngoài contract.
- **Verification:** Static source-backed; runtime unverified khi Flutter/Dart không có.

## Test matrix

| Test ID | View | Scenario | Result |
|---|---|---|---|
| WMB_CANDIDATE_MANAGEMENT-TC01 | WMB_CANDIDATE_MANAGEMENT-V01 | UngVien happy/error/empty state phù hợp | Runtime-unverified |
| WMB_CANDIDATE_MANAGEMENT-TC02 | WMB_CANDIDATE_MANAGEMENT-V02 | EmployeeSearchUI happy/error/empty state phù hợp | Runtime-unverified |
| WMB_CANDIDATE_MANAGEMENT-TC03 | WMB_CANDIDATE_MANAGEMENT-V03 | LocCV happy/error/empty state phù hợp | Runtime-unverified |
| WMB_CANDIDATE_MANAGEMENT-TC04 | WMB_CANDIDATE_MANAGEMENT-V04 | LocCvPlaceholderScreen happy/error/empty state phù hợp | Runtime-unverified |

