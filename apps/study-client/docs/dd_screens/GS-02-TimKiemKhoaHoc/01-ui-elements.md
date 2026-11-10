# GS-02 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [GS-02_markers.json](../../screen_stitch/02_guest_discovery/GS-02_tim-kiem-khoa-hoc/GS-02_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `GS-02-EL-001` | `GS02-EL-01` | Header brand and primary navigation group |
| #2 | `GS-02-EL-002` | `GS02-EL-02` | Header global search input |
| #3 | `GS-02-EL-003` | `GS02-EL-03` | Header notification and avatar utility group |
| #4 | `GS-02-EL-004` | `GS02-EL-04` | Breadcrumb navigation |
| #5 | `GS-02-EL-005` | `GS02-EL-05` | Main query form with input, clear affordance and submit |
| #6 | `GS-02-EL-006` | `GS02-EL-06` | Popular keyword prompt and suggestion chips |
| #7 | `GS-02-EL-007` | `GS02-EL-07` | Search query and result summary with count |
| #8 | `GS-02-EL-008` | `GS02-EL-08` | Sort select |
| #9 | `GS-02-EL-009` | `GS02-EL-09` | Grid and list view toggle group |
| #10 | `GS-02-EL-010` | `GS02-EL-10` | Active filter chips and clear-all affordance |
| #11 | `GS-02-EL-011` | `GS02-EL-11` | Filter sidebar heading and reset action |
| #12 | `GS-02-EL-012` | `GS02-EL-12` | Six-card search results grid as reusable card instances |
| #13 | `GS-02-EL-013` | `GS02-EL-13` | Training-field category checkbox group |
| #14 | `GS-02-EL-014` | `GS02-EL-14` | Skill-level radio group |
| #15 | `GS-02-EL-015` | `GS02-EL-15` | Duration radio group |
| #16 | `GS-02-EL-016` | `GS02-EL-16` | Minimum-rating radio group |
| #17 | `GS-02-EL-017` | `GS02-EL-17` | Tuition checkbox group |
| #18 | `GS-02-EL-018` | `GS02-EL-18` | Apply-filters button |
| #19 | `GS-02-EL-019` | `GS02-EL-19` | Career-path recommendation panel |
| #20 | `GS-02-EL-020` | `GS02-EL-20` | Career-path view CTA |
| #21 | `GS-02-EL-021` | `GS02-EL-21` | Tech advisor CTA |
| #22 | `GS-02-EL-022` | `GS02-EL-22` | Displayed result range 1–6 of 12 |
| #23 | `GS-02-EL-023` | `GS02-EL-23` | Previous, page-number and next pagination group |
| #24 | `GS-02-EL-024` | `GS02-EL-24` | Footer brand, description and accreditation badges |
| #25 | `GS-02-EL-025` | `GS02-EL-25` | Footer navigation columns |
| #26 | `GS-02-EL-026` | `GS02-EL-26` | Copyright and tagline |

## 3. Đặc tả từng element

### Trích từ DD nguồn: 3. Element chi tiết

Một marker xác định một component logic. Marker #12 đại diện cho grid component; sáu card hiển thị là các instance lặp lại của component đó. Mỗi control con và field visual chưa được API hỗ trợ được mô tả trong hàng tương ứng thay vì xem là dữ liệu runtime đã có.

