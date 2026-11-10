# SH-02 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `SH-02-TC-001` | Planning ref / not run | `AC-02` | See source acceptance section | P0 |

## 2. Test planning references

### SH-02-TC-001 — Acceptance planning reference (AC-02)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [SH-02](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/SH-02.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-02`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/SH-02.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: 9. Ma trận kiểm tra và rà soát (dự kiến; chưa chạy)

| Tình huống | Kết quả cần xác minh |
|---|---|
| Email/mật khẩu trống | Kiểm tra cục bộ/trình duyệt chặn #03; không ghi log thông tin đăng nhập |
| Email sai định dạng / dài hơn 255 sau chuẩn hóa | #03 trả 422 và ánh xạ meta.fieldErrors của email |
| Mật khẩu chỉ có khoảng trắng | #03 trả 422; không nhắc lại giá trị |
| Email sai và mật khẩu sai | Cùng trạng thái 401 chung; không thử refresh |
| Thông tin hợp lệ của tài khoản không hoạt động | 403 an toàn khác biệt; không gọi #04 |
| Đăng nhập thành công theo nguồn hiện tại | Ghi nhận shape 200 hồ sơ/token là hành vi nguồn; không âm thầm coi 201 chỉ hồ sơ trong hợp đồng là tương đương |
| Bấm gửi lặp | Chỉ có một yêu cầu #03 khi đang chờ |
| Timeout mạng sau gửi | Không tự gửi lại POST đăng nhập |
| Vai trò học viên thành công | Bộ phiên được duyệt nhận token; #04 dùng Bearer; ánh xạ đúng trường hồ sơ |
| Vai trò người hướng dẫn/quản trị viên | Không gọi API #04 dành cho học viên và không chuyển /student; hiện trạng thái G-02 |
| #04 bỏ permissions/bio | Giao diện không tự tạo dữ liệu |
| #04 trả 401 | Auth/claim lỗi và profile thiếu dùng cùng `DESIGN_AUTHENTICATION_REQUIRED`; không tự refresh nếu chưa có classifier hoặc policy cho phép refresh mọi 401 |
| Liên kết đăng ký | Route SH-03 đề xuất; SH-02 không gọi #01 |
| Nút hiện mật khẩu | Giữ nguyên giá trị; không gửi biểu mẫu; trạng thái được trợ năng hỗ trợ |
| Tính toàn vẹn nguồn | Hash PNG/HTML gốc không đổi; có nguồn gốc bản dựng sạch/ảnh chú thích |

Mã nguồn kiểm thử liên quan gồm test_login_returns_profile_and_tokens_and_commits, test_login_hides_unknown_or_wrong_credentials, test_current_user_returns_safe_profile_and_preserves_trace_id và test_current_user_rejects_non_student_before_database_lookup. Đây là kiểm thử nguồn dùng fixture cục bộ/giả lập, chưa chạy trong phiên tài liệu; chúng không chứng minh xác thực đang triển khai hoặc DB trực tiếp.

**Checklist nghiệm thu tĩnh:**

- [x] 8 marker tuần tự khớp với 8 element IDs trong DD; PNG nguồn và HTML gốc được giữ nguyên.
- [x] Đủ 13 Event ID, mỗi event có trigger, điều kiện, input, quy trình/kết quả và ngoại lệ/khôi phục được nêu.
- [x] API #03/#04 được đối chiếu với catalog/AC và source hiện tại; R-X01 được gắn `SOURCE_BACKED_UNCATALOGUED`.
- [x] Có ma trận state/điều hướng, role guard, validation và nhánh lỗi; mọi policy chưa xác nhận được ghi thành blocker.
- [x] Crosswalk A–F và các liên kết cục bộ đã được rà soát.
- [ ] DD READY: chưa đạt vì contract #03, session/recovery, #04/401 classifier/policy, role bootstrap, route/returnTo và nguồn ảnh còn mở.
- [ ] Runtime verified: chưa xác minh; không chạy test hoặc ứng dụng trong phiên tài liệu.

#### Kế hoạch kiểm chứng từ source PLAN

> CẦN_XÁC_NHẬN: Plan nguồn không có section verification/test được nhận diện.


- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
