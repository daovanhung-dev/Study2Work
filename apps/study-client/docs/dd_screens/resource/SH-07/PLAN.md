# PLAN — SH-07 Theo dõi tác vụ bất đồng bộ

## 1. Phạm vi và nguồn

| Thuộc tính | Giá trị |
|---|---|
| Screen | SH-07 — Theo dõi tác vụ bất đồng bộ |
| Loại / route mục tiêu | Panel / `/operations/:operationId` |
| Vai trò | Student, Mentor hoặc Admin chỉ theo quyền sở hữu được backend xác nhận; Admin bypass chưa được chốt |
| AC / API | AC-12, AC-25, AC-36, AC-38 / API #18 |
| Screen liên kết | ST-07, ME-15, AD-21, AD-25; các luồng nguồn ST-06, ME-14, AD-20, AD-24 |
| Trạng thái tài liệu | DESIGN TARGET; API #18 Draft, chưa wire vào runtime |
| Nguồn thiết kế | `.agents/web-study/design.md`; `apps/study-client/docs/dd_screens/list_screen.md` |

Thiết kế một panel dùng chung để theo dõi tác vụ do Student, Mentor hoặc Admin khởi tạo. Mỗi trạng thái dưới đây là biến thể minh họa theo inventory, không phải bằng chứng rằng backend hiện đã trả enum đó. Không có screen con được khai báo cho SH-07; loading, lỗi và trạng thái job là biến thể của cùng panel.

## 2. Ranh giới dữ liệu và hành vi

| Hạng mục | Kế hoạch | Điều kiện / discrepancy |
|---|---|---|
| Khởi tạo yêu cầu | Chỉ gọi `GET /api/v1/operations/{operation_id}` khi ID đã được backend trả về và được luồng gọi xác nhận. | Không tự tạo, cast, đoán định dạng hoặc lấy ID từ `notification_id` / `order_id`. API #18 đang mâu thuẫn UUID với int64. |
| Dữ liệu được phép trình bày | `status`, `submitted_at`, `updated_at`, `completed_at` nếu có. | Đây là logical fields trong Draft #18; mapping/storage thực chưa được xác nhận. Không thêm % tiến độ, ETA, số người nhận hoặc mô tả loại job khi chưa có nguồn. |
| Polling | Trạng thái `queued`/`running` có nút **Làm mới trạng thái** để gọi lại GET. Poll nền chỉ được bật sau khi BE chốt chu kỳ, giới hạn và terminal enum; khi được duyệt chỉ tiếp tục ở non-terminal và dừng ở terminal. | Không hiển thị bộ đếm hoặc tần suất giả. Dừng yêu cầu khi rời panel, mất phiên hoặc request bị hủy. |
| Trạng thái thành công | Hiển thị “Đã hoàn tất”; chỉ nói tác vụ thành công ở mức generic. | Không khẳng định đã thanh toán, đã ghi danh, thông báo đã gửi hoặc export đã sẵn sàng nếu response theo kind chưa xác nhận. |
| Trạng thái lỗi | Hiển thị copy an toàn; GET có thể được thử lại bằng hành động người dùng. | Không tự retry POST, không tạo job mới, không hiển thị raw backend message. |
| Quyền truy cập | Chỉ render dữ liệu sau khi backend xác nhận quyền sở hữu; 403 và 404 dùng cùng cách diễn đạt không tiết lộ resource. | Không suy ra Admin được bypass owner check; không dùng client role làm bằng chứng sở hữu. |
| Thanh toán | Callback của gateway không chứng minh đã thanh toán; ST-07 chỉ được tiếp tục sau xác nhận payment/entitlement phía server. | Không điều hướng sang trạng thái enrolled từ SH-07. |
| Thông báo | Giữ riêng `operation_id` và `notification_id`. | API #64 đang nhận notification int64 và dựng projection QUEUED/FAILED/SENT; không đổi `SENT` thành `succeeded` khi chưa có quy tắc thống nhất. API #93 trả Notification ở `data` và UUID operation ở `meta`. |
| Export | Nút tải chỉ xuất hiện khi API trả URL tải hợp lệ. | Contract kết quả export chưa chốt; bản thiết kế generic không có nút tải hoạt động. |

