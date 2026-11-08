# Bắt đầu nhanh

## A. Đọc màn hình mẫu

- Mở `../02-EXAMPLES/SH-01-CourseList/00-overview.md` và xem `images/screen-clean.png`.
- Mở `images/screen-numbered.png`, tra `#1...#7` trong `01-ui-elements.md`.
- Với nút click card, lần theo `SH-01-EL-006 → SH-01-EV-004 → SH-02`.
- Với tìm kiếm, lần theo `SH-01-EV-002 → SH-01-BR-001 → SH-01-API-001 → data-flow → TC`.
- Sang `../02-EXAMPLES/SH-02-CourseDetail/` để xem màn tiếp theo.

## B. Sinh mới một screen

Tại **thư mục gốc `DD-Screen-Kit`**:

```bash
python3 03-TOOLS/create_screen.py \
  --id SH-03 --slug MyCourses --title "Khóa học của tôi" \
  --route "/my-courses" --output ./MY-SCREENS
```

Tạo hai ảnh thật trong `MY-SCREENS/SH-03-MyCourses/images/`:
- `screen-clean.png`: screenshot/thiết kế nguyên trạng;
- `screen-numbered.png`: phiên bản đánh nhãn `#1, #2...` đúng element.

Hoàn tất 8 file và chạy:

```bash
python3 03-TOOLS/validate_dd.py ./MY-SCREENS/SH-03-MyCourses
```

**Lưu ý:** công cụ kiểm tra tính đầy đủ cấu trúc và liên kết tệp, **không** chứng minh nghiệp vụ, API hoặc nội dung DD là đúng. Xem checklist nghiệm thu.
