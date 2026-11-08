# SH-06 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `SH-06-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Thông báo 404 không tiết lộ draft/private, cung cấp quay về khóa học.
- Gate/status (giữ nguyên): **D**
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: 8. Bảo mật, accessibility và design system

- API #08 chỉ query `PUBLISHED`; 404 message current source chung cho invalid/missing/unpublished. UI không hiển thị draft/private status, record ID, raw exception, SQL, stack trace hoặc error body thô.
- Không “đoán” resource đã bị xóa/dời; description dùng thông tin trung tính cho “không tìm thấy/không khả dụng”. Không render course cards nếu không có ID và source được phê duyệt.
- Không có authentication trên API #08 current route; client không thêm Bearer requirement cho public request. Nếu một flow khác trả 403, dùng SH-05.
- Header account icon hiện 32×32 `div`, không phải control. Không đổi nó thành profile button nếu chưa có route/requirement.
- Link/bàn phím: mọi anchors phải có href thật, hover/focus-visible/pressed; nav hiện bị ẩn dưới `md` nhưng không có menu alternative. Card link needs accessible name from course title and real route ID. Browser back follows router history; no custom back behavior specified.
- `h1=404` + `h2` error heading cần heading outline rõ; status không chỉ dựa vào màu. Background circles là decorative, hidden khỏi accessibility tree. Hit targets tối thiểu 44×44px; header/footer controls và account icon cần review.
- Study guide hướng dẫn font system/Inter local, content width khoảng 1120px và semantic color token. Prototype tải Google Fonts/Tailwind CDN, max-width 1440px, large decorative gradients và màu thương hiệu khác; cần chuyển về guide ở implementation. Giữ nguyên nguồn PNG.
- Course data/database source query dùng `courses`/`users`, nhưng DDL chỉ là committed design artifact; live schema/deployment chưa xác minh. `mentor_id` nullable trong DDL, trong khi course mapper yêu cầu mentor summary; lỗi mapping hiện trả 500.

### Trích từ DD nguồn: 9. Blocker, discrepancy và câu hỏi mở

| ID | Phân loại | Evidence | Tác động / owner |
|---|---|---|---|
| `SH06-B01` | `DD BLOCKER: SH06_PRODUCTION_SURFACE_UNDECIDED` | Recommendation heading/cards, help/contact, footer links/copyright xuất hiện trong prototype nhưng không có approved content/data/route contract; links dùng `href="#"`. | Product/UX chốt giữ/bỏ và contract của từng surface; không triển khai mock data hay destination tự suy. |
| `SH06-B02` | `DD BLOCKER: AC05_NOT_FOUND_STATUS_CONFLICT` | AC-05 ghi `404/403` cho course không tồn tại/PUBLISHED; API catalog ghi 404/500; handler #08 có 404 cho invalid/missing/unpublished và 500 cho internal error, không có 403. | Owner AC/API xác nhận sửa AC hay bổ sung nghĩa vụ 403; tới khi đó mô tả current #08 và giữ 403 bên ngoài #08. |
| `SH06-D01` | `DISCREPANCY: API_08_STATUS_LABELS_VS_SOURCE` | Dòng SH-06 trong `list_screen.md` ghi BE `D`, API index §5 ghi #008 `R`, API contract tổng thể là approved design nhưng chưa runtime-verified, API DD #08 còn draft; `app/api/v1.py`, module/query/model/helper/test source hiện có. | Giữ riêng nhãn inventory, contract/DD, source và deployment; không gọi `RUNTIME VERIFIED` nếu chưa xác minh deployment. |
| `SH06-I01` | `IMPLEMENTATION BLOCKER: STUDY_WEB_ROUTER_NOT_FOUND` | `apps/study-client/src/` và package manifest không có; ignored dist bundle không chứa route identifier và không có source rebuild. | Frontend xác nhận route fallback, `/not-found`, static host/SPA behavior và navigation paths; không xem đây là runtime evidence. |
| `SH06-D02` | `DESIGN_SYSTEM_DRIFT` | Remote font/Tailwind CDN, max-width 1440px, responsive nav ẩn ở small viewport và profile icon không có semantics; Study guide nêu convention khác. | Product/UX xác nhận guide có hiệu lực với prototype này; implementation dùng design tokens sau khi được chốt. |
| `SH06-D03` | `DB_LIVE_NOT_VERIFIED` | DDL có bảng/columns, nhưng live schema chưa được kiểm tra. | Không khẳng định dữ liệu production hoặc trạng thái khóa học từ DDL alone. |

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
