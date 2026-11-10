# GS-06 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [GS-06_markers.json](../../screen_stitch/02_guest_discovery/GS-06_tai-nguyen-khoa-hoc/GS-06_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `GS-06-EL-001` | `GS06-EL-01` | Header brand and primary navigation group |
| #2 | `GS-06-EL-002` | `GS06-EL-02` | Login, register and profile-icon group |
| #3 | `GS-06-EL-003` | `GS06-EL-03` | Course route, mock-data and contract-status badges |
| #4 | `GS-06-EL-004` | `GS06-EL-04` | Course title and course-code/mentor subtitle |
| #5 | `GS-06-EL-005` | `GS06-EL-05` | V1 gated-security badge |
| #6 | `GS-06-EL-006` | `GS06-EL-06` | Course tab-navigation group |
| #7 | `GS-06-EL-007` | `GS06-EL-07` | Gated/empty resource-state panel: shield, state label, heading and explanation |
| #8 | `GS-06-EL-008` | `GS06-EL-08` | State-inventory heading, count and guidance text |
| #9 | `GS-06-EL-009` | `GS06-EL-09` | Empty-state inventory card |
| #10 | `GS-06-EL-010` | `GS06-EL-10` | List-state inventory card |
| #11 | `GS-06-EL-011` | `GS06-EL-11` | Disabled download button |
| #12 | `GS-06-EL-012` | `GS06-EL-12` | View-document/integrated-API button |
| #13 | `GS-06-EL-013` | `GS06-EL-13` | Forbidden-state inventory card |
| #14 | `GS-06-EL-014` | `GS06-EL-14` | No-fake-data and data-integrity callout |
| #15 | `GS-06-EL-015` | `GS06-EL-15` | Expired-link inventory card |
| #16 | `GS-06-EL-016` | `GS06-EL-16` | Technical-contract section heading and version badge |
| #17 | `GS-06-EL-017` | `GS06-EL-17` | Hand-off standards card: rhythm, control size, contrast and data integrity |
| #18 | `GS-06-EL-018` | `GS06-EL-18` | API #11 reference card and blocker details |
| #19 | `GS-06-EL-019` | `GS06-EL-19` | API #12 reference card and blocker details |
| #20 | `GS-06-EL-020` | `GS06-EL-20` | UI-unblock criteria panel below both API cards |
| #21 | `GS-06-EL-021` | `GS06-EL-21` | Footer brand and product-description group |
| #22 | `GS-06-EL-022` | `GS06-EL-22` | Footer navigation links |
| #23 | `GS-06-EL-023` | `GS06-EL-23` | Footer copyright notice |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả element

Các marker đánh số component/nhóm nguyên vẹn. Những label/text nằm trong cùng một card được đặc tả bên trong row tương ứng; controls có thể thao tác có marker riêng. Tọa độ marker và target center nằm trong `GS-06_markers.json`.

