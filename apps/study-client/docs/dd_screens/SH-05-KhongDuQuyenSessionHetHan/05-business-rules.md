# SH-05 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `SH-05-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Phân biệt 401 (hết hạn/thiếu token), 403 (không đủ quyền), bảo toàn redirect an toàn.
- Gate/status (giữ nguyên): **R**
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: 8. Quy tắc bảo mật, khả năng tiếp cận và design system

- Backend là nguồn thẩm quyền về auth/role. Client chỉ ánh xạ HTTP status và business code; không gán Student/Mentor/Admin theo path hoặc mock state.
- Không render token, profile, stack trace, SQL, database schema hoặc reason nội bộ. Refresh token chỉ đi trong HTTPS request body tới R-X01; không vào URL, browser console, analytics event hoặc UI.
- Chỉ dùng redirect nội bộ trong allowlist; kiểm tra lại authorization sau login. Cách truyền/lưu `returnTo` chưa được chọn; không cho phép external/protocol-relative URL, token hoặc PII.
- Không refresh sau 403. `list_screen.md` yêu cầu single-flight coordinator cho request đồng thời và tối đa một refresh/retry mỗi flow 401; Study Web hiện không có source để chứng minh runtime. Refresh token rotation chỉ cho phép dùng token cũ một lần. Không tự retry cùng refresh token khi response outcome mơ hồ.
- Nút có focus nhìn thấy, hỗ trợ bàn phím; status/error feedback có ngữ nghĩa screen-reader; màu không phải tín hiệu duy nhất. Hit target tương tác tối thiểu 44×44px theo guide. Nút copy 40×40 hiện tại cần sửa.
- Design guide Study yêu cầu font local/system, không thêm remote fonts, content width khoảng 1120px và spacing/token chuẩn. HTML hiện nạp Google Fonts/Tailwind CDN và dùng khung rộng khoảng 1440px; bản prototype không được coi là tuân thủ runtime design system.
- Nội dung kỹ thuật ở #1/#6/#11 và response JSON ở #9 cần được UX xác nhận là có nên xuất hiện trên user-facing screen hay chỉ thuộc handoff.

### Trích từ DD nguồn: 9. Blocker, sai khác và câu hỏi mở

| ID | Phân loại | Bằng chứng / vấn đề | Tác động / người cần quyết định |
|---|---|---|---|
| `SH05-B01` | `BLOCKER: CLIENT_SOURCE_NOT_FOUND` | `apps/study-client/src/` không có trong checkout; không tìm thấy router, auth interceptor hoặc UI runtime. | Frontend cần xác nhận route `/forbidden`, entry contract và tích hợp auth manager. |
| `SH05-B02` | `BLOCKER: CLIENT_SESSION_IMPLEMENTATION` | `list_screen.md` §1.2 đã yêu cầu tối đa một refresh/retry và single-flight cho request đồng thời; Study Web source không có để implement/verify. Token persistence, CSRF/XSS mitigation, safe replay eligibility, timeout/ambiguous rotation outcome và session cleanup vẫn chưa được xác nhận. | Frontend/Security/Product cần xác nhận các quyết định session còn mở; không coi single-flight là product rule chưa quyết định và không tự chọn storage. |
| `SH05-B03` | `BLOCKER: SAFE_RETURN_FALLBACK` | Inventory yêu cầu safe return nhưng chưa chốt fallback cho direct-entry 403 hoặc route cũ không còn tồn tại. | Product/UX chốt public fallback và allowlist. |
| `SH05-D01` | `DISCREPANCY: MOCK_ERROR_ENVELOPE` | Prototype dùng `status`, `timestamp`, `AUTHZ_STUDENT_REQUIRED`, `AUTHN_TOKEN_EXPIRED`; source dùng `success`, `businessCode`, `message`, `data`, `meta`, `traceId` và business code `DESIGN_*`. | Không dùng mock payload trong client contract. |
| `SH05-D02` | `DISCREPANCY: ROUTE_TARGETS` | Prototype href `/sh-01-dashboard`, `/sh-02-login`; inventory đề xuất `/` và `/login`. | Sửa theo router thật trước release; hiện chưa có router để xác minh. |
| `SH05-D03` | `DISCREPANCY: SYNTHETIC_DIAGNOSTICS` | `ROLE_NOT_AUTHORIZED_FOR_STUDENT_SCOPE`, `ACCESS_TOKEN_EXPIRED_OR_INVALID`, `tr_403_sec_study` và timestamp là dữ liệu mẫu, không được API #04/R-X01 trả như vậy. | Thay bằng response thật hoặc copy an toàn được UX duyệt. |
| `SH05-D04` | `UX/A11Y` | Hai nút copy dùng cùng handler/giá trị; #10 là 40×40px; clipboard rejection không được xử lý; JSON/reason dài bị cắt/tràn. | UX/A11y review; hợp nhất hoặc đổi nhãn control, nâng target, thêm feedback và xử lý text. |
| `SH05-D05` | `DESIGN_SYSTEM_DRIFT` | Prototype dùng Google Fonts/Tailwind CDN, khung rộng khoảng 1440px; Study guide hướng dẫn font local/system và khoảng 1120px. | Chuẩn hóa trong UI implementation; không sửa `screen.png` nguồn. |
| `SH05-B04` | `NOT_FOUND: BUSINESS_DESIGN` | `docs/BD/` và `docs/BRD/` không có trong checkout; chưa có quyết định wording chính thức cho 401/403. | Product/UX cung cấp copy đã duyệt; dùng thông điệp trung tính đến lúc đó. |
| `SH05-B05` | `BLOCKER: 401_CAUSE_AND_RECOVERY` | API #04 map invalid/missing JWT/claims và missing profile vào cùng `401 DESIGN_AUTHENTICATION_REQUIRED`; không có reason field để client phân biệt. | Backend/Product chốt hành vi sau khi refresh thành công nhưng API #04 vẫn trả 401, cùng copy/đích cho trường hợp profile thiếu. |
| `SH05-B06` | `BLOCKER: PRODUCTION_UI_COMPOSITION` | `screen.png`/`code.html` là hand-off prototype có preview selector, metadata, diagnostics, raw JSON và policy card; chưa có nguồn xác nhận phần nào dành cho end user. | Product/UX xác nhận UI state cuối, controls được giữ/bỏ và copy trước khi đánh dấu DD READY. |
| `SH05-B07` | `DEPENDENCY: SH02_LOGIN_HANDOFF` | Inventory G-14 giữ discrepancy API #03: catalog `201/UserProfile-only`, current source `200/profile+tokens`; SH-02 chưa thể coi parser/return flow đã xác minh. | SH-02 owner chốt response contract; SH-05 chỉ điều hướng sang màn login đã cấu hình, không tự diễn giải API #03 payload. |

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