## 3. Kế hoạch giao diện

### Art direction

- Phong cách: giao diện sản phẩm học tập chỉn chu, bình tĩnh, có độ tương phản và khoảng trắng rõ; tạo cảm giác hoàn thiện bằng bố cục, nét vẽ SVG đồng nhất và typography thay vì trang trí dày.
- Giữ light-first và palette Study ocean. Nền `#F6FAFC`, surface trắng, heading `#073B57`, body `#17324D`, muted `#536A7A`, viền `#D4E2E9`, primary `#0B5F8A`, hover `#084968`, soft `#E8F4FA`; status success/warning/danger lần lượt `#18794E`, `#8A4B08`, `#B42318` và luôn đi cùng chữ/biểu tượng.
- Font: Inter nếu có sẵn, nếu không dùng system sans-serif; không tải font ngoài. Không dùng emoji, logo giả, ảnh stock, glass, neon hoặc nền gradient lớn.
- Tạo một minh họa SVG trạng thái độc quyền: tấm thẻ tác vụ tối giản nằm trong các vòng cung/đường quỹ đạo nét mảnh. Chỉ glyph trung tâm, tint nhỏ và chip trạng thái đổi theo biến thể; minh họa không biểu diễn % hoặc các bước nghiệp vụ không được xác nhận.
- Dùng icon vector cùng nét 1.75–2px. Radius card 16px, control 10–12px, nhịp khoảng cách 4/8px. Bóng rất nhẹ hoặc chỉ viền.

### Bố cục desktop — 1440 × 960

1. Nền toàn trang `page-background`; khung nội dung tối đa 1120px, căn giữa.
2. Header mảnh, cao khoảng 68px: wordmark chữ “Study” ở trái; nút quay lại có icon mũi tên và nhãn dễ hiểu. Không thêm nav hoặc CTA ngoài luồng.
3. Eyebrow “Theo dõi tác vụ” đặt trên panel, cỡ 13px/600, màu muted.
4. Panel trắng rộng khoảng 920px, chia hai vùng cân bằng: vùng nội dung bên trái khoảng 56%; vùng minh họa trạng thái bên phải khoảng 44%, nền ocean-soft rất nhạt và có ranh giới tinh tế. Card có 16px radius, viền 1px, đổ bóng thấp.
5. Vùng nội dung gồm chip trạng thái, heading lớn 32–36px, mô tả tối đa 2 dòng, đường phân cách, hai metadata hàng/cột (yêu cầu gửi, cập nhật gần nhất), nút primary **Làm mới trạng thái** và ghi chú nhỏ “Trạng thái được cung cấp bởi hệ thống”. `completed_at` chỉ thêm thành hàng thứ ba khi có giá trị.
6. Minh họa dùng hình học SVG tĩnh theo status; không làm animation loop. Bên dưới panel không đặt quảng bá, thống kê hoặc nội dung không thuộc tác vụ.

### Bố cục tablet/mobile

| Viewport | Quy tắc |
|---|---|
| Tablet 768–1023px | Panel tối đa theo gutter 24px; giảm khoảng trống hai cột; minh họa giữ đủ tương phản và không ép cột metadata. |
| Mobile 390px | Gutter 16px; header một hàng; panel xếp dọc, minh họa 112–128px phía trên nội dung, heading 26–28px; metadata thành các hàng nhãn/giá trị; nút cao 48px full-width. |
| Minimum 320px | Không tràn ngang; cho phép giá trị thời gian xuống dòng; nút/icon không bị thu nhỏ dưới target 44px. |

## 4. State matrix cần thiết kế

Các copy dưới đây là copy mục tiêu. Năm job status được vẽ là `DESIGN_ONLY` theo list screen; trước khi kết nối phải thống nhất enum và mapping với BE.