| Marker / Element ID | Tên, loại, vị trí và mục đích | Thuộc tính, dữ liệu, hiển thị và trạng thái | Sự kiện |
|---|---|---|---|
| #1 `GS06-EL-01` | **Loại/vị trí:** nhóm brand và `<nav>` chính, header trên cùng. Brand “Study2Work LMS”, liên kết Trang chủ/Khóa học/Tìm kiếm. | Static labels/icons; HTML anchors `<a href="#">`, `data-path` lần lượt `trang-chu`, `khoa-hoc`, `tim-kiem`; không có route binding. Visible ở ảnh desktop; responsive behavior chưa kiểm chứng. | `GS06-EV-06`. |
| #2 `GS06-EL-02` | **Loại/vị trí:** nhóm hai link auth và icon profile trang trí, phía phải header. | Hai anchor `href="#"`, `data-path=dang-nhap/dang-ky`; avatar là icon trong `div`, không có handler/role rõ. Không có session data. | `GS06-EV-07`; avatar không phải control theo HTML hiện có. |
| #3 `GS06-EL-03` | **Loại/vị trí:** nhóm ba status/metadata badges (`span`), đầu course header card. | Nội dung viết cứng: `/courses/:courseId?tab=resources`, “Dữ liệu minh họa”, `D (DESIGN_ONLY + BLOCK)`. Đây là metadata prototype, không phải router/runtime status do app trả về. | Không có event. |
| #4 `GS06-EL-04` | **Loại/vị trí:** nhóm heading `<h1>` + subtitle `<p>`, phần trái course header card. | Prototype text: “Chuyên gia Frontend React & TypeScript Enterprise”, `FE-PRO-802`, đơn vị hướng dẫn viết cứng. Khi implement, mọi trường phải map từ course API đã duyệt; API #08 hiện không được nối từ Study Web và các field prototype này chưa xác nhận là source data. | Không có event riêng; phụ thuộc course detail/GS-03. |
| #5 `GS06-EL-05` | **Loại/vị trí:** informational badge (`div`/text), bên phải course header card. | Static icon/text “Bảo mật chuẩn V1 Gated”; không phải kết quả authorization, policy version hay security certification. | Không có event. |
| #6 `GS06-EL-06` | **Loại/vị trí:** nhóm 4 tab anchors trong course navigation bar. Nhãn: Tổng quan, Đề cương (GS-04), Đánh giá (GS-05), Tài nguyên (GS-06). | Bốn anchors `href="#"`; item Resources có active blue treatment trong ảnh. Query route/tab binding chưa có. | `GS06-EV-01`, `GS06-EV-08`. |
| #7 `GS06-EL-07` | **Loại/vị trí:** main state card/panel; shield icon, state label, heading và explanation ở cột trái. | Copy nói tài nguyên chờ cấu hình quyền và link xác thực. Đây là hand-off copy, không chứng minh empty API response. Source tĩnh; loading/error binding không có. | Không có event; initial visible prototype state. |
| #8 `GS06-EL-08` | **Loại/vị trí:** side-panel section heading (`h3`), count badge và supporting paragraph. | Static count/copy. Liệt kê trạng thái thiết kế, không phản ánh số trạng thái runtime đã triển khai. | Không có event. |
| #9 `GS06-EL-09` | **Loại/vị trí:** state-inventory card, cột phải, trạng thái Empty. | Label `Empty (Hiện tại)` và copy gộp “chưa có resource” với “API #11/#12 chưa chốt”. Hai điều kiện phải tách: empty chỉ sau success collection rỗng; contract block là error/unavailable. | Không có event. |
| #10 `GS06-EL-10` | **Loại/vị trí:** state-inventory card, cột phải, trạng thái List. | Copy gợi ý phân loại Bài giảng/Code mẫu/Sách tham khảo khi #11 trả mảng. Catalog không có item enum/cardinality/order; không tự tạo group, category, sort hay pagination. | Không có event; future data state. |
| #11 `GS06-EL-11` | **Loại/vị trí:** disabled `<button>` cùng tooltip trong button wrapper, dưới gated-state copy. Nhãn “Tải gói tài liệu học tập”. | HTML button có `disabled`; visual disabled. Tooltip hidden mặc định, CSS `group-hover:flex group-focus-within:flex`; copy khuyến nghị hoàn thiện #12 signed URL nhưng đây là prototype claim, không phải contract. Không có request, filename, file size hoặc URL. Disabled button không keyboard-focusable nên `focus-within` chưa chứng minh tooltip keyboard-accessible. | `GS06-EV-04` — attempted click bị chặn; `GS06-EV-10` — tooltip reveal state. |
| #12 `GS06-EL-12` | **Loại/vị trí:** internal `<a>` link, cạnh nút tải, trỏ tới technical-contract section. Nhãn “Xem tài liệu tích hợp API”. | Anchor `href="#technical-contract-block"`; nhảy fragment tới contract section. Không gọi API. | `GS06-EV-05`. |
| #13 `GS06-EL-13` | **Loại/vị trí:** state-inventory card, cột phải, trạng thái Forbidden. | Prototype ghi HTTP 403 và yêu cầu đăng ký/xin quyền Mentor. AC-06 có nhánh 403; API catalog/current #12 không khai báo/emit 403. “Xin quyền Mentor” không có flow/API được xác nhận. | Không có event; future state sau contract approval. |
| #14 `GS06-EL-14` | **Loại/vị trí:** informational callout/card dưới gated panel. Title “Quy tắc chuẩn hand-off: Không tạo dữ liệu giả”. | Static warning copy: không dùng tên file/dung lượng/link giả; show collection chỉ khi BE chuẩn hóa. Đây là design instruction và phù hợp nguyên tắc traceability; không phải status response. | Không có event. |
| #15 `GS06-EL-15` | **Loại/vị trí:** state-inventory card, cột phải, trạng thái Expired-Link. | Prototype ghi HTTP 410, TTL timeout và đề xuất tạo lại link. Không có 410, TTL hoặc nút retry thực tế trong current API contract; copy là proposal. | Không có event; future state sau signed-URL contract. |
| #16 `GS06-EL-16` | **Loại/vị trí:** technical-contract section heading (`h3`) + version badge ở đầu section dưới. | Static prototype section anchor `technical-contract-block`; version chưa được xác minh là release/build version. | Nhận fragment navigation từ #12. |
| #17 `GS06-EL-17` | **Loại/vị trí:** standards/information card, cột phải dưới state inventory. | Static quality copy: baseline 4px, control ≥44px, WCAG 2.1 AA, chặn link giả. Dùng design target `.agents/web-study/design.md` để controls ≥44px, nhưng WCAG compliance chưa được đo/verified từ asset. Không phải server validation. | Không có event. |
| #18 `GS06-EL-18` | **Loại/vị trí:** API #11 reference card trong technical-contract section, trái. | Prototype hiển thị `GET /courses/{course_id}/resources`; actual catalog path có prefix `/api/v1`. Card nêu response `Resource` đơn thay vì mảng; đó là discrepancy cần giải quyết, không phải data list. | Không có event; tài liệu tham chiếu. API #11 status `DECLARED_NOT_RUNNABLE`. |
| #19 `GS06-EL-19` | **Loại/vị trí:** API #12 reference card trong technical-contract section, phải. | Prototype path rút gọn `/resources/{resource_id}`; catalog/current server path là `/api/v1/resources/{resource_id}`. Card đề cập public/private và signed URL nhưng signer chưa có trong current code. | Không có event; tài liệu tham chiếu. API #12 current source-backed nhưng AC-06 access policy chưa giải quyết. |
| #20 `GS06-EL-20` | **Loại/vị trí:** criteria callout (`div` + `<ul>`) dưới hai API cards. Heading “Điều kiện mở khóa giao diện người dùng”. | Nêu `{ items: Resource[], total: number }`, signed URL TTL + RBAC, gateway mang token. Cả ba đều là prototype proposal; catalog hiện khai báo `ApiEnvelope<Resource>` public/no Bearer và không có total/expiry. Không dùng như request/response contract. | Không có event. |
| #21 `GS06-EL-21` | **Loại/vị trí:** footer brand/product-description group, phía trái footer. | Static brand, tagline, separators/icons. No current dynamic/configured content. | Không có event. |
| #22 `GS06-EL-22` | **Loại/vị trí:** footer `<nav>` group, giữa footer. Links: Chương trình đào tạo, Tra cứu chứng chỉ, Quy chế học vụ, Hỗ trợ học viên. | Bốn anchors `href="#"`; `data-path` chỉ chứa giá trị prototype, không có route mapping. | `GS06-EV-09`. |
| #23 `GS06-EL-23` | **Loại/vị trí:** copyright text, phía phải footer. | Static `© 2025 Study2Work. All rights reserved.`; display copy, không phải dữ liệu API hoặc ngày build. | Không có event. |

## 4. Conditional UI & state variations
- States theo inventory: empty/list/forbidden/expired-link
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/02_guest_discovery/GS-06_tai-nguyen-khoa-hoc/GS-06.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
