# Báo cáo đối chiếu bộ UTC minh họa GS-01 với DD được cung cấp

**Nguồn:** `vi-du/GS-01/DD_goc/GS-01-DanhSachKhoaHoc/`, sao chép từ gói người dùng cung cấp `GS-01-DanhSachKhoaHoc.tar.gz`.

## Thống kê

- Mã màn hình: `GS-01` — Danh sách khóa học, tuyến `/courses`.
- Thành phần gắn ảnh: **16** (`GS-01-EL-001` → `GS-01-EL-016`) trong `01-ui-elements.md`.
- Sự kiện được mô tả: **11** (`GS-01-EV-001` → `GS-01-EV-011`) trong `02-events.md`.
- API: **2**, alias `GS-01-API-001` → API catalog **#05** (`/api/v1/categories`), `GS-01-API-002` → **#06** (`/api/v1/courses`).
- Yêu cầu để truy vết: **23 mã nội bộ** được suy ra từ DD (không phải mã yêu cầu chính thức do dự án phát hành).
- UTC đề xuất: **18** ca toàn màn hình + **28** ca thành phần + **27** ca sự kiện = **73 ca**.
- Kiểm tra tham chiếu: **23/23 yêu cầu có ca**, **16/16 thành phần có ca**, **11/11 sự kiện có ca**. Đây là **độ bao phủ danh mục** chứ không chứng nhận toàn bộ nhánh DD đã được duyệt.

## Các điều kiện hạn chế quan trọng

`00-overview.md` và `05-business-rules.md` ghi rõ thiết kế trạng thái đã tải (card/sort/paging/count), category filter và search handoff chưa được phê duyệt. `07-test-cases.md` nêu rõ các mã cũ là *planning references*, chưa chạy. Ghi chú rà soát source ngày **21/11/2026** xác nhận có route/caller và xử lý bất đồng bộ trong code nhưng **không xác nhận browser/runtime đã được kiểm thử**.

Bởi vậy `utc-gs01.json` có những ca `Đã xác nhận` về luồng/API nguồn và những ca `Chờ xác nhận` về thiết kế chưa chốt; file Excel mẫu **không có ca nào Đạt/Không đạt**. Danh sách 8 blocker nằm tại `02. Tổng quan` và trong JSON.

## Phân loại chấp thuận

- **Chất lượng cấu trúc:** đạt theo bộ validator của skill.
- **Phát hành bộ UTC để rà soát:** có thể dùng làm **kế hoạch kiểm thử dự kiến**.
- **Phê duyệt UTC để thực thi nghiệm thu:** **chưa đạt**, do DD BLOCKED và runtime chưa xác minh.
- **Thực thi test hoặc kiểm tra phần mềm thật:** không thực hiện trong gói minh họa này.
