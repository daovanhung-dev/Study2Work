# ST-08 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-08_markers.json](../../screen_stitch/03_student/ST-08_khoa-hoc-cua-toi/ST-08_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-08-EL-001` | `ST08-EL-01` | Study2Work text link to /student |
| #2 | `ST-08-EL-002` | `ST08-EL-02` | Tổng quan, Khóa học của tôi (active), Tiến độ |
| #3 | `ST-08-EL-003` | `ST08-EL-03` | Khóa học của tôi heading |
| #4 | `ST-08-EL-004` | `ST08-EL-04` | White empty-state surface with local_library icon |
| #5 | `ST-08-EL-005` | `ST08-EL-05` | Chưa có khóa học để hiển thị. |
| #6 | `ST-08-EL-006` | `ST08-EL-06` | No enrolled course or data not updated copy |
| #7 | `ST-08-EL-007` | `ST08-EL-07` | Xem tiến độ học tập link to /student/progress |
| #8 | `ST-08-EL-008` | `ST08-EL-08` | Static Study2Work wordmark in footer |
| #9 | `ST-08-EL-009` | `ST08-EL-09` | Tổng quan, Khóa học của tôi, Tiến độ links |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Element chi tiết

Các số dưới đây khớp với `screen_annotated.png` và `ST-08_markers.json`. Giá trị nhìn thấy đều đến từ HTML viết tĩnh, không phải API.

| # / Element ID | Tên, loại, vị trí | Thuộc tính, dữ liệu và điều kiện | Trạng thái / sự kiện |
|---|---|---|---|
| **#1 — ST08-EL-01** | Brand link “Study2Work”, anchor ở đầu header. | `href="/student"`; nhãn tĩnh. Không có field nhập hoặc validation. Hiển thị trong ảnh 1280×1024. | HTML không khai báo state động; anchor mặc định có thể focus bằng keyboard của trình duyệt, nhưng focus style/app routing chưa verify. `ST08-EV-05`. |
| **#2 — ST08-EL-02** | Nhóm primary navigation trong header: “Tổng quan”, “Khóa học của tôi” (active), “Tiến độ”. | Các href lần lượt `/student`, `/student/courses`, `/student/progress`; active style được gán tĩnh cho “Khóa học của tôi”. Không có permission rule hoặc route registry trong app source. | Bản HTML tĩnh có utility hover cho các link chưa active; không có trạng thái loading/error. `ST08-EV-05`. |
| **#3 — ST08-EL-03** | Page title `h1` “Khóa học của tôi”, đầu vùng nội dung. | Văn bản cố định trong HTML; không lấy từ API, không có giới hạn dữ liệu. | Static/default only; không có event. |
| **#4 — ST08-EL-04** | Empty-state card và icon `local_library`, giữa vùng nội dung. | Surface trắng có nền viền/shadow; icon là Material Symbol. Không có identifier, count hoặc binding dữ liệu. Chỉ là trạng thái minh họa. | Không chứng minh rằng enrollment collection rỗng; không có click handler. |
| **#5 — ST08-EL-05** | Empty-state heading `h2`: “Chưa có khóa học để hiển thị.” | Copy cố định; không có source field/API mapping. | Chỉ xuất hiện trong HTML tĩnh; không có event. |
| **#6 — ST08-EL-06** | Empty-state explanatory copy. | Copy cố định: “Bạn chưa có khóa học nào trong danh sách hoặc dữ liệu chưa được cập nhật.” Hai nguyên nhân được gộp trong copy, nhưng API chưa phân biệt empty với stale/missing data. | Static/default only. Không được dùng để suy ra nguyên nhân thực tế. |
| **#7 — ST08-EL-07** | CTA anchor “Xem tiến độ học tập” với icon `trending_up`. | `href="/student/progress"`; label và icon cố định; nút cao 48px trong HTML. Không truyền course ID hoặc query. | HTML có hover utility; route/runtime/auth guard chưa verify. `ST08-EV-04`. |
| **#8 — ST08-EL-08** | Footer brand “Study2Work”, text/span. | Chữ tĩnh, không phải anchor trong HTML. Không có destination. | Không có event. |
| **#9 — ST08-EL-09** | Nhóm footer navigation: “Tổng quan”, “Khóa học của tôi”, “Tiến độ”. | Href `/student`, `/student/courses`, `/student/progress`. Nội dung và route lặp lại header; không có active state được khai báo ở footer. | HTML có hover utility; runtime routes chưa verify. `ST08-EV-06`. |

### Phần inventory chưa có element trong asset

Status filter/select, course card/list, progress bar, pagination, partial-progress indicator và error/loading display được kỳ vọng hoặc suy ra từ state inventory nhưng không xuất hiện trong source PNG/HTML. Vì không có vị trí, nhãn, field, default, option set hay disabled behavior được duyệt, các phần này không được gán marker/EL ID và không thể coi là UI đã thiết kế. Sự kiện dự kiến tương ứng được ghi ở §4 dưới dạng blocker, không giả lập một control.

### Responsive, accessibility và design system

HTML imports Google Fonts and Tailwind CDN, uses Plus Jakarta Sans and `max-w-[1440px]`; its active nav uses the configured cobalt `#004AC6` while its CTA uses `#0B5F8A`, and the header uses a translucent backdrop blur. Study Web guide instead targets Inter/system typography, no remote font/package import, ocean primary `#0B5F8A`, avoids glass effects and sets a content width up to about 1120px. This is a `DESIGN DISCREPANCY`; no exception is approved. The file also has responsive Tailwind classes and a 48px CTA, but there is no narrow-width capture or app runtime to verify reflow. Confirm focus-visible, contrast, keyboard order, current-page semantics, and wrapping at narrow viewports against the guide when Study Web exists.

## 4. Conditional UI & state variations
- States theo inventory: loading/empty/partial-progress/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-08_khoa-hoc-cua-toi/ST-08.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
