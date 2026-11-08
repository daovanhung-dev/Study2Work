# Quy chuẩn DD Screen

## 1. Đặt tên

- Screen: `SH-01`, `SH-02`... duy nhất trong phạm vi dự án.
- Folder: `<SCREEN_ID>-<PascalCaseSlug>`; tên file cố định theo 8-file contract.
- Element: `SH-01-EL-001`; Event: `SH-01-EV-001`; API use: `SH-01-API-001`; Business Rule: `SH-01-BR-001`; Test Case: `SH-01-TC-001`.
- API chuẩn dùng chung dự án có thể có `API-CATALOG-COURSES-LIST`; `SH-01-API-001` chỉ mô tả cách screen này sử dụng contract.
- Ảnh numbered dùng `#1`, `#2` trên chính UI; mapping ở UI Elements giữ `#1 → SH-01-EL-001`.

## 2. Nơi chịu trách nhiệm cho từng loại thông tin

| Loại | Nguồn duy nhất trong screen | Các file khác |
|---|---|---|
| Mục tiêu, actor, scope | overview | tham chiếu |
| Thuộc tính UI, visibility | ui-elements | tham chiếu EL ID |
| Thứ tự xử lý khi sự kiện xảy ra | events | tham chiếu EV ID |
| State, mapping, cache | data-flow | tham chiếu field/state |
| Request/response/auth/status | api-integration | tham chiếu API ID |
| Điều kiện nghiệp vụ | business-rules | tham chiếu BR ID |
| Entry/exit/route/back | navigation | tham chiếu destination |
| Expected behavior trong kiểm thử | test-cases | tham chiếu EV/BR/API |

## 3. Quy tắc chất lượng

- Mô tả có thể thực thi và kiểm thử được: tránh 'xử lý phù hợp', 'thông báo đẹp'. Nêu cụ thể điều kiện, kết quả và fallback.
- Ghi nguồn giá trị: người dùng nhập, route, API, local storage, tính toán client hoặc server.
- Quy tắc bảo mật và quyền truy cập phải do server xác thực, không tin client-only guard.
- Với network calls: chỉ ra loading, error, retry, empty, cancellation/race, stale state, timeout nếu thích hợp.
- Phân biệt giá trị **mẫu/mock** với **contract đã xác nhận**. Ví dụ SH-01/SH-02 trong kit đều là giả định.
- Link giữa các file bằng đường dẫn Markdown tương đối, không dựa vào vị trí workspace cụ thể.
- Tránh lưu token, password, dữ liệu người dùng thật trong DD/screenshot.

## 4. Mức độ xác nhận

| Status | Ý nghĩa |
|---|---|
| Draft | Chưa kiểm chứng đầy đủ; được phép có CẦN_XÁC_NHẬN |
| Review | Đã có nguồn và đầy đủ nội dung, đang rà soát |
| Approved | Đã xác minh các quyết định quan trọng, được phép triển khai |
| Deprecated | Không còn sử dụng |

## 5. Chất lượng sự kiện (Event Contract)

Mỗi sự kiện cần: (A) trigger/owner; (B) precondition/guard; (C) inputs và source; (D) validation/normalization; (E) xử lý theo thứ tự; (F) API + dữ liệu request; (G) mapping/side effects; (H) state/UI output; (I) error/edge cases; (J) navigation và tests.

## 6. Quy tắc cross-screen

- Mỗi destination phải định danh screen hoặc external route có chủ sở hữu xác định.
- Tham số route có type, validation và phương án khi sai/thiếu.
- Chỉ mô tả back-stack phù hợp router/project, không mặc định `history.back()` luôn hợp lệ.
