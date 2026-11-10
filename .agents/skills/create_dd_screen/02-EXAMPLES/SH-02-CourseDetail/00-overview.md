# SH-02 — Chi tiết khóa học · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `SH-02` |
| Module | Study / Course Catalog |
| Route | `/courses/:courseId` |
| Actor | Khách và người dùng đăng nhập |
| DD status | **Approved (chỉ trong bộ ví dụ giả lập)** |
| Owner | Bộ minh họa DD Screen Kit |
| Version | Demo 1.0 — 2026-11-08 |
| Nguồn | UI mock `images/*`, API/flows giả định, **chưa xác minh repo Study2Work** |

## 1. Mục tiêu / phạm vi
Hiển thị chi tiết khóa học đã chọn từ `SH-01`; cho phép xem mô tả, nội dung chương và đăng ký tham gia nếu đủ điều kiện.

**In-scope:** load chi tiết, xem danh sách chương, mở/đóng chương, đăng ký, xử lý anonymous/đã đăng ký/lỗi. **Out-of-scope:** phát bài học, thanh toán, phê duyệt quản trị.

## 2. Use cases
| UC | Actor | Kết quả |
|---|---|---|
| UC-01 | Bất kỳ | Xem thông tin khóa học published |
| UC-02 | Khách | Nhấn đăng ký → chuyển đăng nhập, mang returnUrl |
| UC-03 | Member | Đăng ký thành công, button đổi `Đã đăng ký` |
| UC-04 | Member đã enroll | Không tạo đăng ký trùng |

## 3. Preconditions / dependencies
- Route có `courseId` non-empty; nguồn `SH-01-EV-004` hoặc deep link trực tiếp.
- `SH-02-API-001`: GET course detail public, `SH-02-API-002`: POST enrollment có auth.
- Destination login **giả lập** `/login?returnUrl=...` nằm ngoài 2-screen demo; tên route thật phải được đối chiếu khi áp dụng.

## 4. UI States
| State | Điều kiện | UI |
|---|---|---|
| Loading | Loading detail | Skeleton title/content; disable CTA |
| Ready | 200, published | Title, tag, chapters, CTA theo auth/enrolled |
| Empty/404 | ID không tồn tại hoặc không public | `Không tìm thấy khóa học` + về danh sách |
| Error | Network/API 5xx | Banner Retry giữ courseId |
| Enrolling | POST đang chạy | CTA spinner/disabled |
| Enrolled | POST success hoặc 409-already-enrolled | CTA `Đã đăng ký` disabled, success toast khi mới đăng ký |

## 5. Luồng tổng quan
`SH-01 click card → SH-02 mount → GET detail → user expand lesson → click enroll → (anonymous: login) hoặc (member: POST enrollment) → update CTA`.

[Ảnh sạch](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)

## 6. Changelog
- 2026-11-08 — Bộ màn hình minh họa hoàn chỉnh; contract và flows giả lập.