| State key | Chip / heading | Minh họa / màu | Mô tả / hành động |
|---|---|---|---|
| `queued` | “Đang chờ” / “Đang chờ xử lý” | Clock glyph, ocean-primary/ocean-soft | “Yêu cầu đang chờ hệ thống xử lý.” Có Làm mới trạng thái. |
| `running` | “Đang xử lý” / “Tác vụ đang được xử lý” | Activity glyph nét tĩnh, ocean-primary/ocean-soft | “Trạng thái sẽ thay đổi khi hệ thống cập nhật.” Không hiển thị phần trăm hoặc ETA. Có Làm mới trạng thái. |
| `succeeded` | “Hoàn tất” / “Tác vụ đã hoàn tất” | Check glyph, success với nhãn chữ | “Tác vụ đã kết thúc thành công.” Không diễn giải payment/enrollment/notification/export. Có thể bỏ nút refresh sau khi terminal được xác nhận. |
| `failed` | “Không thành công” / “Tác vụ chưa thể hoàn tất” | Alert glyph, danger với nhãn chữ | Mô tả trung tính; không thêm retry job hoặc raw error. Chỉ GET lại nếu contract cho phép refresh status. |
| `expired` | “Đã hết hạn” / “Tác vụ đã hết hạn” | Hourglass glyph, warning với nhãn chữ | Copy không cam kết khôi phục/gia hạn. Không tạo job mới. |
| `loading` | Skeleton không nhấp nháy / “Đang tải trạng thái” | Skeletonĩnh | Giữ kích thước ổn định; không tạo layout shift. Tôn trọng reduced motion. |
| `access_hidden` | “Không thể mở tác vụ này” | Lock/route glyph trung tính | Dùng chung nội dung cho 403/404 để không lộ sự tồn tại/owner. Không có nút tiết lộ ID. |
| `fetch_error` | “Chưa tải được trạng thái” | Cloud-off glyph, danger/warning kèm chữ | Nêu lỗi kết nối chung; nút **Thử lại** chỉ gọi lại GET với cùng ID đã xác nhận. |
| `session_expired` | “Phiên đăng nhập đã hết hạn” | Account glyph | Chạy shared session recovery; chỉ đưa tới SH-02 khi luồng auth xác nhận cần đăng nhập lại. |

Ngày/giờ trong ảnh là fixture để trình bày typography, được ghi rõ là dữ liệu minh họa trong `SCREEN.md`; không dùng chúng làm bằng chứng runtime. Không render operation ID trong ảnh vì kiểu ID đang mâu thuẫn và không cần thiết cho mục tiêu theo dõi.

## 5. Element numbering cho annotated view

Ảnh annotated có marker tròn số `#1…#20` đặt sát element, không che chữ hoặc control. Ảnh clean không chứa marker. Các marker dùng cùng ID ở mọi status để đối chiếu được một lần trong `SCREEN.md`.

| # | Element |
|---:|---|
| 1 | Wordmark chữ Study |
| 2 | Nút Quay lại |
| 3 | Icon mũi tên của nút Quay lại |
| 4 | Eyebrow Theo dõi tác vụ |
| 5 | Nền/surface panel |
| 6 | Minh họa trạng thái SVG |
| 7 | Glyph trung tâm minh họa |
| 8 | Chip trạng thái |
| 9 | Icon trạng thái trong chip |
| 10 | Nhãn trạng thái trong chip |
| 11 | Heading trạng thái |
| 12 | Mô tả trạng thái |
| 13 | Đường phân cách |
| 14 | Nhãn thời điểm gửi |
| 15 | Giá trị `submitted_at` |
| 16 | Nhãn cập nhật gần nhất |
| 17 | Giá trị `updated_at` |
| 18 | Nút Làm mới trạng thái / Thử lại |
| 19 | Icon refresh trong nút |
| 20 | Ghi chú nguồn trạng thái |

`completed_at` khi response có giá trị là metadata tùy chọn: bổ sung thành marker #21 (nhãn) và #22 (giá trị), chỉ trong biến thể terminal tương ứng. Các thành phần thuần trang trí được đánh dấu là decorative, không tạo marker riêng nếu chúng không có meaning/interaction độc lập.

## 6. Tương tác và accessibility

