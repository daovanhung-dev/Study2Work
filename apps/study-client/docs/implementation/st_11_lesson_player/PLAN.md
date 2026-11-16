# PLAN: Layout tĩnh ST-11 Lesson Player

## Trạng thái và phê duyệt

- SPEC liên kết: `SPEC.md`, revision 1, người dùng đã duyệt ngày 2026-11-15, SHA-256 `C5038EB66D7A7BF572DC6DE6C204BEC89FE27395FBC6485759FF0B282BB097BB`.
- PLAN revision: 1.
- Phê duyệt: `PENDING`.

## Các bước triển khai

| Bước | SPEC ID | File | Thay đổi và kết quả mong đợi |
|---|---|---|---|
| P1 | R3 | `apps/study-client/src/app/app.routes.ts`; `apps/study-client/src/app/features/student/student.route.ts` | Đăng ký route preview `/student/lessons/:lessonId` qua Student route group lazy-load. Không đọc, kiểm tra hay dùng tham số để tải dữ liệu. |
| P2 | R1, R4 | `apps/study-client/src/app/layouts/student/student-layout.ts`; `student-layout.html`; `student-layout.css` | Tạo shell Student có header và footer theo ảnh, bọc `RouterOutlet`; giữ nguyên đích liên kết trong tài liệu tham chiếu ST-11. |
| P3 | R1, R2, R4 | `apps/study-client/src/app/features/student/ST11/pages/st11-page.ts`; `st11-page.html`; `st11-page.css` | Hiển thị breadcrumb và thẻ fallback căn giữa, đúng nội dung nguồn, icon play SVG cục bộ; bố cục responsive và liên kết có focus nhìn thấy được. Không có API, nút điều khiển player hoặc dữ liệu động. |
| P4 | R1-R4 | `apps/study-client/docs/implementation/st_11_lesson_player/PLAN.md`; worklog task | Ghi bằng chứng triển khai và xác minh theo SPEC ID. Không sửa DD hoặc ảnh. |

## Phụ thuộc và luồng source

```text
app.routes.ts -> student.route.ts -> StudentLayout -> ST11Page -> HTML/SVG tĩnh
Không có data-access, model, HTTP caller, API, DB hay side effect bên ngoài.
```

Feature folder giữ đủ bốn thư mục con trực tiếp theo quy ước: `data-access/`, `models/`, `pages/`, `ui/`. Chỉ tạo file trong `pages/`, vì màn đã duyệt không có hành vi API/model hoặc component con riêng cần triển khai. Không đổi registry `StudyIcon`; glyph play trang trí được viết SVG nội bộ trong template ST11.

## Xác minh và ma trận test case

Task này không thêm hoặc chạy automated test. Route spec hiện có chứa chỉnh sửa từ trước của người dùng và sẽ được giữ nguyên. Chỉ chạy build và xem preview thủ công; các bước này không xác nhận auth Student hay hành vi các đích liên kết.

| TC | SPEC / bước | Chuẩn bị và thao tác | Kết quả mong đợi | Lớp / bằng chứng | Trạng thái |
|---|---|---|---|---|---|
| TC-001 | R1, R2 / P1-P3 | Chạy Study Web và mở `/student/lessons/demo`. | Fallback ST-11 hiển thị; không tải bài học hoặc có điều khiển player. | Xem route thủ công trên browser cục bộ. | `NOT_RUN` |
| TC-002 | R1, R4 / P2-P3 | Xem ở kích thước desktop và viewport hẹp; dùng Tab qua các liên kết. | Thứ bậc bố cục khớp ảnh, thích ứng viewport hẹp, focus vẫn nhìn thấy. | Kiểm tra hình ảnh/keyboard thủ công. | `NOT_RUN` |
| TC-003 | R2, R4 / P2-P3 | Đối chiếu nội dung và href render với DD `04_UI_Spec.md` và `code.html`. | Copy tĩnh và cả bảy đích khớp nguồn; không khẳng định các trang đích đã hoạt động. | Kiểm tra source/DOM thủ công. | `NOT_RUN` |
| TC-004 | R1-R4 / P1-P3 | Chạy `npm.cmd run build` trong `apps/study-client`. | Angular production build hoàn tất không lỗi. | Kết quả build. | `NOT_RUN` |

## Tương thích, rủi ro và hoàn tác

- Route mới được thêm độc lập; không đổi `/`, `/admin` hay `/admin/users`.
- Giữ nguyên route spec đã chỉnh và toàn bộ thay đổi không liên quan trong worktree.
- Student destination và auth chưa có; truy cập trực tiếp preview không đồng nghĩa có kiểm soát quyền.
- Nếu build hoặc xem ảnh phát hiện lỗi, chỉ sửa các file ST-11 đã liệt kê và chạy lại bước xác minh liên quan.
- Hoàn tác bằng cách bỏ Student route/layout/page mới và chỉ hoàn tác phần đăng ký route trong `app.routes.ts`.

## Phần chưa xác minh

- Không có kết quả automated test cho task này.
- Đích liên kết lúc chạy, auth, Student navigation và hành vi Lesson Player chức năng vẫn `UNWIRED`/chưa xác minh.
- Font/icon dùng system/local thay cho Plus Jakarta Sans/Material Symbols từ xa, nên glyph có thể hơi khác ảnh nguồn.
