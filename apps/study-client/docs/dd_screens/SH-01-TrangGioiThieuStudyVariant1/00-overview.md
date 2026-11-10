# SH-01 — Trang giới thiệu Study · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `SH-01` |
| Module | Shared / Auth / System |
| Route | `/` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái DD:** DD BLOCKED · IMPLEMENTATION BLOCKED · RUNTIME NOT VERIFIED |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [SH-01.md](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/SH-01.md), [SH-01_PLAN.md](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/SH-01_PLAN.md), [SH-01_markers.json](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/SH-01_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Giới thiệu giá trị học tập, tìm khóa học và CTA đăng nhập/đăng ký.
- In-scope: Có thể nạp một trang khóa học PUBLISHED; không tạo API hero/KPI mới.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-03 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Giới thiệu giá trị học tập, tìm khóa học và CTA đăng nhập/đăng ký. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #05, #06
- Liên kết màn hình dự kiến: [GS-01](../GS-01-DanhSachKhoaHoc/00-overview.md), [SH-02](../SH-02-DangNhap/00-overview.md), [SH-03](../SH-03-DangKyHocVien/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | skeleton/list/empty/network-error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [SH-01 source screen.png](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/screen_annotated.png))
- Luồng: Có thể nạp một trang khóa học PUBLISHED; không tạo API hero/KPI mới.
- Priority: P0; Gate/source status: **R**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# Tài liệu thiết kế chi tiết màn hình — SH-01 Trang giới thiệu Study

> **Trạng thái DD:** DD BLOCKED · IMPLEMENTATION BLOCKED · RUNTIME NOT VERIFIED
> **Mã màn hình:** SH-01 · **Bề mặt:** Trang · **Tác nhân:** Khách
> **Route đề xuất:** / · **AC:** AC-03 · **Độ ưu tiên:** P0
> **Nhãn phía máy chủ trong danh mục:** R cho bằng chứng nguồn API #05/#06; điều này không chứng minh màn hình Study Web đã tồn tại hoặc được triển khai.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: 1. Tổng quan

SH-01 là trang vào công khai của Study. Mục tiêu là giới thiệu dịch vụ học tập, giúp khách tìm kiếm hoặc duyệt khóa học công khai, đồng thời dẫn tới đăng nhập/đăng ký. Danh mục màn hình chuẩn trong [list_screen.md](../../list_screen.md) tham chiếu API danh mục công khai #05 và API khóa học đã xuất bản #06; trang không được tự tạo API nội dung đầu trang/chỉ số KPI hoặc trình bày dữ liệu mẫu như dữ liệu kinh doanh thật.

Tài liệu hệ thống thiết kế được yêu cầu chỉ là tài liệu tham khảo hình ảnh, không phải chuẩn giao diện Study hiện tại. Dùng [.agents/web-study/design.md](../../../../../.agents/web-study/design.md) làm đích giao diện Study Web: token ngữ nghĩa xanh biển, nhịp khoảng cách 4px, vùng nội dung rộng khoảng 1120px, bố cục thích ứng và điều khiển cao tối thiểu 44px. list_screen.md cũng nêu nhịp 4px, chiều rộng nội dung tối đa khoảng 1200px và vùng chạm >=44px. DESIGN.md tham khảo có màu sắc không nhất quán giữa YAML và văn xuôi, đồng thời nút 40px / ô nhập 42px / khung rộng 1440px; không âm thầm dùng nó để ghi đè hướng dẫn Study.

### 1.1 Trạng thái bằng chứng và ghép tài sản

| Bằng chứng | Phát hiện hiện tại | Trạng thái |
|---|---|---|
| Triển khai Study Web | Không có apps/study-client/src; / và các liên kết trong DD chỉ là đề xuất thiết kế | UNWIRED |
| API #05 / #06 | Có route FastAPI, phần triển khai module và mã kiểm thử nguồn | SOURCE_PRESENT; API DD Draft — Needs Confirmation; runtime/deploy chưa xác minh |
| PNG gốc | Có một tài sản hiện tại, 559×1600 | PRESENT |
| HTML tương ứng | Có, nhưng không tương đương ảnh đầy đủ; có liên kết neo giữ chỗ và hai thẻ khóa học mẫu viết cứng | DISCREPANCY |
| Biến thể thứ hai | Worklog cũ và README trước đây từng liệt kê; cây hiện tại không có thư mục/tệp tương ứng | NOT_FOUND |
| DB/schema | API đọc categories, courses và users qua query source; [DDL legacy](../../../../../infra/postgres/study-server/DB.sql) và V1-PILOT là các nguồn riêng, không chứng minh live schema; không có quan hệ course-category trong DDL legacy | NOT LIVE-VERIFIED / G-05 OPEN |
| Ảnh đã chú thích | [Ảnh SH-01 có đánh số](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/screen_annotated.png) | PRESENT |

Giữ nguyên [ảnh gốc](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/screen.png) và [HTML gốc](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/code.html). SHA-256 trước khi chú thích được ghi trong [kế hoạch SH-01](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/SH-01_PLAN.md).

**Sai khác bản mẫu:** ảnh có phần mở đầu và KPI; năm chip danh mục cùng mũi tên; sáu thẻ khóa học; lợi ích, lời chứng thực, logo doanh nghiệp, CTA email và footer nhiều phần. HTML có header login/register, hero/search, bốn danh mục tĩnh, hai thẻ khóa học mẫu và empty state đồng thời; không có các dải lợi ích, lời chứng thực, logo doanh nghiệp hoặc CTA email như trên ảnh. Header search/chuông/avatar trên ảnh cũng không khớp HTML. HTML có 16 liên kết fragment: 5 trỏ tới section ID có thật (`#khoa-hoc`/`#tim-kiem`), 5 `#` quay lên đầu trang, và 6 fragment `#dang-nhap`, `#dang-ky`, `#dieu-khoan` không có target; chúng không chứng minh route Study tồn tại. Không tài sản nào là nguồn chuẩn cho dữ liệu API hay hành vi khi chạy. Không suy luận ảnh và HTML là hai phiên bản của cùng một triển khai.

### 1.2 Vai trò và quyền truy cập

- Khách được truy cập; trang giới thiệu công khai không cần chặn đăng nhập.
- Điều kiện trước: route / phải được Study Web router đăng ký trong implementation; khi được nối, auth không bắt buộc để vào trang. Chỉ vùng dữ liệu cần kết nối mạng.
- Điều kiện sau: SH-01 không tạo/cập nhật dữ liệu máy chủ; chỉ GET danh mục/khóa học. Người dùng có thể ở lại trang, mở GS-01/GS-02, hoặc tới SH-02/SH-03 theo điều kiện ở §2/§5.
- #05 và #06 là API GET công khai. Nếu nhận 401/403 thì đây là kết quả bất thường; hiển thị lỗi an toàn trong khu vực tương ứng, không tự chuyển tới đăng nhập.
- URL trang không chứa token, dữ liệu người dùng riêng tư hoặc email.
- Chỉ nội dung tìm kiếm q được phép chuyển trong query string tới GS-02 theo danh mục; không đưa dữ liệu biểu mẫu khác vào URL.

### 1.3 Đối chiếu các mục A–F trong objective

| Mục yêu cầu | Nội dung tương ứng trong DD |
|---|---|
| **A. Tổng quan màn hình** | §1 mô tả mã/tên/mục tiêu, actor, điều kiện truy cập, asset evidence và trạng thái; §§2–3 mô tả route liên kết, API, dữ liệu; §8 nêu bảo mật/quyền riêng tư; §10 ghi trạng thái triển khai và phụ thuộc còn mở. |
| **B. Luồng hoạt động tổng thể** | §§2 và 5 lần lượt trình bày flow vào/ra và từng bước khởi tạo, tải song song, kiểm tra/ánh xạ response, thao tác, điều hướng, rỗng và lỗi; §6 là chuyển trạng thái. |
| **C. Đặc tả element** | §4 liệt kê 26 nhóm element, điều kiện hiển thị, dữ liệu, trạng thái và event liên quan; tọa độ ảnh nguồn và mapping marker nằm trong [SH-01_PLAN.md](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/SH-01_PLAN.md) và [SH-01_markers.json](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/SH-01_markers.json). |
| **D. Đặc tả sự kiện** | §5 đặc tả 14 event theo trigger/điều kiện, input, xử lý, kết quả hoặc ngoại lệ; request, response, lỗi và nguồn API được truy vết ở §3. |
| **E. Trạng thái và điều hướng** | Liên kết, route đề xuất và dữ liệu chuyển màn hình ở §2; state và chuyển tiếp ở §6; điều kiện truy cập ở §1.2. |
| **F. Tiêu chí nghiệm thu** | Ma trận rà soát dự kiến ở §9; các câu hỏi, owner và điều kiện chặn ở §10. |

Các section cross-reference chỉ giúp tra cứu yêu cầu; chúng không làm các route, nội dung thiết kế hoặc API đang bị chặn thành behavior đã triển khai.