| Element | Event / state |
|---|---|
| Quay lại | Click/Enter/Space gọi history back nếu có history nội bộ an toàn; nếu không có, ẩn nút để không dẫn tới route tự đoán. Hover đổi nền nhẹ; focus-visible ring ocean-primary; pressed đổi ocean-hover. |
| Làm mới trạng thái | Click/Enter/Space gọi GET #18 bằng ID đã được xác nhận; disable trong lúc request; label thành “Đang làm mới…”; success cập nhật status/time; 401/403/404/500/network đi theo state matrix; không gửi mutation. |
| Thử lại | Chỉ gọi lại GET #18, không gọi producer POST. Disable trong lúc chờ; có focus/pressed/loading state giống primary action. |
| Auto-poll (future gated) | Chỉ bật khi BE chốt interval/rate/visibility policy; queued/running tiếp tục, terminal dừng; hủy request khi unmount/hidden/offline; không tạo timer loop theo số giả. |
| Trạng thái | Không dựa vào màu đơn lẻ: luôn có text, icon và accessible name; announce thay đổi status bằng polite live region. |
| Keyboard | DOM/focus order: quay lại → heading/status → metadata → primary action. Icon trang trí `aria-hidden`; button có visible label; focus không bị clip bởi card. |
| Motion | Hover/focus/pressed 140ms; state transition 200ms; enter tối đa 280ms/4px. Không spinner loop bắt buộc; skeleton tĩnh hoặc shimmer chỉ khi reduced motion cho phép. |

Contrast mục tiêu WCAG AA, text body >=16px khi có thể. Target control >=44px. Tất cả state designs light theme; dark mode ngoài phạm vi guide hiện hành.

## 7. Đầu ra trong folder SH-07

- `PLAN.md` — kế hoạch này, phải tồn tại trước khi yêu cầu tạo ảnh.
- `SCREEN.md` — mô tả source trace, state/flow, token, responsive, element table, size/font/action/hover/focus/error và open discrepancies.
- `source/` — HTML/CSS/inline SVG hoặc source vector do ChatGPT tạo để ảnh có thể render lại; không dùng remote font/dependency.
- `images/` — clean và annotated PNG cho 5 status states ở desktop; clean/annotated responsive `running` ở mobile; tablet `running`; bổ sung preview error/loading nếu thời lượng tạo cho phép, không gộp các trạng thái lỗi thành job status.
- `SH-07-design.zip` — gói toàn bộ PLAN, SCREEN, source và ảnh; mở thử archive và so danh sách file trước khi kết luận.

Không tạo folder screen con vì inventory không khai báo child screen. Tên file dùng status và viewport; `SCREEN.md` định nghĩa rõ khi state là design-only. Sau khi ChatGPT tạo file, kiểm tra kích thước, text, marker collisions/cutoff, crop/contrast/responsive bằng ảnh đã render; ghi lỗi và yêu cầu ChatGPT sửa đến khi toàn bộ kiểm tra đạt. Nếu ChatGPT không tạo ZIP hoặc screenshot dùng được, tiếp tục dùng source/code do ChatGPT cung cấp để dựng package cục bộ và ghi rõ nguồn.

## 8. Tiêu chí review / chấp nhận

- Đúng Study ocean light system, premium nhưng tiết chế; hierarchy/status/next action rõ ngay từ glance.
- Text Việt dấu chính xác, cỡ đọc tốt, không lỗi glyph; icon một bộ vector; không marker che nội dung.
- Cả năm job status có clean + annotated desktop; các marker trùng khớp ID/bảng; loading/access-hidden/fetch-error/session-expired được mô tả đầy đủ.
- 320px không overflow, mobile 390px dùng được một tay, tablet và desktop cân đối; keyboard/focus/hover/disabled có đặc tả.
- Không suy luận ID, ownership Admin, API enum, terminal mapping, cadence/ETA/progress, thanh toán/ghi danh đã xong, notification delivered, hoặc export URL.
- ZIP mở được và chứa đúng file; `PLAN.md`/`SCREEN.md` có trong gói; nguồn dùng lại được nằm cùng folder.
