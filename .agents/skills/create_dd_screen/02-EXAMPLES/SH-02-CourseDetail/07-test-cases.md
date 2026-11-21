# SH-02 — Test Cases

| ID | Type | Preconditions / steps | Expected | References |
|---|---|---|---|---|
| `SH-02-TC-001` | Happy path | Load `/courses/crs-101`; GET 200 valid payload | Title, chapter list, info panel, CTA visible; data đúng | EV-001, API-001, BR-001 |
| `SH-02-TC-002` | Input validation | Load `/courses/` hoặc path param quá 64 chars | Route fallback hoặc not-found, không gọi GET với invalid param | EV-001, BR-005 |
| `SH-02-TC-003` | Anonymous/auth | Anonymous click CTA → login → complete → return detail | Không POST trước login; redirect có returnUrl cùng origin; phải click lại để POST | EV-004/005, BR-002 |
| `SH-02-TC-004` | Enroll success | Member, GET viewer.is_enrolled=false; POST 201 | 1 POST, CTA disabled `Đã đăng ký`, success toast | EV-004, API-002, BR-003 |
| `SH-02-TC-005` | Already enrolled | Member, POST 409 ALREADY_ENROLLED | CTA cập nhật `Đã đăng ký`, không tạo duplicate, không error toast | EV-004, BR-003 |
| `SH-02-TC-006` | Double submit/network | Double click quickly; simulate POST timeout | FE chỉ gọi 1 POST lúc pending; error message; không tự retry POST | EV-004, BR-004 |
| `SH-02-TC-007` | Forbidden/not found | GET 404 private/unpublished ID | Not-found UI, không hiển thị metadata nhạy cảm | EV-001, BR-001/005 |
| `SH-02-TC-008` | Navigation | Click back from SH-02 opened directly | Navigate `/courses`, không phụ thuộc history | EV-002 |
| `SH-02-TC-009` | Accordion | Click chapter 1 twice, then press Enter | Open→close; aria-expanded phản ánh state; không gọi API | EV-003 |
| `SH-02-TC-010` | Retry / stale | GET 503 → Retry → 200; route change trong khi pending | Loading/error/retry đúng; response course cũ không ghi đè | EV-001/006 |

**Extra assertions:** 401/403/422 POST, 5xx/network; null duration; chapters empty; unknown topic enum; sanitization of API text; keyboard focus; responsive width 375px.

**Fixture/source:** Test data và cả API contract là ví dụ minh họa, không gắn với một backend thực tế.
