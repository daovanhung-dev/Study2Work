# SH-01 — Danh sách khóa học · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `SH-01` |
| Module | Study / Course Catalog |
| Route | `/courses` |
| Actor | Khách và người dùng đăng nhập |
| DD status | **Approved (chỉ trong bộ ví dụ giả lập)** |
| Owner | Bộ minh họa DD Screen Kit |
| Version | Demo 1.0 — 2026-11-08 |
| Nguồn | UI mock `images/*`, hợp đồng API và quy tắc **giả định** trong bộ demo; **chưa đối chiếu Study2Work thật** |

## 1. Mục tiêu / phạm vi
Hiển thị khóa học đang công khai; người dùng tìm kiếm theo tiêu đề, lọc theo chủ đề, chuyển trang và mở màn chi tiết `SH-02`.

**Trong phạm vi:** tải danh sách, tìm kiếm, lọc, phân trang, các trạng thái loading/empty/error, điều hướng chi tiết. **Ngoài phạm vi:** đăng ký khóa học, quản trị khóa học, chức năng thanh toán.

## 2. Use cases
| UC | Actor | Kết quả |
|---|---|---|
| UC-01 | Khách/Member | Xem danh sách khóa học đang công khai |
| UC-02 | Khách/Member | Tìm và lọc khóa học |
| UC-03 | Khách/Member | Xem chi tiết một khóa học ở SH-02 |

## 3. Entry và dependencies
- Vào trực tiếp `/courses` hoặc bấm menu `Khóa học` tại `SH-01-EL-001`.
- Public read, không cần access token (giả định ở demo này).
- `SH-01-API-001`: danh sách khóa học; `SH-02`: chi tiết khóa học.

## 4. Trạng thái screen
| State | Điều kiện | UI |
|---|---|---|
| Initial / Loading | Vừa mount hoặc query thay đổi và đang chờ API | Header và bộ lọc vẫn hiển thị; vùng card skeleton; vô hiệu hóa chuyển trang |
| Success | API trả 1+ khóa học | Card, tổng số kết quả, phân trang |
| Empty | API 200, `items=[]` | `Không có khóa học phù hợp`; action Đặt lại bộ lọc |
| Error | Timeout, offline hoặc API 5xx | Banner `Không tải được danh sách`; nút Thử lại, giữ input lọc |

## 5. Assets, hành vi tổng quát
- [Ảnh sạch](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Init → GET courses → cards → người dùng nhập từ khóa/chọn chủ đề/chuyển trang → GET mới → click card → SH-02.
- Liên quan: [UI](01-ui-elements.md), [Events](02-events.md), [Data](03-data-flow.md), [API](04-api-integration.md), [Navigation](06-navigation.md).

## 6. Change log
- 2026-11-08 — Tạo bộ mẫu demo hoàn chỉnh với dữ liệu mô phỏng. Không sử dụng như contract sản phẩm thực tế.