| # / Element ID | Tên, loại, vị trí | Thuộc tính, nguồn dữ liệu và validation | Hiển thị, trạng thái, sự kiện |
|---|---|---|---|
| 1 / GS02-EL-01 | Nhóm logo/brand và navigation chính, header trái | Nội dung/đích link theo asset. Các route ngoài GS-01 chưa được xác nhận. | Luôn thấy trong ảnh. Default/active state theo route cần router. EV-15. |
| 2 / GS02-EL-02 | Ô tìm kiếm global ở header | Screenshot cho thấy input riêng với form chính. Không có quy tắc đồng bộ q, submit hay API riêng. | Visible trong ảnh, absent trong HTML. EV-16. |
| 3 / GS02-EL-03 | Nhóm notification, avatar và tiện ích tài khoản | Không có unread count, menu, account endpoint hay route contract trong phạm vi nguồn đã trace. | Visible trong ảnh; mâu thuẫn Guest actor/header của HTML. EV-17. |
| 4 / GS02-EL-04 | Breadcrumb navigation | Label/đường về GS-01 là kỳ vọng điều hướng; href trong runtime không có. | Visible; EV-15. |
| 5 / GS02-EL-05 | Form tìm kiếm chính: text input, clear affordance, submit | q là chuỗi từ người dùng/URL. API không công bố giới hạn độ dài; không tự đặt max length. Expected trim/lowercase, debounce và URL sync; debounce interval, case display và xử lý q rỗng chưa được chốt. HTML có GET form name=q, không có URL hydration và không có nút clear hiện hành. | Default có thể được nạp từ URL theo expected flow; focus/typing/loading/result/error cần style. EV-02, EV-03, EV-04. |
| 6 / GS02-EL-06 | Prompt từ khóa phổ biến và nhóm suggestion chips | Label/value xuất hiện trong screenshot nhưng không có preset source hoặc contract. Không giả định chip tự submit hay chỉ điền input. | Visible trong screenshot, absent trong HTML. EV-05. |
| 7 / GS02-EL-07 | Tóm tắt q/kết quả và tổng số | q từ URL/state; tổng số từ data.pagination.total của #07. Screenshot có tổng 12; không dùng con số mẫu làm dữ liệu thật. | Loading/ready/empty/error mapping cần tách. EV-01, EV-14. |
| 8 / GS02-EL-08 | Select sort kết quả | API cho phép id, name, price, created_at, mỗi field với asc/desc; default source là created_at DESC, id ASC. Không có API field/score “Phù hợp nhất”. | Screenshot hiện nhãn “Phù hợp nhất”; option mapping bị chặn. EV-11. |
| 9 / GS02-EL-09 | Toggle grid/list | State grid/list theo visual; không có API liên quan. HTML có helper toggle nhưng DOM target/call site không tồn tại. | Screenshot có hai chế độ; state và persistence chưa được xác định. EV-12. |
| 10 / GS02-EL-10 | Chip filter đang bật và hành động xóa tất cả | Tên/giá trị filter là visual; chưa có nguồn state hoặc contract. Không gửi unsupported query. Chưa rõ “clear all” có xóa q hay chỉ filter. | Conditional khi có filter; có trong screenshot, không có HTML. EV-10. |
| 11 / GS02-EL-11 | Tiêu đề sidebar và nút reset | Reset semantics chưa rõ: xóa toàn bộ facet, giữ q, sort hay cả hai. HTML helper không có sidebar DOM. | Visible trong screenshot. EV-09. |
| 12 / GS02-EL-12 | Grid kết quả gồm sáu card instance trong ảnh | API #07 item fields: id, title, optional description, optional thumbnail_url, price dạng decimal string, status, mentor{id,full_name,avatar_url?}. Không có category, currency, rating, duration, tags hoặc discount/old price. Một marker bao phủ reusable card grid; response item id là định danh duy nhất cho điều hướng. | Loading skeleton, ready, empty và error cần thiết kế; card screenshot không gắn ID API. EV-13. |
| 13 / GS02-EL-13 | Nhóm checkbox danh mục đào tạo | Metadata có thể đọc từ #05: id, name, slug, description?. #05 trả category ACTIVE theo locale. API #07 từ chối mọi category khác null; DDL không có relation course-category. Không gửi filter. | Visible trong screenshot; selection chỉ là visual/prototype state cho tới khi contract được cập nhật. EV-06. |
| 14 / GS02-EL-14 | Nhóm radio trình độ | Giá trị/options nhìn thấy là thiết kế, không có query parameter hoặc field backend. Không tạo enum/validation mới. | Screenshot only; không thể lọc kết quả theo source hiện tại. EV-07. |
| 15 / GS02-EL-15 | Nhóm radio thời lượng | Giá trị/options và cách xác định duration không có trong #07 response/schema đã trace. | Screenshot only; EV-07. |
| 16 / GS02-EL-16 | Nhóm radio rating tối thiểu | #07 không trả rating hoặc số lượt đánh giá; không có filter param. | Screenshot only; EV-07. |
| 17 / GS02-EL-17 | Nhóm checkbox học phí | #07 trả price nhưng không trả currency hoặc các nhãn tier/discount trong ảnh; không có query filter theo tuition. | Screenshot only; EV-07. |
| 18 / GS02-EL-18 | Nút áp dụng filter | Payload visual có thể gồm category, skill, duration, rating, tuition; chưa có contract hỗ trợ. Không gửi request #07 với các filter này. | Visible trong screenshot. Hành động bị chặn; EV-08. |
| 19 / GS02-EL-19 | Panel khuyến nghị lộ trình nghề nghiệp | Nội dung biên tập trong ảnh; không thấy API/route trong inventory GS-02 hoặc source đã trace. | Visible trong screenshot; route/service unresolved. EV-18. |
| 20 / GS02-EL-20 | CTA “Xem Lộ trình nghề nghiệp” | Không có destination route/parameter contract đã xác minh. | Visible; click behavior chưa xác nhận. EV-18. |
| 21 / GS02-EL-21 | CTA “Hỏi cố vấn Tech” | Không có contact service/route/API đã xác minh. | Visible; click behavior chưa xác nhận. EV-18. |
| 22 / GS02-EL-22 | Dải hiển thị khoảng kết quả, ví dụ 1–6 / 12 | API pagination có page, size=20, total, total_pages. Range nên tính từ response nếu UI dùng server page; công thức cho page rỗng cần tránh hiển thị số âm. Screenshot 1–6/12 mâu thuẫn với size 20. | Visible trong screenshot; loading/empty states cần ẩn hoặc thay copy theo thiết kế chưa duyệt. EV-14. |
| 23 / GS02-EL-23 | Pagination trước/số trang/tiếp | API page mặc định 1, size cố định 20. size không phải query input. Page<1 trả 422; page ngoài phạm vi trả 200 với items rỗng nhưng total giữ nguyên. | Screenshot có page 1/2 theo size 6, không thể map trực tiếp. EV-14. |
| 24 / GS02-EL-24 | Nhóm brand/footer description/accreditation badges | Nội dung và logo trong asset chưa có API/source data. Không coi badge là chứng nhận thực tế nếu chưa được xác nhận. | Visible trong screenshot, không có trong HTML prototype phần footer này. EV-19. |
| 25 / GS02-EL-25 | Các cột link footer | Destination và quyền truy cập chưa truy vết được tới router hiện hành. | Visible trong screenshot. EV-19. |
| 26 / GS02-EL-26 | Copyright/tagline cuối trang | Nội dung tĩnh theo asset; năm/brand chưa được cấu hình từ source. | Visible trong screenshot. Không có event tương tác đã xác nhận. |

## 4. Conditional UI & state variations
- States theo inventory: typing/loading/no-result/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/02_guest_discovery/GS-02_tim-kiem-khoa-hoc/GS-02.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
